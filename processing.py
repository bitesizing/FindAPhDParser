#%%
import json
from PhDParser import PhDParser
from discipline_dict import disciplines as discipline_dict

# %% 
""" Gather data about EVERY PhD, sorted by discipline. """
for discipline in discipline_dict.keys():
    if discipline == "": continue
    parser = PhDParser(discipline=discipline)
parser.saveAllAsJson()

# %%
""" Return funding information from a file of PhDs. """

def readJson(file_path) -> (json):
    """ Reads .json file and returns it as a variable. """
    with open(file_path, 'r') as file:
        return(json.load(file))    
every_phd = readJson('every_phd.json')

def saveAsJson(contents:(list|dict), file_path:str="json"):
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

funding_list = []
for subject in every_phd.values():
    for project in subject.values():
        funding_list.append(project['funding'])
saveAsJson(funding_list, 'funding.json')