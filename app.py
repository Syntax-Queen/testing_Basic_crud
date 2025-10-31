# Import 
from flask import Flask, render_template, redirect, request, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from model import MyTask

@app.route("/", methods=['POST', 'GET'])
def index():
    # add a task
    if request.method== "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'ERROR: {e}')
            return f"ERROR: {e}"

    # see all task
    else:
        task = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", task=task)


# delete item
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    
    except Exception as e:
        return f'An error  occurred while deleting: {e}'


# edit an item
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Error: {e}'
        
    else:
        return render_template('edit.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)