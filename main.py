from helper import *


class Modelisto:
    model_links = []
    countries = ["US", "Russia", "Italy", "Albania", "UK", "France", "Cyprus", "Greece", "Australia", "Sweden", "United-Arab-Emirates", "Canada", "Ukraine", "Norway", "Finland", "Romania", "Hungary", "Switzerland",
                 "Germany", "Kenya", "South-Africa", "Egypt", "India", "Nigeria", "Poland", "Mexico", "Spain", "Bulgaria", "Pakistan", "Czech-Republic", "Singapore", "Brazil", "Netherlands", "Turkey", "Iran", "Israel", "IL"]
    home_url = "https://modelisto.com"


    def get_page_links(self, url):
        soup = get_soup(url)
        divs = soup.find_all("div", {"class": "uxPerson"})
        links = [self.home_url + div.find("a")["href"] for div in divs]
        return links

    def get_country_model_links(self, country_code):
        base_url = "https://modelisto.com/Ajax/X/VA/List/Persons/?ListName=Models/"
        page_no = 1
        while True:
            url = base_url + country_code + "&p=" + str(page_no)
            page_links = self.get_page_links(url)
            if page_links == []:
                break
            if len(self.model_links)>0 and page_links[-1] == self.model_links[-1]:
                break
            self.model_links.extend(page_links)
            page_no += 1

    def store_model_links(self):
        write_json(self.model_links, "model_links.json")

    def get_all_model_links(self):
        for country_code in self.countries:
            print(country_code)
            self.get_country_model_links(country_code)
        self.store_model_links()

    def get_social_info(self, person_id):
        
        def get_username(soup, title):
            try:
                username = soup.find("button", {"title": title})["data-actionmethod"].split()[1]
            except:
                username = ""
            
            return username

        base_url = "https://modelisto.com/Ajax/X/VA/Person/Links/?PersonID="
        url = base_url + person_id
        soup = get_soup(url)

        insta_username = get_username(soup, "Instagram")
        video_username = get_username(soup, "Video")
        twitter_username = get_username(soup, "Twitter")

        return {
            "insta": insta_username,
            "video": video_username,
            "twitter": twitter_username
        }

    def get_photos(self, person_id):
        
        def get_page_photos(url):
            soup = get_soup(url)
            figures = soup.find_all("figure")
            imgs = []
            for figure in figures:
                imgs.append(figure.find("img")["src"].replace("@180", ""))
            return imgs

        page_no = 1
        base_url = f"https://modelisto.com/Ajax/X/VA/Person/Photos/?PersonID={person_id}&p="
        photos = []

        while True:
            url = base_url + str(page_no)
            page_photos = get_page_photos(url)
            if page_photos == []:
                break
            if len(photos)>0 and page_photos[-1] == photos[-1]:
                break
            photos.extend(page_photos)
        return photos
    
    def remove_url(self, url):
        links = get_json("model_links.json")
        links.remove(url)
        write_json(links, "model_links.json")

    def get_model_info(self, url):

        def get_stats(soup):
            spans = soup.find_all("span", {"class": "statsItem gridcell"})
            stats = {
                "Height": "",
                "Born": "",
                "Bust": "",
                "Hips": "",
                "Waist": "",
                "Weight": "",
                "Hair": "",
                "Eyes": ""
            }
            for span in spans:
                stat = span.text.split(":")[0].split(";")[0]
                value = span.text.split(":")[-1].split(";")[-1].split("/")[-1].strip()
                if stat in stats.keys():
                    stats[stat] = value
            return stats

        data = {}
        soup = get_soup(url)
        try:
            person_id = soup.find("div", {"id": "VAPersonLinks"})["data-qs"].split("=")[1]
        except TypeError:
            append_json({url:""}, "error.json")
            print("PersonID not found")
            return
        social_info = self.get_social_info(person_id)
        if social_info["insta"] == "":
            self.remove_url(url)
            return
        data.update(social_info)
        data["refer_url"] = url
        
        name = soup.find("meta", {"property": "og:title"})["content"].split()
        data["first_name"] = name[0]
        data["last_name"] = " ".join(name[1:])
        data["post_title"] = " ".join(name)

        try:
            data["website"] = soup.find("img", {"class": "Link"})["alt"]
        except TypeError:
            data["website"] = ""
        try:
            data["description"] = soup.find("section", {"class": "note"}).find("p").text.strip()
        except AttributeError:
            data["description"] = ""

        data["nationality"] = soup.find("meta", {"name": "geo.country"})["content"]
        
        stats = get_stats(soup)
        data.update(stats)
        photos = self.get_photos(person_id)
        data["pics"] = photos

        data["email"] = ""
        data["phone"] = ""
        append_json({social_info["insta"]:data}, "data.json")

    def get_all_model_info(self):
        links = get_json("model_links.json")
        done = set([value['refer_url'] for value in get_json("data.json").values()])
        error = get_json("error.json")
        for link in links:
            if link in done or link in error.keys():
                continue
            print(link)
            self.get_model_info(link)

