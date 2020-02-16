import os
import time
import resources

def set_template(url, template_id):
    cmd = '''
    image_url = "http://vadimpy.pythonanywhere.com/frames/" + str(url) + ".jpg"
    curl -v -X POST "http://api-soft.photolab.me/template_process.php" \
        -F image_url[1]={} \
        -F rotate[1]=0 \
        -F flip[1]=0 \
        -F crop[1]=0,0,1,1 \
        -F template_name="{}"
    '''.format(image_url, template_id)
    b = os.popen(cmd,'r',1)
    save_name = "~/vadimpy/tiktok/server/frames/" + str(url) + ".jpg"
    f=open(save_name,'wb+')
    ufr = requests.get(b.readlines()[0])
    f.write(ufr.content)
    f.close()
	
