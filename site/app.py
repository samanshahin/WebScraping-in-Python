from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import time
import threading

app = Flask(__name__)

@app.route('/index')
@app.route('/index/g_idx')
@app.route('/index/fara_idx')
@app.route('/index/custom_idx_one_name')
@app.route('/index/custom_idx_one_price')
@app.route('/index/nazer_msg')
@app.route('/index/m_news')
def index(title=None):
    return check_price()

def check_price():
    #you can repeat it every some seconds by one of threading or sleep :
    # threading.Timer(5.0, check_price).start()
    # while(True){ 
    #    check_price()
    #    sleep(5000)
    # }
    URL = 'http://www.tsetmc.com/Loader.aspx?ParTree=15'
    headers={"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    #press F12 in webpage and check the css,...
    #finding g_idx
    g_idx = soup.find(id="TseTab1Elm")
    g_idx = g_idx.find_all('td')
    g_idx = g_idx[3].get_text()
    #finding fara_idx
    fara_idx = soup.find(id="IfbTab1Elm")
    fara_idx = fara_idx.find_all('td')
    fara_idx = fara_idx[3].get_text()
    #finding custom_idx_one
    custom_idx_one = soup.find(id="TseTab1Elm")
    custom_idx_one = custom_idx_one.find_all('table')
    custom_idx_one = custom_idx_one[2]
    custom_idx_one = custom_idx_one.find_all('td')
    custom_idx_one_name = custom_idx_one[0].get_text()
    custom_idx_one_price = custom_idx_one[1].get_text()
    #finding nazer_msg
    nazer_msg = soup.find(id="TseTab1Elm")
    nazer_msg = nazer_msg.find_all('table')
    nazer_msg = nazer_msg[1]
    nazer_msg = nazer_msg.find_all('td')
    #getting data(news) from donya-e-eqtesad.com
    m_news = get_news_from_eq()

    return render_template('index.html', g_idx=g_idx, fara_idx=fara_idx, 
    custom_idx_one_name = custom_idx_one_name, custom_idx_one_price = custom_idx_one_price,
    nazer_msg = nazer_msg, m_news=m_news)

def get_news_from_eq():
    URL = 'https://www.mehrnews.com/service/Economy'
    headers={"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    m_news = soup.findAll("li", { "class" : "news" })
    return m_news


if __name__ == '__main__':
    app.run()