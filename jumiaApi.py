from bs4 import BeautifulSoup
import requests
from flask import Flask,jsonify,render_template,request

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')



@app.route('/findings',methods=['GET','POST'])
def fetcher():
    subSec = request.form['item']
    url = (f"https://www.jumia.co.ke/catalog/?q={subSec}&sort=lowest-price&shipped_from=country_local&page=1")
    site = requests.get(url)
    soup = BeautifulSoup(site.text,'html.parser')
    products = soup.find_all(class_='core')
    gathered = []

    for prod in products:
        itemName = prod.find(class_='name')
        itemPrice = prod.find(class_='prc')
        itemImage = prod.find(class_='img')
        itemLink = prod['href']

        fillName = itemName.get_text()
        fillPrice = itemPrice.get_text()
        fillLink = (f"https://www.jumia.co.ke{itemLink}")
        fillImage = itemImage['data-src']
        

        gatheredItems = {
            "Name": fillName,
            "Price": fillPrice,
            "Link" : fillLink,
            'Image': fillImage
        }
        
        gathered.append(gatheredItems)

    return render_template('findings.html', results=gathered ,searchTerm=subSec)

if __name__ == '__main__':
    app.run(port='5050')