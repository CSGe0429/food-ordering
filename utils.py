from functools import wraps
from flask import session, jsonify, redirect, url_for


def login_required_json(f):
    """要求登录的 API 装饰器，未登录返回 401 JSON"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated


def login_required_page(f):
    """要求登录的页面装饰器，未登录重定向到登录页"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('page_login'))
        return f(*args, **kwargs)
    return decorated


def guest_only(f):
    """仅游客可访问（已登录用户重定向到菜单页）"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' in session:
            return redirect(url_for('page_menu'))
        return f(*args, **kwargs)
    return decorated
