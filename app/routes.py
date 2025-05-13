from app.blueprints import routes_blueprint
from app.controllers import calories_data, edit_profile, login, logout, index, profile, log_workout, signup, view_friends, accept_friend, decline_friend, start_exercise, workout_plans



routes_blueprint.route('/login', methods=['GET', 'POST'])(login)
routes_blueprint.route('/signup', methods=['GET', 'POST'])(signup)
routes_blueprint.route('/logout')(logout)
routes_blueprint.route('/')(index)
routes_blueprint.route('/profile')(profile)
routes_blueprint.route('/start_exercise', methods=['GET', 'POST'])(start_exercise)
routes_blueprint.route('/log', methods=['GET', 'POST'])(log_workout)
routes_blueprint.route('/api/calories', methods=['GET'])(calories_data)
routes_blueprint.route('/friends', methods=['GET','POST'])(view_friends)
routes_blueprint.route('/friends/accept/<int:req_id>', methods=['POST'])(accept_friend)
routes_blueprint.route('/friends/decline/<int:req_id>', methods=['POST'])(decline_friend)
routes_blueprint.route('/edit_profile', methods=['GET', 'POST'])(edit_profile)
routes_blueprint.route('/workout_plans', methods=['GET', 'POST'])(workout_plans)

