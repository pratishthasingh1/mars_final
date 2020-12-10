from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)
   
@app.route("/scrape")
def scrape():
   print("your in the scrape function=================")
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   #print(mars_data)
   #mars.update({}, mars_data, upsert=True)
   mars.update({"one":1,"two":2}, {"testing":123,"moretesting":456}, upsert=True)
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()