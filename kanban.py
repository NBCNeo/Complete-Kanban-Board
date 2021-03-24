import os
from flask import Flask, redirect, render_template, g, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import logout_user
from flask_login import current_user, login_user, login_required
from models import app, db, User, Task

login = LoginManager()
login.init_app(app)
login.login_view = 'login'

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/login')

@login.user_loader
def user_load(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        
        if user is None:
            error = 'Check your username and password.'
            return render_template('login.html', error=error)
        login_user(user)

        return redirect("/kanban")

    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    return redirect('login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if len(request.form['password']) < 7:
            error = 'Passwords must be greater than 7 characters.'
            return render_template('register.html', error=error)

        if request.form['password'] != request.form['confirm_pass']:
            error = 'Ensure that the passwords match.'
            return render_template('register.html', error=error)

        joined_user = User(username=request.form['username'], password=request.form['password'])

        db.session.add(joined_user)
        db.session.commit()

        return redirect("/login")

    elif request.method == 'GET':
        return render_template('register.html')


@app.route("/update", methods=["POST"])
def update():
    try:
        new_status = request.form.get("new_status")
        name = request.form.get("name")
        task = Task.query.filter_by(title=name).first()
        task.status = new_status
        db.session.commit()

    except Exception as err:
        print(err)

    return redirect("/kanban")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    task = Task.query.filter_by(title=title).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/kanban")


@app.route('/kanban', methods=["GET", "POST"])
@login_required
def home():
    g.user = current_user
    tasks = None
    error = None
    if request.form:
        try:
            if request.form.get("title") in [task.title for task in Task.query.all()]:
                error = "Duplicate tasks."
            else:
                task = Task(id = 1, title=request.form.get("title"), status=request.form.get("status"), user_id = g.user.id)
                tasks = Task.query.all()

                db.session.add(task)
                db.session.commit()

        except Exception as err:
            print(err)

    tasks = Task.query.filter_by(user_id=g.user.id).all()
    todo = Task.query.filter_by(status='Todo',user_id=g.user.id).all()
    in_progress = Task.query.filter_by(status='In Progress',user_id=g.user.id).all()
    completed = Task.query.filter_by(status='Completed',user_id=g.user.id).all()
    return render_template("home.html", error=error, tasks=tasks, todo=todo, in_progress=in_progress, completed=completed, myuser=current_user)


if __name__ == "__main__":
    app.run(debug=False)
