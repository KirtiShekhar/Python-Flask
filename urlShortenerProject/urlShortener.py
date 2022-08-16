import json
import os.path
from flask import Flask,render_template,request,redirect,url_for,flash,abort,session,jsonify

app = Flask(__name__)
app.secret_key = 'Kirti@02021997'

@app.route('/urlShortenerHome')
def home():
    return render_template('home.html',usersession=session.keys())

@app.route('/urlShortenerAbout')
def about():
    return render_template('about.html')

@app.route('/urlshort',methods=['GET','POST'])
def shortUrl():
    if request.method == 'POST':
        usedUrls = {}
        if os.path.exists('usedUrls.json'):
            with open('usedUrls.json') as usedUrl_file:
                usedUrls = json.load(usedUrl_file)
        if request.form['code'] in usedUrls.keys():
            flash('The short name has already been taken. Please use another one.')
            return redirect(url_for('home'))

        usedUrls[request.form['code']] = {'url':request.form['url']}
        with open('usedUrls.json',"w") as usedUrls_file:
            json.dump(usedUrls,usedUrls_file)
            session[request.form['code']] = True
        shortenURL = request.form['code']
        return render_template('urlshort.html',code = shortenURL)
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
def shortNamesUrls(code):
    if os.path.exists('usedUrls.json'):
        with open('usedUrls.json') as usedUrl_file:
            usedUrls = json.load(usedUrl_file)
            if code in usedUrls.keys():
                if 'url'in usedUrls[code].keys():
                    return redirect(usedUrls[code]['url'])
    return abort(404)

@app.errorhandler(404)
def pageNotFoundError(error):
    return render_template('pageNotFound.html'),404

@app.route('/shortNamesUrlAPI')
def sessionApiJson():
    return jsonify(list(session.keys()))