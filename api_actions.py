from flask import Flask, jsonify, request
import recommender

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello():
    return """
     <html><body>
         <h1>Welcome to Recipeace.</h1>
     </body></html>
     """


@app.route('/recipe', methods=["GET"])
def recommend_recipe():
    ingredients = request.args.get('ingredients')
    recipe = recommender.RecSys(ingredients)

    response = {}
    count = 0
    for index, row in recipe.iterrows():
        response[count] = {
            'recipe': str(row['recipe']),
            'score': str(row['score']),
            'ingredients': str(row['ingredients']),
            'url': str(row['url'])
        }
        count += 1
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)