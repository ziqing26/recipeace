import pandas as pd
import time
import numpy as np
import random
from scraping_recipe import ScrapedRecipe

# Reads in the csv containing each recipes url
recipe_df = pd.read_csv("../input/recipe_urls.csv")
# The list of recipe attributes we want to scrape
attribs = ['getRecipeName', 'getServes', 'getCookingTime', 'getDifficulty', 'getIngredients']

# For each url (i) we add the attribute data to the i-th row
temp = pd.DataFrame(columns=attribs)
for i in range(0, len(recipe_df['recipe_urls'])):
    url = recipe_df['recipe_urls'][i]
    recipe_scraper = ScrapedRecipe(url)
    temp.loc[i] = [getattr(recipe_scraper, attrib)() for attrib in attribs]
    if i % 25 == 0:
        print(f'Step {i} completed')
    time.sleep(random.randint(5, 10))

# Put all the data into the same dataframe
temp['recipe_urls'] = recipe_df['recipe_urls']
columns = ['recipe_urls'] + attribs
temp = temp[columns]

Recipe_df = temp

Recipe_df.to_csv(r"../input/Recipe_full.csv", index=False)
