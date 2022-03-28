import pandas as pd
import string
import ast
import re
import unidecode
from nltk.stem import WordNetLemmatizer
import config

def data_parser(ingreds):
    """
    This function takes in a list of ingredients and performs some preprocessing.
       Example:
       input = '['1 x 1.6kg whole duck', '2 heaped teaspoons Chinese five-spice powder', '1 clementine',
                 '6 fresh bay leaves', 'GRAVY', '', '1 bulb of garlic', '2 carrots', '2 red onions',
                 '3 tablespoons plain flour', '100 ml Marsala', '1 litre organic chicken stock']'

       output = ['duck', 'chinese five spice powder', 'clementine', 'fresh bay leaf', 'gravy', 'garlic',
                 'carrot', 'red onion', 'plain flour', 'marsala', 'organic chicken stock']
    """
    if isinstance(ingreds, list):
        ingredients = ingreds
    else:
        ingredients = ast.literal_eval(ingreds)
    # Remove punctuation.
    translator = str.maketrans('', '', string.punctuation)
    lemmatizer = WordNetLemmatizer()
    ingred_list = []
    for i in ingredients:
        i.translate(translator)
        # Split up with hyphens as well as spaces
        items = re.split(' |-', i)
        # Get rid of words containing non alphabet letters
        items = [word for word in items if word.isalpha()]
        # Turn everything to lowercase
        items = [word.lower() for word in items]
        # Remove accents
        items = [unidecode.unidecode(word) for word in
                 items]
        # Lemmatize words so we can compare words to measuring words
        items = [lemmatizer.lemmatize(word) for word in items]
        # Gets rid of measuring words/phrases, e.g. heaped teaspoon
        items = [word for word in items if word not in config.MEASURES]
        # Get rid of common easy words
        items = [word for word in items if word not in config.REMOVABLE_WORDS]
        if items:
            ingred_list.append(' '.join(items))
    ingred_list = " ".join(ingred_list)
    return ingred_list


if __name__ == "__main__":
    recipe_df = pd.read_csv(config.RECIPES_PATH)
    recipe_df['ingredients_parsed'] = recipe_df['ingredients'].apply(lambda x: data_parser(x))
    df = recipe_df[['recipe_name', 'ingredients_parsed', 'ingredients', 'recipe_urls']]
    df = recipe_df.dropna()

    m = df.recipe_name.str.endswith('Recipe - Allrecipes.com')
    df['recipe_name'].loc[m] = df.recipe_name.loc[m].str[:-23]
    df.to_csv(config.PARSED_PATH, index=False)
