import requests

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

    def photos_get(self):
        param = {'access_token': self.token, 'v': self.version, 'user_id': self.id, 'album_id': 'profile', 'extended': '1'}
        response = requests.get(f'https://api.vk.com/method/photos.get', params=param)

        return response.json()

class yandex_disk:
    base_URL = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self, access_token):
        self.token = access_token
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {access_token}'}

    def upload_photos(self, vk_photos):
        response = requests.put(f'{self.base_URL}/resources?path=%2Fphotos', headers=self.headers)

        for item in vk_photos['response']['items']:
            photo_url = item['sizes'][-1]['url'].replace(':', '%3A').replace('/', '%2F').replace('?', '%3F').replace('=', '%3D').replace('&', '%26')
            photo_likes_count = str(item['likes']['count'])
            res = requests.post(f'{self.base_URL}/resources/upload?path=%2Fphotos%2F{photo_likes_count}&url={photo_url}', headers=self.headers)

access_token = ''
user_id = ''
vk = VK(access_token, user_id)

access_token_yandex = ''
ya_disk = yandex_disk(access_token_yandex)

ya_disk.upload_photos(vk.photos_get())


