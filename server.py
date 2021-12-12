# This example sets up an endpoint using the Flask framework.
# Watch this video to get started: https://youtu.be/7Ul1vfmsDck.

import os
import stripe

from flask import Flask, redirect, send_from_directory, render_template

app = Flask(__name__)

stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

@app.route('/')
def send_root():
    return send_from_directory('', 'index.html')

@app.route('/success.html', methods=['GET'])
def send_success():
  return send_from_directory('pages', 'success.html')

@app.route('/cancel.html')
def send_cancel():
  return send_from_directory('', 'cancel.html')

@app.errorhandler(404)
def page_not_found(e):
  return send_from_directory('', '404.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'T-shirt',
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

if __name__== '__main__':
    app.run(port=4242)