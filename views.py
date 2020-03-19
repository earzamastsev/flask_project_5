from app import app
from flask import render_template, jsonify


@app.route('/')
def index():
    return 'Hello word!'


# GET /locations/ – выводит список городов или локаций
@app.route('/locations/')
def locations():
    return jsonify([])


# GET /events/ – выводит список ближайших событий в городе,
@app.route('/events/')
def events():
    return jsonify([])


# POST /enrollments/ – принимает заявку на участие в событии
@app.route('/enrollments/', methods=['POST'])
def enrollments_add():
    return jsonify({"status": "success"})


# DELETE /enrollments/ id=<eventid> – отзывает заявку на участие в событии
@app.route('/enrollments/', methods=['DELETE'])
def enrollments_del():
    return jsonify({"status": "success"})


# POST /register/ – регистрирует пользователя
@app.route('/register/', methods=['POST'])
def register():
    return jsonify({"status": "ok", "id": 1})


# POST /auth/ – проводит аутентификацию пользователя
@app.route('/auth/', methods=['POST'])
def auth():
    return jsonify({"status": "success", "key": 111111111})


# GET /profile/  – возвращает информацию о профиле пользователя
@app.route('/profile/')
def profile():
    return jsonify({"id": 1, "picture": "", "city": "nsk", "about": "", "enrollments": []})
