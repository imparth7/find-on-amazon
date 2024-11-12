# app.py
from flask import Flask, render_template, request
from scraper import scrape_amazon_by_name

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    product_name = request.form['product_name']
    
    # Retrieve products based on the entered name
    products = scrape_amazon_by_name(product_name)
    return render_template('result.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
