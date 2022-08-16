from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Kirti@02021997'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///InteractiveQuotes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sqliteDatabase = SQLAlchemy(app)


class InteractiveQuotes(sqliteDatabase.Model):
    interactiveQuotesId = sqliteDatabase.Column(sqliteDatabase.Integer, primary_key=True, nullable=False)
    interactiveQuotesQuotes = sqliteDatabase.Column(sqliteDatabase.Text, nullable=False)
    interactiveQuotesAuthor = sqliteDatabase.Column(sqliteDatabase.Text, nullable=False)

    def __repr__(self):
        return "Quotes Saved:" + "\n" + "interactiveQuotesId : " + str(
            self.interactiveQuotesId) + "\n" + "interactiveQuotesQuotes : " + self.interactiveQuotesQuotes + "\n" + "interactiveQuotesAuthor : " + \
               self.interactiveQuotesAuthor


@app.route('/interactiveQuoteHome')
def home():
    interactiveFavouriteQuotes = InteractiveQuotes.query.all()
    return render_template('home.html', interactiveFavouriteQuotes=interactiveFavouriteQuotes)


@app.route('/interactiveQuoteAbout')
def about():
    return render_template('about.html')


@app.route('/interactiveQuotes')
def quotes():
    return render_template('quotes.html')


@app.route('/insertinteractiveQuotes', methods=['GET', 'POST'])
def insertQuotes():
    if request.method == 'POST':
        author = request.form['author']
        quotes = request.form['quotes']
        sqliteDatabase.session.add(InteractiveQuotes(interactiveQuotesQuotes=quotes, interactiveQuotesAuthor=author))
        sqliteDatabase.session.commit()
        return redirect(url_for('home'))


@app.errorhandler(404)
def pageNotFoundError(error):
    return render_template('pageNotFound.html'), 404
