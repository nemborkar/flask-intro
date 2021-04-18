from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# when you run a script/module, __name__ variable is __main__ (therefore allowing you a main() function block)
# when you import a script/module to run in another script/module, __name__ variable in the imported script/module is module_name.py (and not "__main__")

# essentially importing only functions but not the main() function block

# this means the app variable is "Flask ready" IN THIS SCRIPT and if it is ever imported, the app variable will always be Flask ready 
app = Flask(__name__)

# tells our app where our database is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# initialise database instance by passing the app through the method
db = SQLAlchemy(app)

# create db model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # string that returns the id when a task is created
    def __repr__(self):
        return '<Task %r>' % self.id

# URL routing
@app.route('/', methods=['POST','GET']) 

# functions go here
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

#for deleting
@app.route('/delete/<int:id>')    
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

# for updating
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that task'

    else:
        return render_template('update.html', task=task)

# main to call everything from
if __name__ == '__main__':
    app.run(debug=True)