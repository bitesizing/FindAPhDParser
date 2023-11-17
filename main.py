# %% 
from PhDParser import PhDParser, DisciplineParser
import disciplines

# %%
""" Fill in variables manually """
# Currently only works for psychology and no subject. Would need to manually get the string codes for other subjects to make it work.
discipline = "psychology"
recent_only = True                  # whether to only show recent projects
keywords = "attention"              # keywords should be comma separated

save_as_json = True                 # whether to save as .json in this file
json_output_path = "recent.json"    # shouldn't need to change this


# %%
""" Find matching PhD projects and save to class """
disciplines = disciplines.disciplines
if discipline not in disciplines: raise Exception('invalid discipline chosen! See `disciplines.py` for current list of valid disciplines...')

parser = PhDParser()
parser.genProjects(discipline=discipline, recent_only=recent_only, keywords=keywords)


# %%
""" Save as .json file """
if save_as_json: parser.saveRecentAsJson(output_path=json_output_path)

# %%
d = DisciplineParser()
print(d.scrapeDisciplines())