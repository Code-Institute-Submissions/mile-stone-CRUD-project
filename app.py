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
    recipe_name.insert_one(request.form.to_dict())
    return redirect(url_for('index'))


# app ROUTE TO SEE THE RECIPE DETAILS

@app.route('/details/<recipe_id>')
def details(recipe_id):
    the_recipe = mongo.db.recipe_name.find_one({"_id": ObjectId(recipe_id)})
  

    return render_template("details.html", recipe=the_recipe)




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)



'''
if request.files:    
        recipe_photo = request.files['recipe_photo']
        mongo.send_file(recipe_photo.filename, recipe_photo)
        mongo.db.recipe_photo.insert({'recipe_photo': recipe_photo.filename})

'''

'''
@app.route('/see_details/<_id>', methods=["GET"])
def see_details(_id):
    recipe_name = mongo.db.recipe_name
    recipe_name.find({"_id": ObjectId(_id)}, {'recipe_name': request.get('recipe_name'),
                                              'recipe_serve': request.get('recipe_serve'),
                                              'recipe_category': request.get('recipe_category'),
                                              'recipe_time': request.get('recipe_time'),
                                              'recipe_photo': request.get('recipe_photo'),
                                              'ingredients': request.get('ingredients'),
                                              'directions': request.get('directions')
                                              
    })

'''
'''
@app.route('/see_details/<recipe_id>',methods=["POST"])
def see_details(recipe_id):
    recipe_name = mongo.db.recipe_name
    recipe_name.find({"_id": ObjectId(recipe_id)}, {'recipe_name': request.form.get('recipe_name'),
                                              'recipe_serve': request.form.get('recipe_serve'),
                                              'recipe_category': request.form.get('recipe_category'),
                                              'recipe_time': request.form.get('recipe_time'),
                                              'recipe_photo': request.form.get('recipe_photo'),
                                              'ingredients': request.form.get('ingredients'),
                                              'directions': request.form.get('directions')
                                              
    })

    return redirect(url_for('index'))

'''