# This example sets up an endpoint using the Flask framework.
# Watch this video to get started: https://youtu.be/7Ul1vfmsDck.

import os
import stripe

from flask import Flask, redirect, send_from_directory, render_template, jsonify

app = Flask(__name__)

stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
connection_token = stripe.terminal.ConnectionToken.create()

@app.route('/', methods=['GET'])
def send_root():
  return send_from_directory('', 'index.html')

@app.route('/index.html', methods=['GET'])
def send_index():
  return send_from_directory('', 'index.html')

@app.route('/success.html', methods=['GET'])
def send_success():
  return send_from_directory('pages', 'success.html')

@app.route('/cancel.html', methods=['GET'])
def send_cancel():
  return send_from_directory('pages', 'cancel.html')

@app.errorhandler(404)
def page_not_found(e):
  return send_from_directory('pages', '404.html')

@app.route('/connection_token', methods=['POST'])
def token():
  token = connection_token
  return jsonify(secret=token.secret)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'Donation',
        },
        'unit_amount': 2000,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='http://localhost:4242/success.html',
    cancel_url='http://localhost:4242/cancel.html',
  )

  return redirect(session.url, code=303)

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__== '__main__':
    app.run(port=4242)