from flask import Flask, render_template

site = Flask(__name__)


@site.route('/')
def index():
    return render_template('index.html')


@site.route('/checkout')
def checkout():
    return render_template('checkout.html')


if __name__ == "__main__":
    site.run(debug=True)
