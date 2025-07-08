from flask import Flask, render_template, request
from binance import Client
import logging

app = Flask(__name__)

# Your testnet API keys
API_KEY = '17a1ea7c2041488577de56bc9b3f9c211c1535e392e0be9e15bdd1811da227df'
API_SECRET = 'ba3bebcb0c1db7ddf2b83cc90ae9dc012b0a17b23a60dfadd60dc87322e134d2'

client = Client(API_KEY, API_SECRET, testnet=True)

logging.basicConfig(filename='trade.log', level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trade', methods=['POST'])
def trade():
    symbol = request.form['symbol'].upper()
    order_type = request.form['order_type']
    side = request.form['side']
    quantity = request.form['quantity']
    price = request.form.get('price', '')

    try:
        if order_type == 'MARKET':
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
        elif order_type == 'LIMIT':
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'
            )
        else:
            return render_template("index.html", response="Unsupported order type.")

        logging.info(f"Order placed: {order}")
        return render_template("index.html", response=order)
    except Exception as e:
        logging.error(f"Error placing order: {str(e)}")
        return render_template("index.html", response=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7860)
