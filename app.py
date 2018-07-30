from flask import Flask, jsonify, render_template
from flask_cors import CORS

import sqlite3
import requests
import csv
import pandas as pd
import ast

app = Flask(__name__)
CORS(app)

# connection = sqlite3.connect('data.db')
# cursor = connection.cursor()

# create_table = 'CREATE TABLE ideas (blob text)'
# cursor.execute(create_table)

# connection.commit()
# connection.close()

# field = 'Gender'
# field2 = 'Count'
# print sum(df.loc[(df['Race/Ethnicity'] == 'White') & (df['Gender'] == 'Male') & df['Count'] > 0, 'Count'])
# print df.loc[(df[field] == 'Male') & df[field2] > 0]
# print df.query('''Gender == 'Male' & RE == 'White' & Count > 0''')
# print df[df.Location == "USA" & df.Gender == "Male"]
# print df[df.Gender == "Male" & df.Location == "USA"]

# print str(int(sum(df.query(buildQuery(test_query))['Count'])))

def buildQuery(fields):
	print ' & '.join(['{} == \'{}\''.format(k, v) for k, v in fields.items()]) + ' & Count > 0'
	out = ''
	for k, v in fields.items():
		if v != 'All':
			out += '{} == \'{}\''.format(k, v) + ' & '
	print out + 'Count > 0'
	return out + 'Count > 0'

def run_query(fields):
	return df.query(buildQuery(fields))

def parseQuery(fields):
	results = run_query(fields)['Count']
	total = sum(results)
	return str(int(total))

@app.route('/')
def fun():
	return render_template('index.html')
	# return jsonify(data)

@app.route('/submit/<string:idea>')
def submit_idea(idea):
	print idea
	# print ast.literal_eval(idea)
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()

	insert_query = 'INSERT INTO ideas VALUES (?)'
	cursor.execute(insert_query, (idea,))

	connection.commit()
	connection.close()
	return ''

@app.route('/total')
def total():
	return str(int(sum(df.loc[(df['Count'] > 0), 'Count'])))

@app.route('/query/<string:q>')
def return_query_results(q):
	print q
	return parseQuery(ast.literal_eval(q))

@app.route('/getjsondata')
def getjson():
	return jsonify(data)

@app.route('/test')
def test():
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()

	test_company = (1, 'Zenysis')
	insert_query = 'INSERT INTO companies VALUES (?, ?)'
	cursor.execute(insert_query, test_company)

	connection.commit()
	connection.close()
	return 'hello worlddadsf'

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

@app.route('/callAPI')
def call():
	# make an api call
	# print 'testing call'
	requests.post('https://textbelt.com/text', {
	  'phone': '6503324607',
	  'message': 'Hello fuck twilio',
	  'key': TEXTBELT_KEY,
	})
	return ''