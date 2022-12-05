from flask import Flask,render_template

import re
import firebase_admin
from firebase_admin import credentials,db
cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, {
	 'databaseURL': 'https://affordable--housing-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


app = Flask(__name__, static_url_path="/static")

@app.route('/')
def index():
	ref = db.reference('/db')
	list = [i.replace('-',' ').capitalize() for i in ref.get().keys()]
	return render_template('index.html',list=list)

@app.route('/state/<state>/')
def city_list(state):
	ref = db.reference(f'/db/{state}')
	
	list = [i.replace('-',' ').capitalize() for i in ref.get().keys()]

	return render_template('state.html',list=list,state=state.replace('-',' ').capitalize())


@app.route('/city/<state>/<city>/')
def details(state,city):
	ref = db.reference('/db')
	body = ref.child(f'{state}/{city}').get()['body']
	alts_data = [i.replace('-',' ').capitalize() for i in ref.child(state).get().keys()]
	city = city.replace('-',' ').capitalize()		
	cur = alts_data.index(city)
	alts = alts_data[cur+1:]
	if len(alts) < 20:
		alts.extend(alts_data[:cur])
	state = state.replace('-',' ').capitalize()		

	return render_template('content.html',body=body,city=city,state=state,alts=alts[:20])
	
def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s

app.jinja_env.filters['slugify']=slugify


if __name__ == '__main__':
	app.run(debug=True)