class Modelsheight:
    model_links = []
    home_url = "http://www.modelsheight.com"
    countries = ["albanian","american","angolan","argentine","armenian","australian","austrian","belarusian","belgian","brazilian","british","bulgarian","canadian","chilean","chinese","colombian","costa rican","croatian","cuban","czech","danish","denmark","dominican","dutch","ethiopian","filipino","finland","french","georgian","german","greek","hungarian","indian","indonesian","iranian","irish","israeli","italian","japanese","kenyan","korean","kuwaiti","latvian","lebanese","lithuanian","luxembourger","macedonian","malaysian","mexican","moldovan","nepali","netherlands","new zealand","nicaraguan","norwegian","palestinian","paraguay","peruvian","philippin","polish","portuguese","puerto-rican","romanian","russian","serbian","slovakian","south africa","south korean","spanish","sudan","swedish","swiss","taiwanese","tanzanian","thailand","turkish","ukrainian","venezuelan","welsh"]

    def get_page_links(self, url):
        soup = get_soup(url)
        if soup.find("div", {"class": "error-404"}) != None:
            return []
        divs = soup.find_all("h2", {"class": "entry-title"})
        links = [div.find("a")['href'] for div in divs]
        return links
    
    def get_country_model_links(self, country_code):
        base_url = "http://www.modelsheight.com/category/"
        page_no = 1
        while True:
            url = base_url + country_code + "/page/" + str(page_no)
            print(url)
            page_links = self.get_page_links(url)
            if page_links == []:
                break
            self.model_links.extend(page_links)
            page_no += 1
    
    def store_model_links(self):
        write_json(self.model_links, "modelsheight_links.json")

    def get_all_model_links(self):
        for country_code in self.countries:
            print(country_code)
            self.get_country_model_links(country_code)
        self.store_model_links()

    def remove_url(self, url):
        links = get_json("modelsheight_links.json")
        links.remove(url)
        write_json(links, "modelsheight_links.json")

    def get_model_info(self, url):
        soup = get_soup(url)
        paras = soup.find_all("p")

        data = {
            "insta": "",
            "tiktok": "",
            "twitter": "",
            "first_name": "",
            "last_name": "",
            "post_title": "",
            "description": "",
            "nationality":"",
            "Height": "",
            "Born": "",
            "Bust": "",
            "Hips": "",
            "Waist": "",
            "Weight": "",
            "Hair": "",
            "Eyes": "",
            "pics": [],
            "website": "",
            "email": "",
            "phone": "",
            "refer_url": url
        }
        key_map = {
            "Instagram": "insta",
            "TikTok": "tiktok",
            "Date of Birth": "Born",
            "Nationality": "nationality",
            "Twitter": "twitter"
        }

        def get_stats(para):
            for line in para:
                stat = line.split(":")[0]
                value = line.split(":")[-1].replace("@", "").split(";")[-1].strip()
                if stat in key_map:
                    stat = key_map[stat]
                if stat in data.keys():
                    data[stat] = value

        def get_description(para):
            data["description"] = para[1]

        def get_photos(soup):
            imgs = [img["data-src"] for img in soup.find_all("img", {"class": "lazy-hidden", "border":"0"})]
            return imgs

        for para in paras:
            para_list = para.get_text(strip=True, separator='\n').splitlines()
            for line in para_list:
                if "Instagram" in line:
                    get_stats(para_list)
                if "Profile" in line:
                    get_description(para_list)
        if data["insta"] == "":
            self.remove_url(url)
            return
        
        name = soup.find("h1", {"class": "entry-title"}).text
        data["first_name"] = name.split(" ")[0]
        data["last_name"] = " ".join(name.split(" ")[1:])
        data["post_title"] = name

        data["pics"] = get_photos(soup)
        print(data["insta"])
        append_json({data["insta"]:data}, "data_modelheights.json")

        
    def get_all_model_info(self):
        links = get_json("modelsheight_links.json")
        done = set([value['refer_url'] for value in get_json("data_modelheights.json").values()])
        for link in links:
            if link in done:
                continue
            print(link)
            self.get_model_info(link)

