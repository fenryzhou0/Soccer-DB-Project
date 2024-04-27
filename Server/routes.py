from flask import Flask, request, jsonify
from models import db, Team

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soccer.db'
db.init_app(app)

@app.route('/team', methods=['POST'])
def create_team():
    team_data = request.get_json()
    new_team = Team(**team_data)
    db.session.add(new_team)
    db.session.commit()
    return jsonify(new_team)

# @app.route('/add_team', methods=['POST'])
# def add_team():
#     print("called add team")
#     team_data = request.get_json()
#     new_team = Team(
#         club_name=team_data['clubName'],
#         coach=team_data['coach'],
#         stadium=team_data['stadium'],
#         city=team_data['city']
#     )
#     db.session.add(new_team)
#     db.session.commit()
#     print("team added")
#     return jsonify({'message': 'Team created'})

# @app.route('/team/<int:team_id>', methods=['PUT'])
# def update_team(team_id):
#     team_data = request.get_json()
#     Team.query.filter_by(team_id=team_id).update(team_data)
#     db.session.commit()
#     return jsonify({'message': 'Team updated'})

# @app.route('/team/<int:team_id>', methods=['DELETE'])
# def delete_team(team_id):
#     Team.query.filter_by(team_id=team_id).delete()
#     db.session.commit()
#     return jsonify({'message': 'Team deleted'})
