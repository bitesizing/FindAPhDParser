import lxml
import requests
import json
from bs4 import BeautifulSoup

class PhDParser():
    def __init__(self):
        """ Initialises the class and also parses all the data straight away, using class functions. """
        self.hashstrings = set()  # TODO find a way to save this to file and reimport...
        self.projects = []  # AGAIN, save and reimport
        self.recent_new_projects = []
    
    def genProjects(self, subject:str="psychology", recent_only:bool=True, keywords:str=""):
        """ Parent function to generate list of projects with all info from a url. Returns and saves to class for exporting. """
        url = self.genURL(subject=subject, recent_only=recent_only, keywords=keywords)
        all_soup = self.parseURL(url)
        self.recent_new_projects = self.parsePhdSoup(all_soup, self.hashstrings, self.projects)
        return self.recent_new_projects
    
    def saveRecentAsJson(self, file_path:str="recent.json"):
        """ Saves recent new projects as a .json file with given output path. """
        if self.recent_new_projects == []: raise Exception('No recent projects to save!')
        with open(file_path, 'w') as json_file:
            json.dump(self.recent_new_projects, json_file, indent=2)

    def genURL(self, subject:str="psychology", recent_only:bool=True, keywords:str="") -> str:
        subjects_dict = {
            'psychology': "psychology/?10M7-0"
        }
        if subject not in subjects_dict: raise KeyError("not a valid subject!")

        url_parts = [f"https://www.findaphd.com/phds/{subjects_dict[subject]}"]
        if recent_only: url_parts.append("Show=M")

        keywords_str = [item.strip() for item in keywords.split(',')]
        keywords_str = f"keywords={("+").join(keywords_str)}"
        url_parts.append(keywords_str)
        url = '&'.join(url_parts)
        return url

    def parseURL(self, url) -> BeautifulSoup:
        """ Returns 'soup' object from a html page using requests and BeautifulSoup. """
        return BeautifulSoup(requests.get(url).text, 'lxml')

    def parsePhdSoup(self, soup, hashstrings:set, projects:list):
        """ Appends new projects inplace to list of projects using beautifulSoup data. """
        box_class = "w-100 card shadow-sm p-4"
        new_projects = []
        soup_projects = soup.find_all(class_=box_class)

        # Extra data from each project title individually.
        for soup_project in soup_projects:
            # Get information from title
            title_class = "h4 text-dark mx-0 mb-3"
            title = soup_project.find(class_=title_class)
            heading_text = title.text
            link = f"https://www.findaphd.com{title['href']}"

            # Process hashstring
            if heading_text in hashstrings: continue  # don't reprocess if already in set
            hashstrings.add(heading_text)

            # Get information from the 'flag' section
            country = soup_project.find(class_="country-flag img-responsive phd-result__dept-inst--country-icon").get("title")

            # Get information about the University
            university = soup_project.find(class_="phd-result__dept-inst--title").text.replace('\n', '')
            
            # Get information about date and deadline
            date = soup_project.find(class_="apply py-2 small").get_text(strip=True)[8:]
            deadline = soup_project.find(class_="hoverTitle subButton badge text-wrap badge-light card-badge p-2 m-1 font-weight-light").get_text(strip=True)

            # Get information about funding
            funding = soup_project.find_all(class_="hoverTitle subButton text-wrap badge badge-light card-badge p-2 m-1 font-weight-light")[1].get_text(strip=True)

            # Append to list and return
            new_projects.append({
                "text": heading_text,
                "date": date,
                "deadline": deadline,
                "funding": funding,
                "link": link,
                "country": country,
                "university": university
            })

        return new_projects

    def hashString(self, string=""):
        """ [DEPRECATED] Removes spaces and makes a string lower. You don't need to do this for it to be hashable, but it's fun. """
        return string.lower().replace(" ", "")[:10]







