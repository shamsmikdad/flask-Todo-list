from flask import Flask, render_template , request, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
#add csrf
app.config['SECRET_KEY']= "this is my secret key"
#add database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///tasks.db'
#initilaize database
db=SQLAlchemy(app)
#create a Model
class Tasks(db.Model):
    id = db.Column(db.Integer , primary_key=True )
    task = db.Column(db.String(500), nullable=False)
    # dateAdded = db.Column(db.DateTime, default=datetime.utcnow)
    #create astring
    def __repr__(self):
        return '<task %r>' % self.task

# @app.route('/user/<name>')
# def user(name):
#     return "<h1>index.html {} </h1>".format(name)

class AddTask(FlaskForm):
    tasks = StringField("add new task", validators=[DataRequired()])
    submit = SubmitField("add task")

@app.route('/', methods=['GET','POST'])
def list():
    tasks = None
    form = AddTask()
    if form.validate_on_submit():
        task = Tasks(task=form.tasks.data)
        db.session.add(task)
        db.session.commit()
        task=form.tasks.data
        form.tasks.data=''
    our_tasks = Tasks.query.order_by(Tasks.id)
    return render_template("index.html", 
    tasks=tasks,
     form=form,
     our_tasks=our_tasks)

if __name__ == "__main__":
    app.run(debug=True)