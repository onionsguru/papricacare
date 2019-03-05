import io
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS
from base64 import b64decode, b64encode
from django.urls import reverse

def count_chars(text):
    cnt_num, cnt_char, cnt_special = 0, 0, 0
    str_c = ['/', '#', '-', '*'] # this set should be tuned up againt new cases    
    for c in text:
        if c.isalpha(): cnt_char += 1
        elif c.isnumeric(): cnt_num += 1
        elif c in str_c: cnt_special += 1
    return (cnt_num, cnt_char, cnt_special)

def is_serial_num(text):
    cnt_num, cnt_char, cnt_special = count_chars(text)
    
    # print(text, cnt_num,cnt_char,cnt_special)

    if cnt_num >= 13 and '-' in text: # 주민번호 패턴
        return True
    elif cnt_special == 0 and \
    (cnt_num >= 6 and cnt_num <= 7 and cnt_char== 1): # 자동차번호 패턴
        return True
    elif cnt_special == 0 and cnt_char == 0 and cnt_num == 8: # 요양기관기호
        return True
    else:
        return False
    
def is_anynum(text):
    cnt_num, cnt_char, cnt_special = count_chars(text)
    if cnt_num > 0: 
        return True
    else:
        return False
    
def is_anychar(text):
    cnt_num, cnt_char, cnt_special = count_chars(text)
    if cnt_char > 0: 
        return True
    else:
        return False 
    
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        data = image_file.read()
    
    image = vision.types.Image(content=data)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

def erase(src, **kwargs):
    type = kwargs.get('type', None)
    is_privacy = kwargs.get('is_privacy', False)
    is_num = kwargs.get('is_num', False)
    is_char = kwargs.get('is_char', False)
   
    if type == 'dataurl':
        data_uri = src
        header, encoded = data_uri.split(",", 1)
        data = b64decode(encoded)
        
        src = '.temp.temp'
        fp = io.open(src, 'wb')
        fp.write(data)
        fp.close()
        
    texts = detect_text(src)
    
    if len(texts) == 0:
        print('OCR results in nothing!')
        return None
    # print(texts[0].description
    privacies=[]

    for i in range(1, len(texts)):
        if (is_privacy and is_serial_num(texts[i].description)) \
            or (is_num and is_anynum(texts[i].description)) \
            or (is_char and is_anychar(texts[i].description)):
            
            coord = []
            vertex = texts[i].bounding_poly.vertices[0]
            coord.append((vertex.x,vertex.y))
            vertex = texts[i].bounding_poly.vertices[2]
            coord.append((vertex.x,vertex.y))       
            privacies.append(coord)
        
    im = Image.open(src)
    
    try:
        exif = im._getexif()
        
        if exif and len(exif):
            ori = exif[274] # orientation info 1:normal 6: on right side (gyro-rotated)
            if ori != 1:
                im = im.transpose(Image.ROTATE_270)
    except AttributeError:
        pass
    
    draw = ImageDraw.Draw(im)
    
    for p in privacies:
        draw.rectangle(xy=p,fill='red')
    output = '.safe.png'
    im.save(output)
    
    if type == 'dataurl':
        header = b'data:image/png;base64,'
        fp = open(output, 'rb')
        content = fp.read()
        fp.close()
        data_url = header + b64encode(content)
        output = data_url.decode('utf-8')
  
    return output
                        