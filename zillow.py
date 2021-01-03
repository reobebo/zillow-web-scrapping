import requests
from bs4 import BeautifulSoup
import json
import time
import csv


class ZillowScrapper():
    results = []
    headers = {
        'authority': 'www.zillow.com',
        'method': 'GET',
        'path': '/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-87.93676890551758%2C%22east%22%3A-87.73592509448243%2C%22south%22%3A42.093954179305584%2C%22north%22%3A42.145649672382795%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A33178%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22isCondo%22%3A%7B%22value%22%3Afalse%7D%2C%22isMultiFamily%22%3A%7B%22value%22%3Afalse%7D%2C%22isManufactured%22%3A%7B%22value%22%3Afalse%7D%2C%22isLotLand%22%3A%7B%22value%22%3Afalse%7D%2C%22isTownhouse%22%3A%7B%22value%22%3Afalse%7D%2C%22isApartment%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22]}&requestId=3',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'abtest=3|DHh6iHOdzsABTWy1Mg; zguid=23|%24d3df345c-1463-4bd5-b814-3de13ee3046d; G_ENABLED_IDPS=google; JSESSIONID=A904DC6B24055FE02572046737CEB172; zgsession=1|08dbb5ef-f30c-4924-a927-e5aa533b7656; search=6|1604093628615%7Crect%3D42.17288106125459%252C-87.73592509448243%252C42.06668884360084%252C-87.93676890551758%26rid%3D33178%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26type%3Dhouse%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%0933178%09%09%09%09%09%09; AWSALB=A9iM/Ayuwf3p9/a5p1sSt5SWrzycwy4wpu314BpTC1EoyhPbdKVS10Yi8ZLFQyaDuVlUMCLd2VKq5lKgM44sOEgjxwQLAwp/L2AQY4s1lfhEaFvrWZeVmymBBww4; AWSALBCORS=A9iM/Ayuwf3p9/a5p1sSt5SWrzycwy4wpu314BpTC1EoyhPbdKVS10Yi8ZLFQyaDuVlUMCLd2VKq5lKgM44sOEgjxwQLAwp/L2AQY4s1lfhEaFvrWZeVmymBBww4',
        'referer': 'https://www.zillow.com/northbrook-il/houses/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-87.93676890551758%2C%22east%22%3A-87.73592509448243%2C%22south%22%3A42.093954179305584%2C%22north%22%3A42.145649672382795%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A33178%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    def fetch(self, url, params):

        response = requests.get(url, headers=self.headers, params=params)
        print(response.status_code)
        return response

    def run(self):
        url = 'https://www.zillow.com/northbrook-il'
        #url = 'https://www.zillow.com/northbrook-il/houses/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-87.95479335009766%2C%22east%22%3A-87.71790064990235%2C%22south%22%3A42.08605608186619%2C%22north%22%3A42.153540345934054%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A33178%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22abo%22%3A%7B%22value%22%3Atrue%7D%2C%22pnd%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'

        for page in range(1, 8):
            params = {
                'searchQueryState': '{"pagination": {"currentPage": %s}, "mapBounds": {"west": -87.95479335009766, "east": -87.71790064990235, "south": 42.08605608186619, "north": 42.153540345934054}, "regionSelection": [{"regionId": 33178, "regionType": 6}], "isMapVisible": true, "filterState": {"sortSelection": {"value": "globalrelevanceex"}, "isAllHomes": {"value": true}, "isCondo": {"value": false}, "isMultiFamily": {"value": false}, "isManufactured": {"value": false}, "isLotLand": {"value": false}, "isTownhouse": {"value": false}, "isApartment": {"value": false}, "isAcceptingBackupOffersSelected": {"value": true}, "isPendingListingsSelected": {"value": true}}, "isListVisible": true, "mapZoom": 12}' % page
            }
            print(params)
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv()

    def parse(self, reponse):
        content = BeautifulSoup(reponse, 'lxml')
        deck = content.find(
            'ul', {'class': 'photo-cards photo-cards_wow photo-cards_short'})
        for card in deck.contents:
            script = card.find('script', {'type': 'application/ld+json'})
            price = card.find('div', {'class': 'list-card-price'})

            if price and script:

                script_json = json.loads(script.contents[0])
                self.results.append({
                    'address': script_json['name'],
                    'square_feet': script_json['floorSize']['value'],
                    'url': script_json['url'],
                    'price': card.find('div', {'class': 'list-card-price'}).text,
                    'price_per_sq_ft': (int(card.find('div', {'class': 'list-card-price'}).text.replace('$', '').replace(',', '').replace('--', '0').replace('Est. ', ''))/int(script_json['floorSize']['value'].replace(',', '').replace('--', '0'))),
                    'status': card.find('div', {'class': 'list-card-type'}).text,
                    'number_of_beds': card.find('ul', {'class': 'list-card-details'}).text[0],
                    'number_of_bathrooms': card.find('ul', {'class': 'list-card-details'}).text[5]
                })

    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)


if __name__ == '__main__':
    scrapper = ZillowScrapper()
    scrapper.run()
