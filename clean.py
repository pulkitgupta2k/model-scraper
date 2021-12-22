import json

def utf_encode(file):
    with open(file, "r", encoding='utf8') as f:
            data = json.load(f)
    with open(file, "w", encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

def conv_date(date):
    month_key = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    date = date.split(" ")
    day = date[0][:-2]
    if len(day) < 2:
        day = "0"+day
    month = month_key[date[2]]
    new_date = f"{month}/{day}/{date[3]}"
    return new_date

def conv_date_heights(date):
    month_key = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    date = date.split(" ")
    if len(date) != 3:
        print(date)
        return ""
    day = date[1][:-1]
    if len(day) < 2:
        day = "0"+day
    try:
        month = month_key[date[0]]
    except:
        print(date)
        return ""
    new_date = f"{month}/{day}/{date[2]}"
    return new_date

def change_date():
    # with open("data_babepedia.json") as f:
    #     data = json.load(f)
    # for key, value in data.items():
    #     if value["Born"]:
    #         data[key]["Born"] = conv_date(value["Born"])
    # with open("data_babepedia.json", "w") as f:
    #     json.dump(data, f)
    with open("data_modelheights.json") as f:
        data = json.load(f)
    for key, value in data.items():
        if value["Born"]:
            data[key]["Born"] = conv_date_heights(value["Born"])
    with open("data_modelheights.json", "w") as f:
        json.dump(data, f)

def flatten(t):
    l = []
    for ele in t:
        if type(ele) == str:
            l.append(ele)
        if type(ele) == list:
            l.extend(ele)
    return l

def merge():
    with open("data_modelisto.json") as f:
        data_modelisto = json.load(f)
    with open("data_modelheights.json") as f:
        data_modelheights = json.load(f)
    with open("data_babepedia.json") as f:
        data_babepedia = json.load(f)
    data = {}

    for key, item in data_babepedia.items():
        data[key] = item
        if key in data_modelisto.keys():
            for k,v in item.items():
                if v == "":
                    data[key][k] = data_modelisto[key][k]
            data[key]["pics"].append(data_modelisto[key]["pics"])
        if key in data_modelheights.keys():
            for k,v in item.items():
                if v == "":
                    data[key][k] = data_modelheights[key][k]
            data[key]["pics"].append(data_modelheights[key]["pics"])
    
    for key, item in data_modelheights.items():
        if key in data.keys():
            continue
        data[key] = item
        if key in data_modelisto.keys():
            for k,v in item.items():
                if v == "":
                    data[key][k] = data_modelisto[key][k]
            data[key]["pics"].append(data_modelisto[key]["pics"])
    
    for key, item in data_modelisto.items():
        if key in data.keys():
            continue
        data[key] = item
    with open("data.json", "w") as f:
        json.dump(data, f)
    



def merge_babepedia():
    with open("data_babepedia.json") as f:
        data = json.load(f)
    with open("data_babepedia_1.json") as f:
        data_babepedia_1 = json.load(f)
    data.update(data_babepedia_1)
    with open("data_babepedia.json", "w") as f:
        json.dump(data, f)

def modelisto_clean():
    with open("data_modelisto.json") as f:
        data = json.load(f)
    for key, value in data.items():
        data[key]["tiktok"] = ""
        data[key].pop("video")
    with open("data_modelisto.json", "w") as f:
        json.dump(data, f)


def data_clean():
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)
    for key, value in data.items():
        data[key]["pics"] = flatten(value["pics"])
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

# print(conv_date_heights("April 1, 1993"))
# change_date()
# merge()
# modelisto_clean()
# utf_encode("data.json")
# print(flatten(["sd" ]))
data_clean()