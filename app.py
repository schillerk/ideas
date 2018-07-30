from flask import Flask, jsonify, render_template
from flask_cors import CORS

import sqlite3
import requests
import csv
import pandas as pd
import ast

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/submit/<string:idea>')
def submit_idea(idea):
	print idea
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()

	insert_query = 'INSERT INTO ideas VALUES (?)'
	cursor.execute(insert_query, (idea,))

	connection.commit()
	connection.close()
	return ''

@app.route('/getdata')
def getdata():
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()

	out = []
	select_query = 'SELECT * FROM ideas'
	for row in cursor.execute(select_query):
		out.append(row)

	connection.commit()
	connection.close()
	return jsonify(out)

@app.route('/textbeltdemo')
def textbelt():
	requests.post('https://textbelt.com/text', {
	  'phone': 'PHONE NUMBER GOES HERE',
	  'message': 'Hello World! Twilio sucks.',
	  'key': 'TEXTBELT KEY GOES HERE',
	})
	return ''
