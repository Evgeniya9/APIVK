import requests
from progress.bar import IncrementalBar

bar_photos_get = IncrementalBar('Photos get', max=1)
bar_photos_get = IncrementalBar('Photos get', max=1)
class VK:


    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version, 'user_id': self.id}


    def users_info(self):

        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})

        return response.json()

    def photos_get(self, count):
        param = {'access_token': self.token, 'v': self.version, 'owner_id': self.id, 'album_id': 'profile', 'extended': '1', 'count': count}
        response = requests.get(f'https://api.vk.com/method/photos.get', params=param)
        bar_photos_get.next()
        bar_photos_get.finish()

        return response.json()

class yandex_disk:
    base_URL = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self, access_token):
        self.token = access_token
        self.params = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {access_token}'}

    def upload_photos(self, vk_photos):
        bar_photos_upload = IncrementalBar('Photos get', max=len(vk_photos['response']['items']))
        response = requests.put(f'{self.base_URL}/resources?path=%2Fphotos', headers=self.params)

        for item in vk_photos['response']['items']:
            photo_url = item['sizes'][-1]['url']
            photo_likes_count = str(item['likes']['count'])
            res = requests.post(f'{self.base_URL}/resources/upload?path=%2Fphotos%2F{photo_likes_count}&url={photo_url}', headers=self.params)
            bar_photos_upload.next()

        bar_photos_upload.finish()

access_token = ''
user_id = ''
vk = VK(access_token, user_id)

access_token_yandex = ''
ya_disk = yandex_disk(access_token_yandex)

ya_disk.upload_photos(vk.photos_get(8))



