from decimal import Decimal
from flask import Blueprint, request, jsonify, session
from models import db, CartItem, MenuItem
from utils import login_required_json

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/api/cart', methods=['GET'])
@login_required_json
def get_cart():
    items = CartItem.query.filter_by(user_id=session['user_id']).all()
    total = sum(item.subtotal for item in items)

    return jsonify({
        'items': [{
            'id': item.id,
            'menu_item_id': item.menu_item_id,
            'name': item.menu_item.name,
            'price': float(item.menu_item.price),
            'quantity': item.quantity,
            'subtotal': float(item.subtotal)
        } for item in items],
        'total': float(total),
        'count': len(items)
    })


@cart_bp.route('/api/cart/add', methods=['POST'])
@login_required_json
def add_to_cart():
    data = request.json or {}
    menu_item_id = data.get('menu_item_id')
    quantity = max(1, int(data.get('quantity', 1) or 1))

    if not menu_item_id:
        return jsonify({'error': '请指定菜品'}), 400

    menu_item = db.session.get(MenuItem, menu_item_id)
    if not menu_item or not menu_item.is_available:
        return jsonify({'error': '菜品不存在或已下架'}), 404

    existing = CartItem.query.filter_by(
        user_id=session['user_id'], menu_item_id=menu_item_id
    ).first()

    if existing:
        existing.quantity += quantity
    else:
        db.session.add(CartItem(
            user_id=session['user_id'],
            menu_item_id=menu_item_id,
            quantity=quantity
        ))

    db.session.commit()
    return jsonify({'message': '已加入购物车'})


@cart_bp.route('/api/cart/<int:item_id>', methods=['PUT'])
@login_required_json
def update_cart_item(item_id):
    item = CartItem.query.filter_by(id=item_id, user_id=session['user_id']).first()
    if not item:
        return jsonify({'error': '购物车项不存在'}), 404

    quantity = (request.json or {}).get('quantity')
    if quantity is None or int(quantity) <= 0:
        db.session.delete(item)
    else:
        item.quantity = int(quantity)

    db.session.commit()
    return jsonify({'message': '已更新'})


@cart_bp.route('/api/cart/<int:item_id>', methods=['DELETE'])
@login_required_json
def delete_cart_item(item_id):
    item = CartItem.query.filter_by(id=item_id, user_id=session['user_id']).first()
    if not item:
        return jsonify({'error': '购物车项不存在'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': '已删除'})


@cart_bp.route('/api/cart', methods=['DELETE'])
@login_required_json
def clear_cart():
    CartItem.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    return jsonify({'message': '购物车已清空'})
