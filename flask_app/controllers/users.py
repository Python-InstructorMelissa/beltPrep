from flask_app import app
from flask import Flask, render_template, session, redirect, flash, request
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/', methods=['POST'])
def register():
    isValid = User.validate(request.form)
    if not isValid:
        return redirect('/')
    newUser = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(newUser)
    if not id:
        flash("Somewhere you messup silly lady")
        return redirect('/')
    session['user_id'] = id
    flash('Hey you logged in')
    return redirect('/dashboard/')


@app.route('/login/', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data)
    if not user:
        flash("That email is not in our system")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("You got the wrong password")
        return redirect('/')
    session['user_id'] = user.id
    flash('Welcome back')
    return redirect('/dashboard/')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')