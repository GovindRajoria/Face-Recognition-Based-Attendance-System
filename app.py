from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Event(db.Model):  
    SNo=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable= False)
    desc=db.Column(db.String(400),nullable= False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SNo} - {self.title}"

@app.route('/')
def hello_world():
    event=Event(title="add 1st event", desc="detail btao")
    db.session.add(event)
    db.session.commit()
    return render_template('come.html')
  

@app.route('/paging')
def bhai():
    return 'naya page bn gya h'


if __name__ == "__main__":
    app.run(debug=True,port=5000)


# run in env_app only as in that old versions of module are installed otherwise it wont work properly