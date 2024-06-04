from flask import Flask, render_template, request, redirect, url_for
from twitter_scrapping import main as run_scraper
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client.twitter_trends
collection = db.trends

@app.route('/')
def index():
    # Retrieve data from MongoDB
    trending_data = collection.find(sort=[('date', -1)], projection={'_id': False})
    trending_data_list = list(trending_data)
    if trending_data_list:
        trend = trending_data_list[0]
    else:
        trend = {
            'nameoftrend1': 'No data',
            'nameoftrend2': 'No data',
            'nameoftrend3': 'No data',
            'nameoftrend4': 'No data',
            'nameoftrend5': 'No data',
            'date': 'N/A',
            'ip_address': 'N/A'
        }

    return render_template('index.html', trend=trend)

@app.route('/scrape', methods=['POST'])
def scrape():
    if request.method == 'POST':
        run_scraper()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