class Babepedia:
    home_url = "https://babepedia.com"
    model_links = []

    def get_page_links(self, url):
        soup = get_soup(url)
        ol = soup.find("ol", {"class": "top100text"})
        divs = ol.find_all("a")
        links = [self.home_url + a["href"] for a in divs]
        return links
        
    def store_model_links(self):
        write_json(self.model_links, "babepedia_links.json")

    def get_all_model_links(self):
        base_url = "https://www.babepedia.com/instagramtop100followercounttext?page="
        page_no = 1
        for page_no in range(1,492):
            print(page_no)
            url = base_url + str(page_no)
            page_links = self.get_page_links(url)
            self.model_links.extend(page_links)
            self.store_model_links()
    
    def remove_url(self, url):
        links = get_json("babepedia_links.json")
        links.remove(url)
        write_json(links, "babepedia_links.json")    

    def get_model_info(self, url):
        soup = get_soup(url)

        data = {
            "insta": "",
            "tiktok": "",
            "twitter": "",
            "first_name": "",
            "last_name": "",
            "post_title": "",
            "description": "",
            "nationality":"",
            "Height": "",
            "Born": "",
            "Bust": "",
            "Hips": "",
            "Waist": "",
            "Weight": "",
            "Hair": "",
            "Eyes": "",
            "pics": [],
            "website": "",
            "email": "",
            "phone": "",
            "refer_url": url,
            "gender": "woman"
        }
        
        def get_social():
            div = soup.find("div", {"id": "socialicons"})
            for a in div.find_all("a"):
                alt = a.find("img")["alt"]
                if alt == "Official website":
                    data["website"] = a["href"]
                if alt == "Instagram account":
                    data["insta"] = a["href"].split("/")[-1].replace("@", "")
                if alt == "Twitter account":
                    data["twitter"] = a["href"].split("/")[-1].replace("@", "")
                if alt == "TikTok account":
                    data["tiktok"] = a["href"].split("/")[-1].replace("@", "")

        def get_stats():
            ul = soup.find("ul", {"id": "biolist"})
            for li in ul.find_all("li"):
                try:
                    stat = li.find("span", {"class": "label"}).text
                except AttributeError:
                    continue
                if stat == "Born:":
                    born = " ".join([a.text for a in li.find_all("a")])
                    data["Born"] = born
                if stat == "Birthplace":
                    data["nationality"] = li.find("a").text
                if stat == "Hair color:":
                    data["Hair"] = li.find("a").text
                if stat == "Eye color:":
                    data["Eyes"] = li.find("a").text
                if stat == "Height:":
                    data["Height"] = li.text.split("(")[-1].split(")")[0].replace("or ", "")
                if stat == "Weight:":
                    data["Weight"] = li.text.split("(")[-1].split(")")[0].replace("or ", "")
                if stat == "Measurements:":
                    try:
                        measurement = li.text.replace("Measurements:", "").strip().split("-")
                        data["Bust"] = measurement[0]
                        data["Waist"] = measurement[1]
                        data["Hips"] = measurement[2]
                    except:
                        pass
        
        def get_pics():
            imgs = []
            gallery = soup.find("div", {"class": "gallery useruploads"})
            for a in gallery.find_all("a", {"class": "img"}):
                imgs.append(self.home_url + a["href"])
            return imgs

        try:
            get_social()
        except:
            return

        if data["insta"] == "":
            return

        get_stats()
        name = soup.find("h1", {"id": "babename"}).text
        data["first_name"] = name.split(" ")[0]
        data["last_name"] = " ".join(name.split(" ")[1:])
        data["post_title"] = name 
        try:
            data["description"] = soup.find("div", {"class": "babebanner separate"}).find("p").text
        except:
            pass
        try:
            data["pics"] = get_pics()
        except:
            pass

        return data

    def get_all_model_info(self):
        links = get_json("babepedia_links.json")
        done = set([value['refer_url'] for value in get_json("data_babepedia.json").values()])
        i = 0
        new_data = {}
        for link in links[:25000]:
            if link in done:
                continue
            print(link)
            data = self.get_model_info(link)
            if data == None:
                self.remove_url(link)
                continue
            new_data[data["insta"]] = data
            i+=1
            if i%20 == 0:
                append_json(new_data, "data_babepedia.json")
                new_data = {}
                print(f"writing {i}")


if __name__ == "__main__":
    # model = Modelisto()
    # model.get_all_model_info()


    # model = Modelsheight()
    # model.get_model_info("http://www.modelsheight.com/desi-perkins/")

    model = Babepedia()
    model.get_all_model_info()
    # model.get_model_info("https://www.babepedia.com/babe/Stevie_Reyes")