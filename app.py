from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#set up app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    #create uniqe id for task numbers
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    #create datetime created for user 
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    #create function to return string when task is made
    def __repr__(self):
        return "<Task %r>" % self.id

#create route for input
@app.route('/', methods = ['POST', 'GET'])
def index():
    #if user presses "add task"
    if request.method == 'POST':
        # set = to user input
        task_content = request.form['content']
        if len(task_content) == 0:
            return redirect("/")
        new_task = Todo(content = task_content)
        # try to commit to datbase
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Failed"
    else:
       #order all taks by date created
        tasks = Todo.query.order_by(Todo.date_created).all()
        #return back to page
        return render_template('index.html', tasks = tasks)
#create new route for delete button
@app.route('/delete/<int:id>')
def delete(id):
    #get id or 404 error if not found
    task_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_delete)
        db.session.commit()
        #return to homepage
        return redirect("/")
    except:
        return "Not deleted"

#create new route for update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug = True)