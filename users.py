import re
from flask import Blueprint
import hashlib
import secrets


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def index():
    users = user.query.all()
    result = []
    for u in tweets:
        result.append(u.serialize())
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = user.query.get_or_404(id)
    return jsonify(t.serialize())


@bp.route('', methods=['POST'])
def create():
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    if len(request.json['username']) < 4 or len(request.json['password']) < 8:
        return abort(400)
    u = User(
        username=request.json['username'],
        password=request.json['password']
    )
    db.session.add(u)
    db.session.commit()
    return jsonify(t.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = user.query.get_or_404(id)
    try:
        db.session.delete(u)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    u = User.query.get_or_404(id)
    if 'username' not in request.json and 'password' not in request.json:
        return abort(400)
    if 'username' in request.json:
        u.username = request.json['username']
    if 'password' in request.json:
        u.password = scramble(request.json['password'])

    try:
        db.session.commit()
        return jsonify(True)

    except:
        return jsonify(False)


@bp.route('/<int:id>/liked_tweets', methods=['GET'])
def liking_users(id: int):
    u = User.query.get_or_404(id)
    likes = u.liked_users
    result = []
    for l in likes:
        result.append(l.serialize())
    return jsonify(result)


@bp.route('/<int:id>/liked_tweets', methods=['GET'])
def liked_tweets(id: int):
    u = User.query.get_or_404(id)
    likes = u.liked_tweets
    result = []
    for l in likes:
        result.append(l.serialize())
    return jsonify(result)
