# вписать в терминале или командной строке (если ещё не установлено)
# pip install requests

import requests
import json

client_id = input("Введите Ваш YOUR_CLIENT_ID (при регистрации приложения в Meta): ")
client_secret = input("Введите Ваш YOUR_CLIENT_ID (при регистрации приложения в Meta): ")
redirect_uri = input("Введите URL необходимого аккаунта YOUR_REDIRECT_URI: ")

auth_url = f"https://api.instagram.com/oauth/authorize?client_id={client_id}&amp;redirect_uri={redirect_uri}&amp;scope=user_profile,user_media&amp;response_type=code"

print(f"Перейдите по ссылке для авторизации: {auth_url}")
code = input("Введите полученный код: ")

token_url = "https://api.instagram.com/oauth/access_token"
data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "authorization_code",
    "redirect_uri": redirect_uri,
    "code": code
}
response = requests.post(token_url, data=data)
access_token = response.json()["access_token"]
print(f"Токен доступа: {access_token}")

###################################
# Получение информации с аккаунта #
###################################
user_info_url = f"https://graph.instagram.com/me?fields=id,username&amp;access_token={access_token}"
response = requests.get(user_info_url)
user_info = response.json()

print(json.dumps(user_info, indent=2))

###################################
# Получение списка последних фото #
###################################

media_url = f"https://graph.instagram.com/me/media?fields=id,media_type,media_url,thumbnail_url,permalink&amp;access_token={access_token}"
response = requests.get(media_url)
media = response.json()["data"]

for item in media:
    if item["media_type"] == "IMAGE":
        print(f"{item['permalink']} - {item['media_url']}")