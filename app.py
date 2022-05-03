from flask import (Flask, render_template, request, flash)
from bs4 import BeautifulSoup
import requests
import re
import spacy
from typing import Counter

app = Flask(__name__)
app.secret_key = 'dd hh'


@app.route('/', methods=("GET", "POST"), strict_slashes=False)
def home():
    if request.method == "POST":
        try :

            global req

            req = request.form.get("requested_url")

            html_content = requests.get(str(req))
            soup = BeautifulSoup(html_content.text, 'html.parser')
            contents = soup.find(class_ = "jobsearch-jobDescriptionText")

            contents = re.sub('<br/>','. ',str(contents))
            contents = re.sub('<[^<]+?>', ' ', str(contents))
            contents = re.sub('\&amp;', ' / ', str(contents))
            contents = re.sub('- ', '', str(contents))

            nlp = spacy.load("fr_core_news_md")
            doc = nlp(contents)
            nouns = [token.lemma_ for token in doc if token.pos_ == "NOUN"]
            nouns_freq = Counter(nouns).most_common(5)

            verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
            verbs_freq = Counter(verbs).most_common(5)

            n_labels = [row[0] for row in nouns_freq]
            n_values = [row[1] for row in nouns_freq]

            v_labels = [row[0] for row in verbs_freq]
            v_values = [row[1] for row in verbs_freq]

            return render_template("index.html", n_labels=n_labels, n_values=n_values, v_labels=v_labels, v_values=v_values)

        except Exception as e:
            flash(str(e), "danger")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
