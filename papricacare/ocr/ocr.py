import io, os
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS
from base64 import b64decode, b64encode
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

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
    #print(text, cnt_num,cnt_char,cnt_special)
    if cnt_num >= 13 and '-' in text: # 주민번호 패턴
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

def process(attr):    
    src = attr.get('img_src', None)
    is_privacy = attr.get('is_privacy', False)
    is_num = attr.get('is_num', False)
    is_char = attr.get('is_char', False)

    is_drug = attr.get('is_drug', False)
    is_disease = attr.get('is_disease', False)
    is_hosp = attr.get('is_hosp', False)
   
    data_uri = src
    header, encoded = data_uri.split(",", 1)
    data = b64decode(encoded)
    
    src = '.temp.temp'
    fp = io.open(src, 'wb')
    fp.write(data)
    fp.close()
        
    texts = detect_text(src)
    candidates = []
    
    if is_drug:
        import drug
        for i in range(1, len(texts)):
            p_code = texts[i].description
            # print(f'{p_code}:{len(p_code)}')
            try:
                cnt_num, cnt_char, cnt_special = count_chars(p_code)
                if cnt_num >= 8:
                    p = drug.models.Product.objects.filter(prod_code__contains=p_code)
                    for c in p:
                        print(f'- A possible drug code: "{c}"')
                        r = drug.models.Registration.objects.get(pk=c.reg_code)
                        if c.ing_code: # becasue fk is handled to keep going by nulll 
                            i = drug.models.Ingredient.objects.get(pk=c.ing_code)
                            if i.ing_form_id:
                                f = drug.models.IngreForm.objects.get(pk=i.ing_form_id)
                                if f.ing_id:
                                    d = drug.models.IngreDesc.objects.get(pk=f.ing_id)
                                    drug_info = {'drug_name':r.drug_name, 
                                                 'form_name':f.ing_name_kr,
                                                 'one_liner_kr':d.one_liner_kr}
                                else:
                                    drug_info = {'drug_name':r.drug_name,
                                                 'form_name':f.ing_name_kr}
                            else:
                                drug_info = {'drug_name':r.drug_name}
                                    
                            if drug_info not in candidates: 
                                candidates.append(drug_info)
                        else: # case that the fk:ing_code = null
                            drug_info = {'drug_name':r.drug_name}
                            if drug_info not in candidates: 
                                candidates.append(drug_info)                               
            except ObjectDoesNotExist:
                    pass    
                
    if len(texts) == 0 or (is_privacy == False and is_num == False and is_char == False):
        return (texts, None)
    
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
    if os.path.exists(src):
        os.remove(src)
    try:
        exif = im._getexif()
        
        if exif and len(exif):
            ori = exif[274] # orientation info 1:normal 6: on right side (gyro-rotated)
            if ori != 1:
                im = im.transpose(Image.ROTATE_270)
    except AttributeError: # error when calling _getexif()
        pass
    except Exception: # error when reading exif[278...]
        pass
    
    draw = ImageDraw.Draw(im)
    
    for p in privacies:
        draw.rectangle(xy=p,fill='red')
    output = '.safe.png'
    im.save(output)
    
    header = b'data:image/png;base64,'
    fp = open(output, 'rb')
    content = fp.read()
    fp.close()
    if os.path.exists(output):
        os.remove(output)
    data_url = header + b64encode(content)
    output = data_url.decode('utf-8')

    return (candidates, output)
                        