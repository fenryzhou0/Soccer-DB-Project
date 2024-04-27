from flask import Flask
from sqlalchemy.orm import sessionmaker
from models import db, Team, Player, Match, Goal, Standing
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soccer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy db instance
db.init_app(app)

# Hardcoded player data
player_data = {
    'player_id': 21,
    'first_name': 'Mohamed',
    'last_name': 'Salah',
    'position': 'RW',
    'team': 7
}

# Hardcoded match data
match_data = {
    'match_id': 7,
    'home_team': 3,
    'away_team': 1,
    'date': datetime.now(),
    'stadium': "Metropolitano",
    'home_team_score': 1, 
    'away_team_score': 3
}

# Hardcoded goal data
goal_data = {
    'goal_id': 31,
    'player_id': 1,
    'match_id': 7,
    'team_id': 1,
}

# Hardcoded standing data
standing_data = {
    'standing_id': 7,
    'team_id': 7,
    'matches_played': 2,
    'wins': 1,
    'draws': 1,
    'losses': 0,
    'points': 4
}

def insert_player(player_data):
    with app.app_context():
        new_player = Player(**player_data)
        db.session.add(new_player)
        db.session.commit()
        print('Player added successfully')

def delete_player(player_id):
    with app.app_context():
        player_to_remove = Player.query.get(player_id)
        if player_to_remove:
            db.session.delete(player_to_remove)
            db.session.commit()
            print('Player removed successfully')
        else:
            print('No player found with the given ID')

def insert_match(match_data):
    with app.app_context():
        new_match = Match(**match_data)
        db.session.add(new_match)
        db.session.commit()
        print('Match added successfully')

def delete_match(match_id):
    with app.app_context():
        match_to_remove = Match.query.get(match_id)
        if match_to_remove:
            db.session.delete(match_to_remove)
            db.session.commit()
            print('Match removed successfully')
        else:
            print('No match found with the given ID')

def insert_goal(goal_data):
    with app.app_context():
        new_goal = Goal(**goal_data)
        db.session.add(new_goal)
        db.session.commit()
        print('Goal added successfully')

def delete_goal(goal_id):
    with app.app_context():
        goal_to_remove = Goal.query.get(goal_id)
        if goal_to_remove:
            db.session.delete(goal_to_remove)
            db.session.commit()
            print('Goal removed successfully')
        else:
            print('No goal found with the given ID')

def insert_standing(standing_data):
    with app.app_context():
        new_standing = Standing(**standing_data)
        db.session.add(new_standing)
        db.session.commit()
        print('Standing added successfully')

def delete_standing(standing_id):
    with app.app_context():
        standing_to_remove = Standing.query.get(standing_id)
        if standing_to_remove:
            db.session.delete(standing_to_remove)
            db.session.commit()
            print('Standing removed successfully')
        else:
            print('No standing found with the given ID')

def select_all_matches():
    with app.app_context():
        all_matches = Match.query.all()
        for match in all_matches:
            print(match)
    
def select_all_players():
    with app.app_context():
        all_players = Player.query.all()
        for player in all_players:
            print(player)

def select_all_goals():
    with app.app_context():
        all_goals = Goal.query.all()
        for goal in all_goals:
            print(goal)

def select_all_standings():
    with app.app_context():
        all_standings = Standing.query.all()
        for standing in all_standings:
            print(standing)

# insert_player(player_data)
# delete_player(4)
# select_all_players()

# insert_match(match_data)
# delete_match(2)
# select_all_matches()

# insert_goal(goal_data)
# delete_goal(1)
# select_all_goals()

insert_standing(standing_data)
# delete_standing(1)
# select_all_standings()

