from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'Teams'
    team_id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(64))
    coach = db.Column(db.String(64))
    stadium = db.Column(db.String(64))
    city = db.Column(db.String(64))

    def serialize(self):
        return {
            'team_id': self.team_id,
            'club_name': self.club_name,
            'coach': self.coach,
            'stadium': self.stadium,
            'city': self.city
        }

class Player(db.Model):
    __tablename__ = 'Players'
    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    position = db.Column(db.String(64))
    team = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))

    def serialize(self):
        return {
            'player_id': self.player_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
            'team': self.team
        }
    
class Match(db.Model):
    __tablename__ = 'Matches'
    match_id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
    away_team = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    stadium = db.Column(db.String(64))
    home_team_score = db.Column(db.Integer)
    away_team_score = db.Column(db.Integer)

    def serialize(self):
        return {
            'match_id': self.match_id,
            'home_team': self.home_team,
            'away_team': self.away_team,
            'date': self.date,
            'stadium': self.stadium,
            'home_team_score': self.home_team_score,
            'away_team_score': self.away_team_score
        }
    
class Goal(db.Model):
    __tablename__ = 'Goals'
    goal_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('Players.player_id'))
    match_id = db.Column(db.Integer, db.ForeignKey('Matches.match_id'))
    team_id = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))

    def serialize(self):
        return {
            'goal_id': self.goal_id,
            'player_id': self.player_id,
            'match_id': self.match_id,
            'team_id': self.team_id
        }

class Standing(db.Model):
    __tablename__ = 'Standings'
    standing_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
    matches_played = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    points = db.Column(db.Integer)

    def serialize(self):
        return {
            'standing_id': self.standing_id,
            'team_id': self.team_id,
            'matches_played': self.matches_played,
            'wins': self.wins,
            'draws': self.draws,
            'losses': self.losses,
            'points': self.points
        }
    
