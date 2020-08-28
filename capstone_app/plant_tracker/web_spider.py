from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest
from . import models

class WebSpider:
    def __init__(self):
        self.url = "https://www.houseplantsexpert.com/a-z-list-of-house-plants.html"
        # fend off site's defense against webscraping by modifying header involved in request to simulate that of a browser
        self.headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

        req = requests.get(self.url, self.headers)
        self.html = BeautifulSoup(req.content, 'html.parser')
        self.flag_to_execute = True

    def get_flag(self):
        return self.flag_to_execute

    def set_flag(self, boolean):
        self.flag_to_execute = boolean

    def get_names(self, raw_data):
        return [tag["data-name"] for tag in raw_data.find_all("a", {"data-name": True})]

    def get_images(self, raw_data):
        return [tag["src"] for tag in raw_data.find_all("img", {"class": "imagePlant"})]

    def get_other_data(self, raw_data):
        """
        this function needs to scrape each house_plant's characteristics in one scrape, and output all the arrays as a tuple
        :param raw_data: original html document containing the hyperlinks for each house plant
        :return: tuple containing arrays for scientific names, origins, max growths, poisonous for pets, and watering data
        """

        results = {"Origin": [], "Names:": [], "Max Growth (approx)": [], "Poisonous for pets:": [], "Light": [],
                   "Watering": []}

        for tag in raw_data.find_all("a", {"data-name": True}):
            req = requests.get(tag["href"], self.headers)
            plant_html = BeautifulSoup(req.content, "html.parser")
            tables = plant_html.find_all("table", {"class": "table"})[:2]
            for table in tables:
                children = table.findChildren("td")
                for i, t in enumerate(children):
                    if t.text[:-1] in results.keys():
                        results[t.text[:-1]].append(children[i + 1].text)

        return results["Names:"], results["Origin"], results["Max Growth (approx)"], results["Poisonous for pets:"], \
               results["Light"], results["Watering"]

    def scrape(self):
        """
        This function should be the only function called from an instance of this class. It returns a transposed
        matrix of the websites data using the other methods the instance possesses
        """
        scientific_names, origins, growth, poisonous, light, watering = self.get_other_data(self.html)

        data = {
            "plant_name": self.get_names(self.html),
            "image_url": self.get_images(self.html),
            "scientific_name": scientific_names,
            "origin": origins,
            "growth": growth,
            "poisonous": poisonous,
            "light": light,
            "watering": watering
        }

        return list(zip_longest(*data.values()))

#________________________________Calling code to add results via Django ORM______________________________________

#Called once
"""
def results_to_db():
    scraper = WebSpider()

    if scraper.get_flag() == True:
        matrix = scraper.scrape()

        for row in matrix:
            obj = models.Plants(plant_name = row[0], image_url = row[1], scientific_name = row[2], origin = row[3], growth_desc = row[4], poisonous_desc = row[5], light_desc = row[6], watering_desc = row[7])
            obj.save()

    scraper.set_flag(False)
"""