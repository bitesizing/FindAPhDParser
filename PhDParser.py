import lxml
import requests
import json
from bs4 import BeautifulSoup
import disciplines

class Parser():
    def __init__(self):
        self.disciplines = disciplines.disciplines

    def parseURL(self, url) -> BeautifulSoup:
        """ Returns 'soup' object from a html page using requests and BeautifulSoup. 
            url (str) : valid findaPhD url to parse
            RETURNS BeautifulSoup : BeautifulSoup object used to parse data
        """
        return BeautifulSoup(requests.get(url).text, 'lxml')

    def saveAsJson(self, contents:(list[dict]), file_path:str="json"):
        """ Saves list of dictionaries as .json file. 
            contents (list[dict]) : contents to save in .json file
            file_path (str) : path to save, including filename. can be relative. defaults to json + the lowest integer unused by an existing 'json' file
        """
        if file_path == "json": 
            i = 1
            while True:
                try: open(f"str{i}.json")
                except FileNotFoundError: break
                else: i+=1
            file_path = f"str{i}.json"
            
        with open(file_path, 'w') as json_file:
            json.dump(contents, json_file, indent=2)

class PhDParser(Parser):
    def __init__(self):
        """ Initialises class with new_projects """
        super().__init__()  # initialise parent class
        self.hashstrings = set()  # TODO find a way to save this to file and reimport...
        self.projects = []  # AGAIN, save and reimport
        self.recent_new_projects = []

    def genProjects(self, discipline:str="psychology", recent_only:bool=True, keywords:str="") -> list[dict]:
        """ Parent function. Generates a list of projects from input parameters. Returns and saves internally. 
            discipline (str) : discipline of study to search within. default is "psychology"
            recent_only (bool) : show only recent PhD opportunities. default is True
            keywords (str) : *comma separated* list of search terms. defaults to no terms
            RETURNS list[dict] : list of projects with all project info
        """
        url = self.genURL(discipline=discipline, recent_only=recent_only, keywords=keywords)
        all_soup = self.parseURL(url)
        self.recent_new_projects = self.parsePhdSoup(all_soup, self.hashstrings, self.projects)
        return self.recent_new_projects

    def saveRecentAsJson(self, file_path:str="recent.json"):
        """ Saves recent new projects as a .json file with given output path. 
            file_path (str) : path to save projects to. default is "recent.json" in current directory.
        """
        if self.recent_new_projects == []: raise Exception('No recent projects to save!')
        self.saveAsJson(self.recent_new_projects, file_path=file_path)

    def genURL(self, discipline:str="psychology", recent_only:bool=True, keywords:str="") -> str:
        """ Generates a valid findaPhD url using search keywords. 
            discipline (str) : discipline of study to search within. default is "psychology"
            recent_only (bool) : show only recent PhD opportunities. default is True
            keywords (str) : *comma separated* list of search terms. defaults to no terms
            RETURNS str : valid findaPhD url
        """
        if discipline not in self.disciplines: raise KeyError("not a valid subject!")

        url_parts = [f"https://www.findaphd.com/phds/{disciplines[discipline]}"]
        if recent_only: url_parts.append("Show=M")

        keywords_str = [item.strip() for item in keywords.split(',')]
        keywords_str = f"keywords={("+").join(keywords_str)}"
        url_parts.append(keywords_str)
        url = '&'.join(url_parts)
        return url
    

    def parsePhdSoup(self, soup:BeautifulSoup, hashstrings:set[str], projects:list[dict]):
        """ Returns list of new PhD projecst using BeautifulSoup data. 
            soup (BeautifulSoup) : BeautifulSoup data for a findaPhD search page
            hashstrings (set[str]) : set of previous PhD titles. separates new from old titles
            projects (list[dict]) : list of previous projects. currently unused
        """
        new_projects = []
        phd_containers = soup.find_all(class_="w-100 card shadow-sm p-4")

        # Extra data from each project title individually.
        for container in phd_containers:
            # Get information from title
            title_container = container.find(class_="h4 text-dark mx-0 mb-3")
            link = f"https://www.findaphd.com{title_container['href']}"  # generate link to page
            title = title_container.text  # generate title

            # Process hashstring
            if title in hashstrings: continue  # don't reprocess if already in set
            hashstrings.add(title)  # add to existing hashstrings

            # Get information about PhD country from the 'flag' section
            country = container.find(class_="country-flag img-responsive phd-result__dept-inst--country-icon").get("title")

            # Get university name
            university = container.find(class_="phd-result__dept-inst--title").text.replace('\n', '')
            
            # Get date of last update and deadline date
            date_updated = container.find(class_="apply py-2 small").get_text(strip=True)[8:]
            deadline = container.find(class_="hoverTitle subButton badge text-wrap badge-light card-badge p-2 m-1 font-weight-light").get_text(strip=True)

            # Get funding information
            funding = container.find_all(class_="hoverTitle subButton text-wrap badge badge-light card-badge p-2 m-1 font-weight-light")[1].get_text(strip=True)

            # Append to list and return
            new_projects.append({
                "title": title,
                "date_updated": date_updated,
                "deadline": deadline,
                "funding": funding,
                "link": link,
                "country": country,
                "university": university
            })
        return new_projects






