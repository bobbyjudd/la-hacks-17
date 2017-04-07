import serial
import socket
from flask import Flask
from flask import render_template
from flask import abort

# Foot measurement server attributes
TCP_IP = '10.103.246.211'
TCP_PORT = 5005
BUFFER_SIZE = 256

app = Flask(__name__)

@app.route("/")
def hello(shoe_id=None, size=None):
	shoe_id = getData()
	size = None
	if(str(shoe_id) == "b'0'"):
		return render_template('index.html', shoe_id=shoe_id)
	else:
		return render_template('shoe-info.html', shoe_id=shoe_id, size=size)

@app.route('/measure')
def measure(shoe_id=None, size=None):
	shoe_id = getData()
	size = getSize()
	if(str(shoe_id) == "b'0'"):
		return render_template('index.html', shoe_id=shoe_id)
	else:
		return render_template('shoe-info.html', shoe_id=shoe_id, size=size)

def getData():
	with serial.Serial('COM6', 9600, timeout=2) as ser:
		data = ser.read()
		print("DATA: ", data)
		ser.reset_input_buffer()
		ser.close()
		return data


def getSize():
	print("Getting foot size")
	data = None
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		try:
			s.connect((TCP_IP, TCP_PORT))
			data = str(s.recv(BUFFER_SIZE))
		except Exception as e:
			print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
		finally:
			s.close()
			return data
		
def saveCurrentView(view):
	with open('./currentView.txt', 'r+') as f:
	    text = f.read()
	    text = re.sub('foobar', 'bar', text)
	    f.seek(0)
	    f.write(text)
	    f.truncate()

if __name__ == "__main__":
    app.run()