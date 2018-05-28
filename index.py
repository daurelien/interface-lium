from flask import Flask, render_template, request
import requests, os #Partie transcription
from xml.dom import minidom
import encodings
import urllib, json	#Partie traduction


app = Flask(__name__)
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/traduction/', methods=['GET','POST'])
def traduction():
	if(request.method == 'POST'):
		url = "http://195.221.215.195/translate?"
		params = {'q' : '', 'key' : 'x', 'target' : '', 'source' : ''}

		params['q'] = request.form['text']
		params['target'] = request.args.get('target')
		params['source'] = request.args.get('source')
		data = urllib.parse.urlencode(params)
		data = data.encode('utf-8')
		req = urllib.request.Request(url, data)
		response = urllib.request.urlopen(req)
		result = json.loads(response.read().decode())
		res = ""
		for r in result['data']['translations']:       
			res += r['translatedText']

		return render_template('traduction.html', translation=res)
	else:
		return render_template('traduction.html')

@app.route('/transcription/')
def transcription():
	if(request.args.get('lang')=="fr"):
		fname=os.path.realpath(request.args.get('audio'))
		headers = {
			'Authentication-Token': 'WyI2IiwiMjYxMDNlNGI1NGE0Zjg4MDM5OWFmMzQ2OWNjZDg0ZDkiXQ.DTpmVA._0g0_VGtt4Qw58bqPC8xppAKrZM',
		}

		files = {
			'file': ('bb.wav', open(fname, 'rb')),
			'content': (None, '{"start": true, "asr_model_name": "french.studio.fr_FR"}'),
		}

		response = requests.post('http://spk1.univ-lemans.fr:8000/api/v1.1/files', headers=headers, files=files)
		params = (
			('format', 'xml'),
		)

		response = requests.get('http://spk1.univ-lemans.fr:8000/api/v1.1/files/26/transcription', headers=headers, params=params)
		f = open('reco.xml','w',encoding='utf8')
		txt=response.text
		for ligne in txt:
			ligne=ligne.encode('utf-8').decode('utf-8')
			f.write(ligne)
		f.close()
	
		ch=""
		xmldoc = minidom.parse("reco.xml")
		itemlist = xmldoc.getElementsByTagName('word')
		for s in itemlist:
		   #print(s.attributes['value'].value)
			ch+=" "+s.attributes['value'].value
		
		return render_template('transcription.html',txt=ch)

	if(request.args.get('lang')!=""):
		return render_template('transcription.html')
	
if __name__ == "__main__":
    app.run()
# Config options - Make sure you created a 'config.py' file.
# To get one variable, tape app.config['MY_VARIABLE']

#app.config.from_object('config.py')
