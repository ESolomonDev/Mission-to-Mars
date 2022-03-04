#import flask, render a template, redirect to url and create url
from flask import Flask, render_template, redirect, url_for
#import PyMongo
from flask_pymongo import PyMongo
#import previous scraping code
import scraping

app =Flask(__name__)
# Use flask_pymongo to set up mongo connection
#connect to mongo using a URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#route for home page
@app.route("/")
def index():
    #pyMongo to get the 'mars' collection which is created in scraping.py
   mars = mongo.db.mars.find_one()
   #return index.html and use mars collection in mongoDB
   return render_template("index.html", mars=mars)

#define the scraping route
@app.route("/scrape")
def scrape():
   #new caribale that points to mongo datase
   mars = mongo.db.mars
   #created a new variable to hold the newly scraped data
   mars_data = scraping.scrape_all()
   #update the database but not if an identical record exists
   # .update_one(query_parameter, {"$set": data}, options)
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   #add a redirect after successfully scraping the data
   return redirect('/', code=302)
#run falsk app
if __name__ == "__main__":
   app.run()