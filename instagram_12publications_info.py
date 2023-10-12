# Получает информацию об аккаунте Instagram только по его логину, получает 12 последних публикаций и их описание

# вписать в терминале или командной строке (если ещё не установлено)
# pip install httpx jmespath

import json
import httpx

INDENTS = 4 # indents count in JSON and console

client = httpx.Client(
    headers={
        # this is internal ID of an instegram backend app. It doesn't change often.
        "x-ig-app-id": "936619743392459",
        # use browser-like features
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      "AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)

def scrape_user(username: str):
    """Scrape Instagram user's data"""
    result = client.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
    )
    data = json.loads(result.content)
    return data["data"]["user"]

def deep_dict_get(_dict, keys, default=None):
    """Get value from dict by list-keys"""
    for key in keys:
        if isinstance(_dict, dict):
            _dict = _dict.get(key, default)
        else:
            return default
    return _dict

def print_user_data(_dict, keys, description, default=None, indents=INDENTS):
    """Print description and value by key in dict"""
    user_data = deep_dict_get(_dict, keys, default=default)
    if user_data and user_data not in [False, True]:
        print(f"{' ' * indents}{description}: {user_data}")
    elif user_data in [False, True]:
        result = {False: 'Нет', True: 'Да'}[user_data]
        print(f"{' ' * indents}{description}: {result}")

user_name = input("Введите алиас необходимого аккаунта Instagram: ")

# Get JSON file from account and save info into file
scrape_data = scrape_user(user_name)
with open('data.txt', 'w', encoding='utf-8') as outfile:
    json.dump(scrape_data, outfile, ensure_ascii=False, indent=4)

# Print user info
print(f"Информация о пользователе {user_name}:")
print_user_data(scrape_data, ['id'], 'ID')
print_user_data(scrape_data, ['full_name'], 'Полное имя')
print_user_data(scrape_data, ['biography'], 'Биография')
print_user_data(scrape_data, ['external_url'], 'Дополнительная ссылка')
print_user_data(scrape_data, ['edge_followed_by', 'count'], 'Подписчиков')
print_user_data(scrape_data, ['edge_follow', 'count'], 'Подписок')
print_user_data(scrape_data, ['edge_owner_to_timeline_media', 'count'], 'Публикаций')
print_user_data(scrape_data, ['highlight_reel_count'], 'Закреплённых Reels')
print_user_data(scrape_data, ['is_business_account'], 'Является бизнес-акаунтом')
print_user_data(scrape_data, ['is_professional_account'], 'Является профессиональным акаунтом')
print_user_data(scrape_data, ['is_private'], 'Является приватным акаунтом')
print_user_data(scrape_data, ['is_verified'], 'Является подтверждённым акаунтом')
print_user_data(scrape_data, ['profile_pic_url_hd'], 'Фото профиля')

# All publications count
publications_count = deep_dict_get(scrape_data, ['edge_owner_to_timeline_media'])['count']
publications_count_len = len(str(publications_count))
if publications_count:
    print("\n👇 Последнии публикации по дате размещения:👇\n")
    for j, publication in enumerate(scrape_data['edge_owner_to_timeline_media']['edges']):
        print('', end=' ' * INDENTS)
        publication_index = str(j+1).rjust(publications_count_len)
        print(f"Публикация №{publication_index}: [https://www.instagram.com/p/{publication['node']['shortcode']}]:")

        # Text of publication
        if 'edge_media_to_caption' in publication['node']:
            if deep_dict_get(publication, ['node', 'edge_media_to_caption', 'edges']):
                print(f"{' ' * INDENTS*2}Текст публикации:")
                for text in publication['node']['edge_media_to_caption']['edges']:
                    print(f"{' ' * INDENTS*3}{repr(text['node']['text'])[1:-1]}")

        # URL-picture
        print(f"{' ' * INDENTS*2}Картинка публикации:")
        print(f"{' ' * INDENTS*3}{publication['node']['display_url']}")

        # Attachments in publication
        if 'edge_sidecar_to_children' in publication['node']:
            for i, publication_attachment in enumerate(publication['node']['edge_sidecar_to_children']['edges']):
                print('', end=' ' * INDENTS*2)
                publication_attachment_index = str(i+1).rjust(publications_count_len)
                print(f"Вложение №{publication_attachment_index}:"
                      f"[https://www.instagram.com/p/{publication['node']['shortcode']}/?img_index={i+1}]:")
                print(f"{' ' * INDENTS*3}{publication_attachment['node']['display_url']}")