from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrappy_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    #mars = mongo.db.mars.find_one()
    mars_data = scrappy_mars.scrape_all()
    return render_template("index.html", mars_info=mars_data)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrappy_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"


if __name__ == "__main__":
    app.run()