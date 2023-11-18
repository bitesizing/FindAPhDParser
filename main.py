# %% 
from PhDParser import PhDParser, DisciplineParser
import discipline_dict

# %%
""" Fill in variables manually """
discipline = "psychology"           # discipline (subject) to search within
recent_only = True                  # whether to only show recent projects
keywords = "development"              # keywords should be comma separated

save_as_json = True                 # whether to save as .json in this file
json_output_path = "recent.json"    # shouldn't need to change this


# %%
""" Find matching PhD projects and save to class """
disciplines = discipline_dict.disciplines
discipline = discipline.lower()
if discipline not in disciplines: raise Exception('invalid discipline chosen! See `disciplines.py` for current list of valid disciplines...')

parser = PhDParser(discipline=discipline, recent_only=recent_only, keywords=keywords)


# %%
""" Save as .json file """
if save_as_json: parser.saveCurrentAsJson(output_path=json_output_path)