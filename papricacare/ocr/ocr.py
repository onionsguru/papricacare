import io, os
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS
from base64 import b64decode, b64encode
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

'''
 vertex = texts[i].bounding_poly.vertices[0]
            coord.append((vertex.x,vertex.y))
'''

def get_collective_texts(title_list, text):
    candidates = dict()
    
    for tl in title_list:
        if t in tl:
            if text not in candidates.keys():
                candidates[tl] = text
            else:
                print('overwritten with keys!')
                    
    for c in candidates:
        print(c.description)
                

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
    data_url = attr.get('img_src', None)
    is_privacy = attr.get('is_privacy', False)
    is_num = attr.get('is_num', False)
    is_char = attr.get('is_char', False)

    is_drug = attr.get('is_drug', False)
    is_disease = attr.get('is_disease', False)
    is_hosp = attr.get('is_hosp', False)
   
    header, encoded = data_url.split(",", 1)
    data = b64decode(encoded)
    
    src = '.temp.temp'
    fp = io.open(src, 'wb')
    fp.write(data)
    fp.close()
        
    texts = detect_text(src)
    candidates = []
    hospital_info = '-'
    disease_info = []
    issue_date_info = '2018-04-03'
    
    if is_drug or is_hosp or is_disease:
        import drug, hospital, disease
        for i in range(1, len(texts)):
            p_code = texts[i].description
            p_code_len = len(p_code)
            print(f'{p_code}:{p_code_len}')
            try:
                cnt_num, cnt_char, cnt_special = count_chars(p_code)
                if is_drug and cnt_char == 0 and cnt_special == 0 and cnt_num >= 9: # drug code
                    p = drug.models.Product.objects.filter(prod_code__contains=p_code)
                    for c in p:
                        r = drug.models.Registration.objects.get(pk=c.reg_code)
                        print(f'- A possible drug: "({p_code} -> {c.prod_code})"')

                        drug_info = {"reg_code": c.prod_code, "drug_name": r.drug_name, "dose":"-", "qty_perday":"-"}
                        if drug_info not in candidates:
                            candidates.append(drug_info);
                elif is_hosp and cnt_special >= 2 and cnt_char == 0 and cnt_num >= 7: # phone number
                    p = hospital.models.Hospital.objects.get(phone=p_code)
                    hospital_info = {"name": p.name}
                elif is_disease and cnt_num >=3 and cnt_num <=4:
                    if p_code[0].isalpha() or p_code[0] == '1' :
                        if '.' not in p_code:
                            pp_code = p_code[0:3] + '.' + p_code[3:]
                        else:
                            pp_code = p_code
                            
                        if pp_code[0] == '1': # for ocr typo
                            pp_code = 'I' + pp_code[1:]
                        d = disease.models.Disease.objects.get(code=pp_code)         
                        temp = {"code": d.code, "name": d.name_kr}
                        if temp not in disease_info:
                            disease_info.append(temp)

            except ObjectDoesNotExist as details:
                    print(details.args[0])
        
        # get_collective_texts(['질병분류기호'], texts[i])
                
    if len(texts) == 0 or (is_privacy == False and is_num == False and is_char == False):
        return (disease_info, hospital_info, issue_date_info, candidates, '#')
    
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
        draw.rectangle(xy=p,outline='red', fill='red')
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

    return (disease_info, hospital_info, issue_date_info, candidates, output)
                        
