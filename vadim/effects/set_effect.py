import os
import time

def set_template(image_url, template_id):
    cmd = '''
    curl -v -X POST "http://api-soft.photolab.me/template_process.php" \
        -F image_url[1]={} \
        -F rotate[1]=0 \
        -F flip[1]=0 \
        -F crop[1]=0,0,1,1 \
        -F template_name="{}"
    '''.format(image_url, template_id)
    b = os.popen(cmd,'r',1)
    return b.readlines()[0]

image_url = 'https://sun9-18.userapi.com/c857128/v857128987/206b/wKyX8pQOABs.jpg'
template_id = '1'
print(set_template(image_url, template_id))
