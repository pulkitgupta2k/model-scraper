import requests
import json
import glob

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
                response = requests.get(url)
                with open(f"images/{key}{str(i)}.jpg", "wb") as f:
                    f.write(response.content)
            except:
                print(url)

get_images()