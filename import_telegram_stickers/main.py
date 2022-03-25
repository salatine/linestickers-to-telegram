from dataclasses import dataclass
import json
from typing import Tuple
import requests
import io
from PIL import Image
from import_telegram_stickers.variables import *

@dataclass
class Sticker:
    pack_id: int
    sticker_id: int
    emojis: list[str]

    @staticmethod
    def from_json(json: dict[str, any]) -> 'Sticker':
        return Sticker(
            pack_id=json['pack_id'],
            sticker_id=json['sticker_id'],
            emojis=json['emojis'],
        )

@dataclass
class StickerPack:
    name: str
    stickers: list[Sticker]

    @staticmethod
    def from_json(json: dict[str, any]) -> 'StickerPack':
        return StickerPack(
            name=json['title'],
            stickers=[Sticker.from_json(sticker) for sticker in json['set']]
        )

@dataclass
class TelegramFile:
    file_id: str
    file_unique_id: str

    @staticmethod
    def create_telegram_file(file_id: str, file_unique_id: str) -> 'TelegramFile':
        return TelegramFile(
            file_id=file_id,
            file_unique_id=file_unique_id,
        )

def load_sticker_pack(filename: str) -> StickerPack:
    with io.open(filename, encoding='utf-8-sig') as file:
        json_data = json.load(file)

        return StickerPack.from_json(json_data)

def download_sticker_image(sticker_id: int) -> bytes:
    url = f'https://stickershop.line-scdn.net/stickershop/v1/sticker/{sticker_id}/iPhone/sticker@2x.png'
    response = requests.get(url)
    response.raise_for_status()

    assert response.headers['Content-Type'] == 'image/png'
    
    img_bytesio = io.BytesIO(response.content)
    img = Image.open(img_bytesio, mode='r')
    old_width, old_height = img.size
    new_width, new_height = None, None
    
    if old_width > old_height:
        new_width = 512
        ratio = new_width / old_width
        new_height = int(old_height * ratio)
    else:
        new_height = 512
        ratio = new_height / old_height
        new_width = int(old_width * ratio)

    roi_img = img.resize((new_width, new_height), Image.ANTIALIAS)
    
    img_byte_arr = io.BytesIO()
    roi_img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr

def telegram_upload_sticker_file(sticker_id: int) -> TelegramFile:
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/uploadStickerFile'
    sticker_img = download_sticker_image(sticker_id)
    png_sticker = {'png_sticker': sticker_img}
    data = {'user_id': USER_ID}

    # response do módulo requests
    response = requests.post(url, data=data, files=png_sticker)    

    # o metodo .json converte o corpo da resposta em um dicionário
    json_data = response.json()
    print(json_data)

    response.raise_for_status()

    assert json_data['ok']

    file = TelegramFile.create_telegram_file(
        file_id=json_data['result']['file_id'], 
        file_unique_id=json_data['result']['file_unique_id']
    )

    return file

def telegram_create_new_sticker_set(name: str, title: str, sticker: Sticker) -> Tuple[str, str]:
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/createNewStickerSet'

    telegram_file = telegram_upload_sticker_file(sticker.sticker_id)
    data = {
        'user_id': USER_ID, 
        'name': name,
        'title': title,
        'png_sticker': telegram_file.file_id,
        'emojis': ''.join(sticker.emojis)
    }

    response = requests.post(url, data=data)
    print(response.text)
    response.raise_for_status()

    return name, response.text

def telegram_add_sticker_to_set(name: str, sticker: Sticker):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/addStickerToSet'

    telegram_file = telegram_upload_sticker_file(sticker.sticker_id)
    data = {
        'user_id': USER_ID,
        'name': name,
        'png_sticker': telegram_file.file_id,
        'emojis': ''.join(sticker.emojis),
    }

    response = requests.post(url, data=data)
    response.raise_for_status()

    return response.text

def telegram_create_sticker_pack(name: str, title: str, stickerpack: StickerPack) -> None:
    name = name + f'_by_{TELEGRAM_BOT_USERNAME}'
    first_sticker = stickerpack.stickers[0]
    telegram_create_new_sticker_set(name, title, first_sticker)

    for sticker in stickerpack.stickers[1:]:
        telegram_add_sticker_to_set(name, sticker)
    
def main():
    sticker_pack = load_sticker_pack('stickers.json')
    telegram_create_sticker_pack(STICKER_NAME, STICKER_TITLE, sticker_pack)

if __name__ == "__main__":
    main()
