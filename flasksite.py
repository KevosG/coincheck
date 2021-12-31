from flask import Flask
import coincheck

app = Flask(__name__)

@app.route('/')
def index():
    pricechange = "CCC is UP by " + cccdaychangerounded + "% in the last 24 hours!"
    return pricechange

if __name__ == "__main__":
    app.run(debug=True)