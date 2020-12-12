from flask import Flask ,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql+psycopg2://postgres:nainesh20@localhost/quotes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jswieqwiecefli:cb3c7eb28d43a9d93a7ec5dabf1f58b199cce58f69bd289594bba978dad81cf7@ec2-54-84-98-18.compute-1.amazonaws.com:5432/d8h77e319c66ik'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class Favquotes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(30))
    quote = db.Column(db.String(2000))
    email_id = db.Column(db.String(30))


@app.route('/')
def index():
    result = Favquotes.query.all()
    return render_template('index.html',result=result)

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

@app.route('/process', methods =['POST'])
def process():
    author = request.form['author']
    quote = request.form['quote']
    email_id = request.form['email_id']
    quotedata = Favquotes(author=author,quote=quote,email_id=email_id)
    db.session.add(quotedata)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    manager.run()
