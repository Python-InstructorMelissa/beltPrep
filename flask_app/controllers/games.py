import imp
from flask_app import app
from flask import Flask, render_template, session, redirect, flash, request
from flask_app.models.game import Game
from flask_app.models.user import User


@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        flash("Dude log in already")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    theUser = User.getOne(data)
    theGames = Game.allEntries()
    # print("the games controler: ", theGames)
    return render_template('dashboard.html', user=theUser, games=theGames)

@app.route('/newGame/')
def newGame():
    if 'user_id' not in session:
        flash('please log in')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    theUser = User.getOne(data)
    return render_template('newGame.html', user=theUser)


@app.route('/createGame/', methods=['POST'])
def createGame():
    data = {
        'teamOne': request.form['teamOne'],
        'teamTwo': request.form['teamTwo'],
        'finalScore': request.form['finalScore'],
        'info': request.form['info'],
        'gameDate': request.form['gameDate'],
        'user_id': session['user_id']
    }
    Game.save(data)
    flash("Your games scores were saved")
    return redirect('/dashboard/')

@app.route('/<int:game_id>/view/')
def viewGame(game_id):
    if 'user_id' not in session:
        flash('please log in')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    gameData = {
        'id': game_id
    }
    theUser = User.getOne(data)
    theUsers = User.getAll()
    theGame = Game.getOne(gameData)
    return render_template('viewGame.html', user=theUser, users=theUsers, game=theGame)

@app.route('/<int:game_id>/edit/')
def editGame(game_id):
    if 'user_id' not in session:
        flash('please log in')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    gameData = {
        'id': game_id
    }
    theUser = User.getOne(data)
    theGame = Game.getOne(gameData)
    return render_template('editGame.html', user=theUser, game=theGame)

@app.route('/<int:game_id>/update/', methods=['POST'])
def updateGame(game_id):
    data = {
        'id': game_id,
        'teamOne': request.form['teamOne'],
        'teamTwo': request.form['teamTwo'],
        'finalScore': request.form['finalScore'],
        'info': request.form['info'],
        'gameDate': request.form['gameDate'],
    }
    Game.update(data)
    flash("Game data updated")
    return redirect('/dashboard/')

@app.route('/<int:game_id>/delete/')
def deleteGame(game_id):
    data = {
        'id': game_id
    }
    Game.delete(data)
    flash("Game has been deleted")
    return redirect('/dashboard/')