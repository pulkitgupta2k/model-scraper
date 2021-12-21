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
                username = soup.find("button", {"title": title})["data-actionmethod"].split()[-1]
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
        person_id = soup.find("div", {"id": "VAPersonLinks"})["data-qs"].split("=")[1]
        social_info = self.get_social_info(person_id)
        if social_info["insta"] == "":
            return
        data.update(social_info)
        data["refer_url"] = url
        
        name = soup.find("meta", {"property": "og:title"})["content"].split()
        data["first_name"] = name[0]
        data["last_name"] = " ".join(name[1:])
        data["post_title"] = " ".join(name)
        
        data["website"] = soup.find("img", {"class": "Link"})["alt"]
        data["description"] = soup.find("section", {"class": "note"}).find("p").text.strip()
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
        for link in links:
            print(link)
            self.get_model_info(link)

if __name__ == "__main__":
    model = Modelisto()
    model.get_all_model_info()
