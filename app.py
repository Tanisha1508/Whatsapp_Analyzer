from flask import Flask, flash, request, redirect, render_template,Response, make_response
from werkzeug.utils import secure_filename
import mainanalyzer
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

global stats
stats=None
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# path = "uploads"
# file Upload
# UPLOAD_FOLDER = os.path.join(path, 'uploads')
UPLOAD_FOLDER = "uploads"
#if not os.path.isdir(UPLOAD_FOLDER):
    #os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt'])

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route("/msgsperday_chart")
# def msgsperday_chart():
#     return render_template('msgsperday_chart.html', url ='static//images//plot1.png')

# @app.route("/msgsperuser_chart")
# def msgsperuser_chart():
#     return render_template('msgsperuser_chart.html', url ='static//images//plot2.png')

# @app.route("/msgstime_chart")
# def msgstime_chart():
#     return render_template('time_msgs.html', url ='static//images//plot3.png')
        

@app.route('/')
def upload_form():
    return render_template('home.html')


@app.route('/', methods=["GET", "POST"])
def home():
    global stats
    if request.method == "GET":
        return render_template("home.html")
    else:
        # check if the post request has the file part
        if 'chat_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['chat_file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath="uploads" + "//" + filename
            stats = mainanalyzer.upload(filepath)
            if stats == None:
                return render_template("apology.html")
            else:
                
                return render_template("results.html", jsonfile=stats,img1="static//images//plot1.png",img2="static//images//plot2.png")
                
        else:
            flash('Allowed file type is txt')
            return redirect(request.url)

@app.route('/results',methods=["GET", "POST"])
def results():
    global stats
    print(stats)
    return render_template("results.html",jsonfile=stats)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/limitations')
def limitations():
    return render_template("limitations.html")


if __name__ == "__main__":
    app.run(debug=True)
