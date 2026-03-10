from flask import Flask, render_template, request
from tinydb import TinyDB

app = Flask(__name__)

@app.route('/') 
def  index():  
    return render_template('index.html')

    if request.headers.get('X-Forwarded-For'): 
	    ip = request.headers.get('X-Forwarded-For').split(',')[0] 
    else:
    	ip = request.remote_addr  
    print(ip)  # Za debugging return  f"Vaš IP je: {ip}"`
	
db = TinyDB('obiskovalci.json')
db.insert({'IP' : '192.168.0.1', 'drzava' : 'Slovenia'})    


	
app.run(debug = True)