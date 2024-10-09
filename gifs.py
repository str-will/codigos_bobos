import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Carregar as variáveis chave do arquivo .env

TENOR_API_KEY = os.getenv('tenor_api_key')

def obtem_gif(palavra_chave):
    url = f'https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s' % (palavra_chave, TENOR_API_KEY, TENOR_API_KEY, 1)
    response = requests.get(url) # fazendo a requisição

    if response.status_code == 200: # se a requisição foi bem sucedida
        data = response.json()
        if data['results']: # se houver gifs na resposta
            return data['results'][0]['media_formats']['gif']['url'] # retorna a URL do gif

    return None # caso não encontre gifs, retorna None