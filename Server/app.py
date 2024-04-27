from flask import Flask, request, jsonify, render_template, abort
from models import db, Team, Player, Match, Goal, Standing
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soccer.db'
db.init_app(app)



# Define your routes here

@app.route('/')
def home():
    db.create_all()
    return render_template('index.html')


@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/add_team', methods=['POST'])
def add_team():
    team_data = request.get_json()
    team_id = team_data.get('team_id')
    
    try:
        # Check if team_id already exists in the database
        if Team.query.filter_by(team_id=team_id).first():
            return jsonify({'message': 'Team ID already exists. Please enter a different ID.'}), 400
        
        try:
            team_id_int = int(team_id)
            if team_id_int < 0:
                return jsonify({'message': 'Invalid team ID. Please enter a positive integer.'}), 400
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid team ID. Please enter a valid integer.'}), 400

        # if 'club_name' not in team_data or 'coach' not in team_data or 'stadium' not in team_data or 'city' not in team_data:
        #     return jsonify({'message': 'Missing required data. Please fill in all fields.'}), 400

        new_team = Team(
            team_id=team_id,
            club_name=team_data['club_name'],
            coach=team_data['coach'],
            stadium=team_data['stadium'],
            city=team_data['city']
        )
        db.session.add(new_team)
        new_standing = Standing(
            standing_id=team_id,
            team_id = team_id,
            matches_played=0,
            wins=0,
            draws=0,
            losses=0,
            points=0
        )
        db.session.add(new_standing)
        db.session.commit()
        return jsonify({'message': 'Team created successfully!'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Failed to create team. Please try again.'}), 500

@app.route('/edit_team', methods=['POST'])
def edit_team():
    team_data = request.get_json()
    old_team_id = team_data.get('selected_team_id')
    team_id = team_data.get('team_id')

    try:
        # Check if team_id already exists in the database
        if Team.query.filter((Team.team_id == team_id) & (Team.team_id != old_team_id)).first():
            return jsonify({'message': 'Team ID already exists. Please enter a different ID.'}), 400
        
        try:
            team_id_int = int(team_id)
            if team_id_int < 0:
                return jsonify({'message': 'Invalid team ID. Please enter a positive integer.'}), 400
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid team ID. Please enter a valid integer.'}), 400

        team = db.session.query(Team).get(old_team_id)
        team_standing = db.session.query(Standing).get(old_team_id)
        print(team_standing)
        if team:
            team.team_id = team_data.get('team_id')
            team.club_name = team_data.get('club_name')
            team.coach = team_data.get('coach')
            team.stadium = team_data.get('stadium')
            team.city = team_data.get('city')
            team_standing.team_id = team_data.get('team_id')
            db.session.commit()
            return jsonify({'message': 'Team edited successfully!'}), 200
        else:
            return jsonify({'message': 'Team not found'}), 404
    except:
        db.session.rollback()

@app.route('/delete_team/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    try:
        team = db.session.query(Team).get(team_id)
        team_standing = db.session.query(Standing).get(team_id)
        if team_standing:
            db.session.delete(team_standing)
            db.session.commit()
        if team:
            db.session.delete(team)
            db.session.commit()
            return jsonify({'message': 'Team deleted'})
        else:
            return jsonify({'message': 'Team not found'})
    except:
        db.session.rollback()
    
@app.route('/get_teams', methods=['GET'])
def get_teams():
    teams = db.session.query(Team).all()
    return jsonify({'teams': [{'id': team.team_id, 'clubName': team.club_name} for team in teams]})

@app.route('/get_players', methods=['GET'])
def get_players():
    team_id = request.args.get('team_id')
    if team_id is None:
        return jsonify({'message': 'Missing team_id parameter'}), 400

    players = db.session.query(Player).filter(Player.team == team_id).all()
    return jsonify({'players': [{'id': player.player_id, 'first_name': player.first_name, 'last_name': player.last_name} for player in players]})

@app.route('/generate_player_report', methods=['GET'])
def generate_player_report():
    team_id = request.args.get('team_id')
    player_id = request.args.get('player_id')

    # Create a prepared statement with placeholders for the parameters
    query = text("""
        SELECT
            t.club_name,
            p.first_name,
            p.last_name,
            COUNT(g.goal_id) AS total_goals,
            COUNT(DISTINCT m.match_id) AS matches_played,
            CAST(COUNT(g.goal_id) AS FLOAT) / COUNT(DISTINCT m.match_id) AS avg_goals_per_game
        FROM
            teams t
            JOIN players p ON p.team = t.team_id
            JOIN matches m ON m.home_team = t.team_id OR m.away_team = t.team_id
            LEFT JOIN goals g ON g.player_id = p.player_id AND g.team_id = t.team_id AND g.match_id = m.match_id
        WHERE
            t.team_id = :team_id AND p.player_id = :player_id
        GROUP BY
            p.player_id
    """)


    # Execute the prepared statement with the parameter values
    result = db.session.execute(query, {"team_id": team_id, "player_id": player_id})

    # Fetch the results from the executed statement
    data = result.fetchall()

    data_list = []
    for row in data:
        row_dict = {}
        for i, column in enumerate(result.keys()):
            row_dict[column] = row[i]
        data_list.append(row_dict)

    print(data_list)
    
    # Return a JSON response with the relevant information
    return jsonify(data_list)

@app.route('/generate_team_report', methods=['POST'])
def generate_team_report():
    team_data = request.get_json()

    min_matches_played = team_data.get('minMatchesPlayed')
    max_matches_played = team_data.get('maxMatchesPlayed')
    min_points = team_data.get('minPoints')
    max_points = team_data.get('maxPoints')

    query = text("""
                SELECT
                    MIN(sp.matches_played) AS min_matches_played,
                    MAX(sp.matches_played) AS max_matches_played,
                    MIN(sp.points) AS min_points,
                    MAX(sp.points) AS max_points
                FROM
                    Standings sp
                JOIN teams t ON sp.team_id = t.team_id;
                 """)

    # Execute the prepared statement with the parameter values
    result = db.session.execute(query)

    # Fetch the results from the executed statement
    data = result.fetchall()

    if not min_matches_played:
        min_matches_played = data[0][0]
    if not max_matches_played:
        max_matches_played = data[0][1]
    if not min_points:
        min_points = data[0][2]
    if not max_points:
        max_points = data[0][3]
    

    query = text("""
        SELECT
            t.club_name,
            s.matches_played,
            s.wins,
            s.draws,
            s.losses,
            s.points,
            ROUND(CAST(s.points AS FLOAT) / s.matches_played, 2) AS avg_points_per_match
        FROM
            teams t
            JOIN standings s ON t.team_id = s.team_id
        WHERE
            s.matches_played >= :min_matches_played AND s.matches_played <= :max_matches_played AND s.points >= :min_points AND s.points <= :max_points
                 """)
    
    result = db.session.execute(query, {"min_matches_played": min_matches_played, "max_matches_played": max_matches_played, "min_points": min_points, "max_points": max_points})

    # Fetch the results from the executed statement
    data = result.fetchall()

    data_list = []
    for row in data:
        row_dict = {}
        for i, column in enumerate(result.keys()):
            row_dict[column] = row[i]
        data_list.append(row_dict)
    
    print(data_list)
    
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)
