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
    return render_template("index.html", recipe_name=mongo.db.recipe_name.find(),
                                         recipe_photo=mongo.db.recipe_photo.find())

@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', recipe_name=mongo.db.recipe_name.find())
                                            # recipe_photo=mongo.db.recipe_photo.find())


# this route will insert all the SUPPLIERS input field into DB and return them in the CUSTOMER MANAGEMENT PAGE.
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipe_name = mongo.db.recipe_name
    recipe_name.insert_one(request.form.to_dict())
    return redirect(url_for('index'))

   

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