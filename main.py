"""Main"""
import bs4
import requests
import constants
import json

MAX_DEPTH = 1


class Webcrawler:
    def __init__(self):
        self.urls = []
        self.visited = {}
        self.current_depth = 1
        self.results = []

    @staticmethod
    def generate_urls():
        """Generate a list of seed URLs"""
        url_list = []
        for sport in constants.SPORTS:
            url = "https://www.google.com/search?q=" + sport + "+leagues"
            url_list.append(url)
        return url_list

    def add_google_links(self, response_soup):
        """Add links from Google query"""
        filtered_results = response_soup.find_all("h3")
        for result in enumerate(filtered_results):
            parent = result[1].find_parent()
            link = parent.get('href')
            if link:
                self.urls.append(link[7:])

    def scrape_data(self, response_soup):
        """Scrape data from the site"""
        data = {
            "title": response_soup.title.string
            if response_soup and response_soup.title
            else "No Title Found",
            "text": response_soup.get_text()
        }
        self.results.append(data)
        if self.current_depth < MAX_DEPTH:
            for link in soup.find_all('a'):
                self.urls.append(link.get('href'))
            self.current_depth += 1


if __name__ == '__main__':
    webcrawler = Webcrawler()
    webcrawler.urls = webcrawler.generate_urls()
    while len(webcrawler.urls) > 0:
        try:
            current_url = webcrawler.urls.pop()
            webcrawler.visited[current_url] = True
            request_result = requests.get(current_url)
            soup = bs4.BeautifulSoup(request_result.text, "html.parser")
            print(current_url)
            if "google.com" in current_url:
                webcrawler.add_google_links(response_soup=soup)
            else:
                webcrawler.scrape_data(response_soup=soup)
        except Exception as error:
            print(error)

    out_file = open("webcrawler_results.json", "w")

    json.dump(webcrawler.results, out_file, indent=4)

    out_file.close()
