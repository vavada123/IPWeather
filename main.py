from flask import Flask, render_template, request
from tinydb import TinyDB
import requests
import json

app = Flask(__name__)

db = TinyDB('obiskovalci.json')  

@app.route('/obiskovalci')
def prikazi_obiskovalce():
    with open('obiskovalci.json', 'r') as f:
        data = json.load(f)
    
    vsi_obiski = data.get("_default", {})
    
    return render_template('obiskovalci.html', obiskovalci=vsi_obiski)


@app.route('/') 
def  index():  
    if request.headers.get('X-Forwarded-For'): 
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr  
    print(ip)  # Za debugging return  f"Vaš IP je: {ip}"`


    url = f"https://freeipapi.com/api/json/{ip}"
    response = requests.get(url)
    podatki = response.json()

    lat = podatki.get('latitude')
    lon = podatki.get('longitude')

    urlweather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&current=temperature_2m&timezone=auto"
    responseweather = requests.get(urlweather)
    podatkiweather = responseweather.json()

    kraj = podatki.get('cityName')
    temperatura = podatkiweather.get('current', {}).get('temperature_2m')

    db.insert({'IP' : ip, 'drzava' : kraj, 'temperatura' : temperatura})  

    return render_template('index.html',ip=ip, kraj=kraj, temperatura=temperatura)



	
app.run(host='0.0.0.0', port=5000, debug=True)