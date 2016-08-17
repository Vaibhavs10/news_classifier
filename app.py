import pandas as pd
from sklearn.externals import joblib
import string
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from flask import Flask, render_template, request
from model import InputForm


app = Flask(__name__)

def vect(text):
	stemmer = PorterStemmer()
	tokens = text.split()
	tokens_filtered = [w for w in tokens if not w in stopwords.words('english')]
	stems = [stemmer.stem(t) for t in tokens_filtered]
	stems_nopunct = [s for s in stems if re.match('^[a-zA-Z]+$', s) is not None]
	return (stems_nopunct)


def predict(text, tfidf, ch2):
	df = pd.Series([text])
	df = df.apply(text_process)
	to_predict = tfidf.transform(df)
	pred = ch2.transform(to_predict)
	prediction = clf.predict(pred)
	return prediction

def text_process(text):
	exclude = string.punctuation
	text = re.sub('<[^>]*>','', text)
	text = ''.join(character for character in text.lower() if character not in exclude)
	return text


tfidf = joblib.load('vector.pkl')
chi = joblib.load('chi2.pkl')
clf = joblib.load('classifier.pkl')


@app.route('/', methods=['GET','POST'])
def index():

	
	form = InputForm(request.form)
	if request.method == 'POST' and form.validate():
		text = ((form.a.data).lower().strip())
		answer = str(predict(text, tfidf, chi)[0])

	else:
		text = None
		answer = None
	
	return render_template('view.html', form=form, text=text, answer=answer)


if __name__=='__main__':	
	app.run(debug=True)