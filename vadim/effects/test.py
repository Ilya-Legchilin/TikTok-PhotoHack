from client_photolab import ClientPhotolab
import os.path

api = ClientPhotolab()

resourses_filename = 'resources.zip'
if not os.path.exists(resourses_filename):
    api.download_file('http://soft.photolab.me/samples/resources.zip', resourses_filename)

content_filename = 'girl.jpg'
if not os.path.exists(content_filename):
    api.download_file('http://soft.photolab.me/samples/girl.jpg', content_filename)


content_url = api.image_upload(content_filename)
print('content_url: {}'.format(content_url))

template_name = api.template_upload(resourses_filename)
print('template_name: {}'.format(template_name))


result_url = api.template_process(template_name, [{
    'url' : content_url,
    'rotate' : 0,
    'flip' : 0,
    'crop' : '0,0,1,1'
}])
print('for template_name: {}, result_url: {}'.format(template_name, result_url))

for combo_id in [5635874, 3124589]:
    original_content_url = content_url
    print('===')
    print('start process combo_id: {}'.format(combo_id))
    i = 0
    for step in api.photolab_steps_advanced(combo_id)['steps']:
        template_name = str(step['id'])
        contents = []
        for i in range(0, len(step['image_urls'])):
            image_url = step['image_urls'][i]
            if len(step['image_urls'][i]) == 0:
                image_url = original_content_url
            contents.append({
                'url'       : image_url,
                'rotate'    : 0,
                'flip'      : 0,
                'crop'      : '0,0,1,1'
            })
        if len(contents) == 0:
            contents.append({
                'url'       : original_content_url,
                'rotate'    : 0,
                'flip'      : 0,
                'crop'      : '0,0,1,1'
            })
        result_url = api.photolab_process(template_name, contents)
        i = i + 1
        if i != 0:
            original_content_url = result_url
        print('---for template_name: {}, result_url: {}'.format(template_name, result_url))

    print('result_url: {}'.format(result_url))
