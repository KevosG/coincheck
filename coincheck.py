from flask import Flask, render_template
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

CMC_KEY = os.getenv('CMC_KEY')

# universal param vars for using CMC api 
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': f'{CMC_KEY}'
}

# takes symbol as input and returns the first matching id from the cmc map
def getcryptoid(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'symbol': f'{symbol}'
    }
    map = requests.get(url, headers=headers, params=parameters)
    mapjson = map.json()
    id = mapjson['data'][0]['id']
    return id

# takes a symbol as input and returns the full quote result in json format
def getquote(symbol):
    id = getcryptoid(symbol)
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'id':f'{id}'
    }
    quote = requests.get(url, headers=headers, params=parameters)
    quotejson = quote.json()
    return quotejson

def getmcapwithid(id):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'id':f'{id}'
    }
    quote = requests.get(url, headers=headers, params=parameters)
    quotejson = quote.json()
    mcap = quotejson['data'][f'{id}']['quote']['USD']['fully_diluted_market_cap']
    return mcap

def getmcap(symbol):
    quote = getquote(symbol)
    mcap = quote['data'][f'{getcryptoid(symbol)}']['quote']['USD']['fully_diluted_market_cap']
    return mcap 

def getdaychange(symbol):
    quote = getquote(symbol)
    daychange = quote['data'][f'{getcryptoid(symbol)}']['quote']['USD']['percent_change_24h']
    daychangerounded = str(round(daychange, 2))
    return daychangerounded


#"${:,.2f}".format(thethingtomakecash)
# pull CCC day change and mcap
cccdaychange = getdaychange('CCC')
cccmcap = getmcap('CCC')

# pull MCC mcap specfically
mccmcap = getmcapwithid('16160')

if float(cccdaychange) > 0:
    daychangemsg = "CCC is UP by " + cccdaychange + "% in the last 24 hours!"
elif float(cccdaychange) < 0:
    daychangemsg = "CCC is DOWN by " + cccdaychange + "% in the last 24 hours!"

mcapmsg = "CCC Market Cap is currently: " + '${:,.2f}'.format(cccmcap)
mccmcapmsg = "MCC Market Cap is currently: " + '${:,.2f}'.format(mccmcap)
togomulti = str(round(mccmcap / cccmcap, 2))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", daychangemsg=daychangemsg, mcapmsg=mcapmsg, mccmcapmsg=mccmcapmsg, togomulti=togomulti)

if __name__ == "__main__":
    app.run(debug=True)
