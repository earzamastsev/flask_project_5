from app import app
from flask import render_template, jsonify, request, abort
from schemas import LocationSchema, EventSchema, ParticipantsSchema, TypeSchema
from models import db, Location, Event, Participant, TypeEvent


@app.route('/')
def index():
    return 'Hello word!'


# GET /locations/ – выводит список городов или локаций
@app.route('/locations/')
def locations():
    location_schema = LocationSchema(many=True)
    locations = db.session.query(Location).all()
    serialized = location_schema.dump(locations)
    return jsonify(serialized)


# GET /events/ – выводит список ближайших событий в городе,
@app.route('/events/')
def events():
    eventtype = request.args.get('eventtype')
    location = request.args.get('location')
    event_schema = EventSchema(many=True)
    if eventtype:
        evnt = db.session.query(TypeEvent).filter(TypeEvent.code == eventtype).first_or_404()
        events = db.session.query(Event).filter(Event.types.contains(evnt)).all()
    elif location:
        loc = db.session.query(Location).filter(Location.code == location).first_or_404()
        events = db.session.query(Event).filter(Event.locations.contains(loc)).all()
    elif request.args:
        return abort(404)
    else:
        events = db.session.query(Event).all()
    serialized = event_schema.dump(events)
    return jsonify(serialized)


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
    json_data = request.get_json()
    if json_data:
        if db.session.query(Participant).filter(Participant.email == json_data['email']).first():
            return jsonify({"status": "error - user already exist"})
        user = Participant(**json_data)
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": "ok", "id": user.id})
    return jsonify({"status": "error"}), 500


# POST /auth/ – проводит аутентификацию пользователя
@app.route('/auth/', methods=['POST'])
def auth():
    return jsonify({"status": "success", "key": 111111111})


# GET /profile/  – возвращает информацию о профиле пользователя
@app.route('/profile/<int:uid>/')
def profile(uid):
    user = db.session.query(Participant).get(uid)
    if not user:
        return jsonify({"status": "error"})
    user_schema = ParticipantsSchema(exclude=['password'])
    serialized = user_schema.dump(user)
    return jsonify(serialized)


@app.errorhandler(404)
def error(e):
    return jsonify({"status": "error"}), 500
