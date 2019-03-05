import io
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    '''
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    '''
    content = path.split('/') # 0: 'data:image' 1: 'type';basexx 
    image = vision.types.Image(content=bytes(content[2],'utf-8'))
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

def is_serial_num(text):
    num = sum(c.isdigit() for c in text )
    
    if num >= 7 and '-' in text: 
        return True
    else:
        return False
    
def erase_privacies(src, sink, is_show):
    texts = detect_text(src)
    
    if len(texts) == 0:
        return None
    # print(texts[0].description
    privacies=[]

    for i in range(1, len(texts)-1):
        if texts[i].description.startswith('주민등록'):
            coord = []
            vertex = texts[i+1].bounding_poly.vertices[0]
            coord.append((vertex.x,vertex.y))
            vertex = texts[i+1].bounding_poly.vertices[2]
            coord.append((vertex.x,vertex.y))       
            privacies.append(coord)
            break;
        else:
            if is_serial_num(texts[i].description):
                coord = []
                vertex = texts[i].bounding_poly.vertices[0]
                coord.append((vertex.x,vertex.y))
                vertex = texts[i].bounding_poly.vertices[2]
                coord.append((vertex.x,vertex.y))       
                privacies.append(coord)
                break;

    im = Image.open(src)
    exif = im._getexif()
    
    if len(exif):
        ori = exif[274] # orientation info 1:normal 6: on right side (gyro-rotated)
        if ori != 1:
            im = im.transpose(Image.ROTATE_270)
    
    draw = ImageDraw.Draw(im)
    
    for p in privacies:
        draw.rectangle(xy=p,fill='red')
        
    im.save(sink)
    if is_show:
        im.show()
        
    return privacies
                        