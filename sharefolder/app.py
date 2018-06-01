from flask import Flask, render_template, request, redirect, url_for, flash
import threading, socket
from filetransferutility import *
from werkzeug import secure_filename

app = Flask(__name__)

server = None
client = None
connected = False

@app.route('/', methods=['POST', 'GET'])
def createserver():
	# if connected:
	# 	redirect(url_for("sendfile"))
	if request.method == "POST" :
		user = request.form.get('user')
		password = request.form.get('password')
		try:			
			server = Server(user, password)
		except Exception as e:
			flash('Authentication Failed')
			return render_template('createserver.html')
		iThread = threading.Thread(target=server.startserver)
		iThread.daemon = True
		iThread.start()
		return redirect(url_for('searchserver'))

	return render_template('createserver.html')


@app.route('/searchserver', methods=['POST', 'GET'])
def searchserver():
	# if connected:
	# 	redirect(url_for("sendfile"))
	if request.method == "POST":
		return redirect(url_for('displayserver'))
	return render_template('searchserver.html')


@app.route('/displayserver', methods=['POST', 'GET'])
def displayserver():
	# if connected:
	# 	redirect(url_for("sendfile"))
	if request.method == "POST":
		user = request.form.get('username')
		password = request.form.get('password')
		hostname = request.form.get('ip')
		global client 
		client = Client(user, password, hostname)
		print(client)
		if client.status == "230 Login successful.":
			connected = True
			flash(client.status)
		else:
			flash("Wrong credentials")
			return redirect(url_for("searchserver")) 

		return redirect(url_for("sendfile"))

	ipfinder = IpFinder()
	ips, my_ip = ipfinder.get_all_host()
	
	return render_template("displayserver.html", **locals())


@app.route('/sendfile', methods=['POST', 'GET'])
def sendfile():
	if request.method == "POST":
		global client
		file=request.files.get('file')

		filename = secure_filename(file.filename)
		print(filename)
		result = client.connect(filename, file)

		print(filename)
		return render_template('sendfile.html')
	return render_template('sendfile.html')


@app.route('/closeserver', methods=['POST', 'GET'])
def closeserver():
	client.quit()
	connected = False
	return redirect(url_for("searchserver"))

if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run()