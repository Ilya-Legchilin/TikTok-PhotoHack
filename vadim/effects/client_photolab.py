import requests
import logging
import json

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(filename)s:%(lineno)d - %(message)s')

class ClientPhotolab(object):

    api_endpoint = 'http://api-soft.photolab.me'
    api_upload_endpoint = 'http://upload-soft.photolab.me/upload.php?no_resize=1'
    api_endpoint_proxy = 'http://api-proxy-soft.photolab.me'

    def image_upload(self, image):
        image_blob = None
        if type(image) is str:
            image_blob = open(image, 'rb')
        elif type(image) is file:
            image_blob = file
        else:
            raise Exception('image not file and not filename')

        files = {'file1': image_blob}
        response = requests.post(self.api_upload_endpoint, files=files)
        resp_body = response.text
        logging.info('response: {}'.format(resp_body))
        return resp_body

    def template_upload(self, resources):
        resources_blob = None
        if type(resources) is str:
            resources_blob = open(resources, 'rb')
        elif type(resources) is file:
            resources_blob = file
        else:
            raise Exception('resources not file and not filename')

        files = {'resources': resources_blob}
        endpoint = '{}/template_upload.php'.format(self.api_endpoint_proxy)
        response = requests.post(endpoint, files=files)
        resp_body = response.text
        logging.info('response: {}'.format(resp_body))
        return resp_body

    def template_process(self, template_name, contents):
        form = {
            'template_name' : template_name
        }
        for i in range(0, len(contents)):
            content = contents[i]
            form['image_url[' + str(i+1) + ']'] = content['url']
            if 'crop' in content:
                form['crop[' + str(i+1) + ']'] = content['crop']
            if 'flip' in content:
                form['flip[' + str(i+1) + ']'] = content['flip']
            if 'rotate' in content:
                form['rotate[' + str(i+1) + ']'] = content['rotate']


        endpoint = '{}/template_process.php'.format(self.api_endpoint)
        return self._query(endpoint, data=form)

    def photolab_process(self, template_name, contents):
        form = {
            'template_name' : template_name
        }
        for i in range(0, len(contents)):
            content = contents[i]
            form['image_url[' + str(i+1) + ']'] = content['url']
            if 'crop' in content:
                form['crop[' + str(i+1) + ']'] = content['crop']
            if 'flip' in content:
                form['flip[' + str(i+1) + ']'] = content['flip']
            if 'rotate' in content:
                form['rotate[' + str(i+1) + ']'] = content['rotate']

        endpoint = '{}/template_process.php'.format(self.api_endpoint)
        return self._query(endpoint, data=form)

    def photolab_steps(self, combo_id):
        form = {
            'combo_id' : combo_id
        }
        endpoint = '{}/photolab_steps.php'.format(self.api_endpoint)
        return json.loads(self._query(endpoint, data=form))

    def photolab_steps_advanced(self, combo_id):
        form = {
            'combo_id' : combo_id
        }
        endpoint = '{}/photolab_steps_advanced.php'.format(self.api_endpoint)
        return json.loads(self._query(endpoint, data=form))

    def download_file(self, endpoint, dst):
        response = requests.get(endpoint)
        if response.status_code == 200:
            try:
                f = open(dst, 'wb')
            except IOError as e:
                raise e
            else:
                with f:
                    f.write(response.content)
                    f.close()
        else:
            raise Exception('_query: {}, status_code: {}'.format(endpoint, response.status_code))

    def _query(self, endpoint, data=None, files=None):
        response = requests.post(endpoint, data=data, files=files)
        resp_body = response.text
        logging.info('response: {}'.format(resp_body))
        if response.status_code != 200:
            raise Exception('_query: {}, error: {}'.format(endpoint, resp_body))

        return resp_body
