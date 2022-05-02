from nturl2path import url2pathname
from flask import (Flask, render_template, request, flash)
import re
import spacy
import requests
from typing import Counter
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'dd hh'

@app.route('/', methods=("GET", "POST"))
def home():
    if request.method == "POST":

        try :
            global requested_url

            req = requests.get(requested_url)
            soup = BeautifulSoup(req.text, 'html.parser')
            contents = soup.find(class_ = "jobsearch-jobDescriptionText")


            contents = re.sub('<br/>','. ',str(contents))
            contents = re.sub('<[^<]+?>', ' ', str(contents))
            contents = re.sub('\&amp;', ' / ', str(contents))


            nlp = spacy.load("fr_core_news_md")
            doc = nlp(contents)
            nouns = [token.lemma_ for token in doc if token.pos_ == "NOUN"]
            nouns_freq = Counter(nouns)
            print(nouns_freq.most_common(10))

            return render_template("index.html")

        except Exception as e:
            flash(e, "danger")

    return render_template("index.html")

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
