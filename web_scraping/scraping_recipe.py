import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0"
}


class ScrapedRecipe:
    """ Recipes properties:
    Attributes:
        url: The url of the recipe on Jamie Oliver site.
    Methods:
        Ingredients: Recipe ingredients.
        Cooking time: What it says on the tin.
        Difficulty: Recipe difficulty.
        Serves: How many people the recipe serves.
    """

    def __init__(self, url):
        self.url = url
        self.soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')

    def getRecipeName(self):
        try:
            return self.soup.find('h1').text.strip()
        except (Exception,):
            return np.nan

    def getServes(self):
        try:
            return self.soup.find('div', {'class': 'recipe-detail serves'}).text.split(' ', 1)[1]
        except (Exception,):
            return np.nan

    def getCookingTime(self):
        try:
            return self.soup.find('div', {'class': 'recipe-detail time'}).text.split('In')[1]
        except (Exception,):
            return np.nan

    def getDifficulty(self):
        try:
            return \
                self.soup.find('div', {'class': 'col-md-12 recipe-details-col remove-left-col-padding-md'}).text.split(
                    'Difficulty')[1]
        except (Exception,):
            return np.nan

    def getIngredients(self):
        try:
            ingredients = []
            for li in self.soup.select('.ingred-list li'):
                ingredient = ' '.join(li.text.split())
                ingredients.append(ingredient)
            return ingredients
        except (Exception,):
            return np.nan
