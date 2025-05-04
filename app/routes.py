from app.blueprints import routes_blueprint
from app.controllers import calories_data, login, logout, index, profile, log_workout, signup



routes_blueprint.route('/login', methods=['GET', 'POST'])(login)
routes_blueprint.route('/signup', methods=['GET', 'POST'])(signup)
routes_blueprint.route('/logout')(logout)
routes_blueprint.route('/')(index)
routes_blueprint.route('/profile')(profile)
routes_blueprint.route('/log', methods=['GET', 'POST'])(log_workout)
routes_blueprint.route('/api/calories', methods=['GET'])(calories_data)

