import os
from flask import Flask, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get('cook_book')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)    


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", recipe_name=mongo.db.recipe_name.find())
                                         

@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', recipe_name=mongo.db.recipe_name.find())
                                      

# this route will insert all the RECIPES input field into DB and return them in the INDEX.
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipe_name = mongo.db.recipe_name
    recipe = recipe_name.insert_one(request.form.to_dict())
    inserted_id = recipe.inserted_id
    recipe_name.update(
        {"_id": ObjectId(inserted_id)},
        {"$set": {"ingredients": request.form.get("ingredients").splitlines(),
                  "directions": request.form.get("directions").splitlines()}})
    return redirect(url_for('index'))


# app ROUTE TO SEE THE RECIPE DETAILS

@app.route('/details/<recipe_id>')
def details(recipe_id):
    the_recipe = mongo.db.recipe_name.find_one({"_id": ObjectId(recipe_id)})
    return render_template("details.html", recipe=the_recipe)



# APP ROUTE TO DELETE A RECIPE IN THE DB
@app.route('/delete/<recipe_id>')
def delete(recipe_id):
    mongo.db.recipe_name.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for('index'))


# APP ROUTE TO EDIT RECIPE DETAILS
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    edit_recipe = mongo.db.recipe_name.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=edit_recipe)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipe_name = mongo.db.recipe_name
    recipe_name.update({'_id': ObjectId(recipe_id)},
    {
        'recipe_name': request.form.get('recipe_name'),
        'recipe_serve': request.form.get('recipe_serve'),
        'recipe_category': request.form.get('recipe_category'),
        'recipe_time': request.form.get('recipe_time'),
        'recipe_photo': request.form.get('recipe_photo'),
        'ingredients': request.form.get('ingredients').splitlines(),
        'directions': request.form.get('directions').splitlines()
    })
    return redirect(url_for('index'))


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    recipe_name = mongo.db.recipe_name.find({'$text':{'$search': query}})
    return render_template('index.html', recipe_name=recipe_name, type=search)
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)



