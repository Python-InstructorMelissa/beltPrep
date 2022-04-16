from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Game:
    db = 'baseball'
    def __init__(self, data):
        self.id = data['id']
        self.teamOne = data['teamOne']
        self.teamTwo = data['teamTwo']
        self.finalScore = data['finalScore']
        self.info = data['info']
        self.gameDate = data['gameDate']
        self.createdAt = data['createdAt']
        self.updateAt = data['updatedAt']
        self.user_id = data['user_id']

    def teams(self):
        return f'{self.teamOne} vs {self.teamTwo}'

    @staticmethod
    def validate(game):
        isValid = True
        if len(game['teamOne']) < 3:
            isValid = False
            flash("Please use team official name that is more than 3 characters")
        if len(game['teamTwo']) < 3:
            isValid = False
            flash("Please use team official name that is more than 3 characters")
        return isValid

    
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM game;"
        results = connectToMySQL(cls.db).query_db(query)
        games = []
        for row in results:
            games.append(cls(row))
        return games

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM game WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO game (teamOne, teamTwo, finalScore, info, gameDate, user_id) VALUES (%(teamOne)s, %(teamTwo)s, %(finalScore)s, %(info)s, %(gameDate)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE game SET teamOne=%(teamOne)s, teamTwo=%(teamTwo)s, finalScore=%(finalScore)s, info=%(info)s, gameDate=%(gameDate)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM game WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def allEntries(cls):
        query = 'SELECT * FROM game JOIN user on game.user_id = user.id;'
        results = connectToMySQL(cls.db).query_db(query)
        print('The Reuslts allEntries Model: ', results)
        return results