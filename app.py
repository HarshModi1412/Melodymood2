from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy as sa
from datetime import datetime
import openai

openai.api_key = "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"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///2.db"
db = sa(app)

class IM(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    mood1 = db.Column(db.String(200), nullable=False)
    mood2 = db.Column(db.String(200), nullable=False)
    songs = db.Column(db.String(600), nullable=False, default='')
    dT = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.mood1}-{self.mood2}-{self.songs}"

with app.app_context():
    db.create_all()

@app.route('/')
def html():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/gs', methods=['GET','POST'])
def htmlgs():
    mood1 = ''  # Initialize the variables
    mood2 = ''
    songs=''
    if request.method == 'POST':
        #print("post")
        mood1 = request.form['mood1']
        mood2 = request.form['mood2']
        #print(mood1, mood2)
        #print(f"To solve {mood1} using {mood2}.")
        prompt =f"You are a person who can suggest songs based on person's mood so. Give 5 songs of exactly {mood1} and give 5 songs of {mood2}. And like Hindi songs only. and give songs name only in reponse"
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=4000)
        print(response.choices[0].text)
        songs = response.choices[0].text
        im = IM(mood1=mood1, mood2=mood2, songs=songs)
        db.session.add(im)
        db.session.commit()
    return render_template('gs.html', songs=songs)

@app.route('/show')
def history():
    allIM = IM.query.all()
    return render_template('history.html', allIM=allIM)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ExPlay')
def ExPlay():
    return render_template('ExPlay.html')

@app.route('/delete/<int:sno>')
def delete(sno):
    im = IM.query.filter_by(sno=sno).first()
    db.session.delete(im)
    db.session.commit()
    return redirect("/show")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
