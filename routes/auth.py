from flask import Blueprint, request, jsonify, session
from models import db, User
from utils import login_required_json

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    if len(username) < 2:
        return jsonify({'error': '用户名至少2个字符'}), 400
    if len(password) < 4:
        return jsonify({'error': '密码至少4个字符'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 409

    user = User(
        username=username,
        phone=data.get('phone', '').strip(),
        address=data.get('address', '').strip()
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    session['username'] = user.username
    return jsonify({'message': '注册成功', 'user': {'id': user.id, 'username': user.username}}), 201


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': '用户名或密码错误'}), 401

    session['user_id'] = user.id
    session['username'] = user.username
    return jsonify({'message': '登录成功', 'user': {'id': user.id, 'username': user.username}})


@auth_bp.route('/api/auth/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({'message': '已退出登录'})


@auth_bp.route('/api/auth/me', methods=['GET'])
@login_required_json
def me():
    user = db.session.get(User, session['user_id'])
    if not user:
        session.clear()
        return jsonify({'error': '用户不存在'}), 401
    return jsonify({
        'user': {
            'id': user.id, 'username': user.username,
            'phone': user.phone, 'address': user.address
        }
    })
