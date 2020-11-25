from flask import Flask, request, render_template  
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import uuid


app = Flask(__name__)   

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods =['GET', 'POST']) 
def submit_textarea(): 
	if request.method == "POST": 
		#content typed
		text = request.form.get("text")
		filename = str(uuid.uuid4())+'.txt'
		script_location = Path(__file__).absolute().parent
		file_location = script_location / 'files'/filename
		with open(file_location, 'w') as fp: 
			fp.writelines(text) 
		# k is the output from the learning algorithm
		k = 1
		return render_template('index.html', k = k)
		# return ('', 204)
	else:
		return ('', 204)

@app.route('/getfile', methods=['GET','POST'])
def getfile():
	try:
		if request.method == 'POST':
			file = request.files['myfile']
			filename = secure_filename(file.filename) 
			file.save(os.path.join("files",filename))
			script_location = Path(__file__).absolute().parent
			file_location = script_location / 'files'/filename
			with open(file_location, errors='ignore') as f:
				#content from uploaded file
				file_content = f.read() 
			# k is the output from the learning algorithm
			k = "ab"
			return render_template('index.html', k = k)
			# return ('', 204)


		else:
			result = request.args.get['myfile']
			return ('', 204)
	except:
		return ('', 204)
  
if __name__=='__main__': 
	
	app.run(debug=True) 