import requests
from bs4 import BeautifulSoup
import json

from requests.api import head

def get_soup(link):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',}
    html = requests.get(link, headers=headers).content
    return BeautifulSoup(html, "html.parser")

def write_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f)

def get_json(file):
    with open(file) as f:
        data = json.load(f)
    return data

def append_json(new_data, file):
    with open(file) as f:
        data = json.load(f)
    data.update(new_data)
    with open(file, "w") as f:
        json.dump(data, f)