import requests
import json
import glob

from requests.api import head

current_images = set([x[7:-4] for x in glob.glob("images/*")])


def get_images():
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)

    for key, value in data.items():
        i=0
        for url in value["pics"]:
            try:
                i+=1
                if f"{key}{str(i)}" in current_images:
                    continue
                headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',}
                response = requests.get(url, headers=headers)
                with open(f"images/{key}{str(i)}.jpg", "wb") as f:
                    f.write(response.content)
            except:
                print(url)

get_images()