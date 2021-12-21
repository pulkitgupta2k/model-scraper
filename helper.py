import requests
from bs4 import BeautifulSoup
import json

def get_soup(link):
    html = requests.get(link).content
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
        json.dump(data, file)