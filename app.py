from flask import Flask, render_template, request

app = Flask(__name__)
DEBUGGING = True

@app.route('/', methods = ["GET", "POST"])
def home():
	return render_template('home.html')


app.run(debug=DEBUGGING)