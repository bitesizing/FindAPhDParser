# %% 
""" TO DO: 
- Work into getting the data viewable in a good format, e.g. using UI tools. 
"""

import PhDParser

# %% 
""" Run code and save recent PhDs as .json file. """
parser = PhDParser()
parser.genProjects(keywords="attention")
parser.saveRecentAsJson()

# %%

