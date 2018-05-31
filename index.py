# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
import requests
import time
import os
from xml.dom import minidom
import encodings

app = Flask(__name__)

# Partie renvoyant sur la page d'accueil
@app.route('/')
def index():
	return render_template('index.html')


#Partie retournant sur la page de traduction
#Si la page est vide, renvoie la page pour écrire du texte à traduire
#Sinon récupération du contenu du texte pour effectuer la traduction
@app.route('/traduction/')
def traduction():
	if(request.args.get('source')==None):
		return render_template('traduction.html')
	if(request.args.get('source')!=""):	#Récupération des données puis envoi de la requête à l'API
		data = request.args.get('text')
		tar = request.args.get('target')
		sou = request.args.get('source')
		params = (('q', data),('key', 'x'),('target', tar),('source', sou))
		response = requests.get('http://195.221.215.195/translate', params=params)
		rep=response.json() #Transformation des données sous format json pour affichage
		out=''
		for d in rep['data']['translations']:       
				Sout=d['translatedText']
		return render_template('traduction.html', t=out,txt=data,src=sou,target=tar)


#Partie retournant sur la page de transcription
#Si la méthode est GET alors renvoi simple de la page de transcription vide
#Sinon, récupération des données et envoi à l'API en vue d'obtenir une réponse
@app.route('/transcription/',methods=['POST','GET'])
def transcription():
	file=''
	lang=''
	fname=''
	ch=''
	if request.method == 'POST': #Effectuer la transcription : Enregistrement du fichier et chemin + langue transcription
		file=request.files['audio'] 
		file.save(file.filename)
		lang=request.form['lang']
		fname=file.filename
		headers = {
		'Authentication-Token': 'WyI2IiwiMjYxMDNlNGI1NGE0Zjg4MDM5OWFmMzQ2OWNjZDg0ZDkiXQ.DTpmVA._0g0_VGtt4Qw58bqPC8xppAKrZM',
		}
		
		#Vérification de la langue de transcription
		if(request.form['lang']=="fr"):
			files = {
				'file': ('audio.wav', open(fname, 'rb')),
				'content': (None, '{"start": true, "asr_model_name": "french.studio.fr_FR"}'),
			}
		if(request.form['lang']=="ang"):
			files = {
				'file': ('audio.wav', open(fname, 'rb')),
				'content': (None, '{"start": true, "asr_model_name": "english.studio"}'),
			}
		response = requests.post('http://spk1.univ-lemans.fr:8000/api/v1.1/files', headers=headers, files=files)
		res = response.json()
		idd = res['id']
		
		url = 'http://spk1.univ-lemans.fr:8000/api/v1.1/processes/'+str(idd)
		response = requests.get(url, headers=headers)
		res = response.json()
		progress = res['progress'] #Récupération du pourcentage de transcription via l'url
		while(True):
				if(progress==100):
					break
				#time.sleep(20)
				url = 'http://spk1.univ-lemans.fr:8000/api/v1.1/processes/'+str(idd)
				response = requests.get(url, headers=headers)
				res1 = response.json()
				progress = res1['progress']
		
		#Récupérer le résultat du décodage
		#Ecriture dans un fichier puis lecture pour affichage
		params = (
			('format', 'xml'),
		)
		url = 'http://spk1.univ-lemans.fr:8000/api/v1.1/files/'+str(idd)+'/transcription'
		response = requests.get(url, headers=headers, params=params)
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
		   # print(s.attributes['value'].value)
			ch+=" "+s.attributes['value'].value
		text_trancrit=ch
	#RECUPERATION ATTRIBUT HTML PAGE TRANSCRIPTION.HTML
	return render_template('transcription.html',txt=ch,lang=lang)
	
##Charger le démarrage du serveur et de la page avec python index.py
if __name__ == "__main__":
    app.run()
# Config options - Make sure you created a 'config.py' file.
# To get one variable, tape app.config['MY_VARIABLE']
#app.config.from_object('config.py')
