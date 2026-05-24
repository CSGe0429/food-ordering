from decimal import Decimal
from flask import Blueprint, request, jsonify, session
from models import db, Order, OrderItem, CartItem, User
from utils import login_required_json

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/api/orders', methods=['POST'])
@login_required_json
def place_order():
    data = request.json or {}
    delivery_address = data.get('delivery_address', '').strip()
    notes = data.get('notes', '').strip()

    if not delivery_address:
        user = db.session.get(User, session['user_id'])
        delivery_address = user.address or ''
    if not delivery_address:
        return jsonify({'error': '请填写配送地址'}), 400

    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    if not cart_items:
        return jsonify({'error': '购物车为空'}), 400

    total = sum(item.subtotal for item in cart_items)

    order = Order(
        user_id=session['user_id'],
        total_amount=total,
        delivery_address=delivery_address,
        notes=notes
    )
    db.session.add(order)
    db.session.flush()

    for cart_item in cart_items:
        db.session.add(OrderItem(
            order_id=order.id,
            menu_item_id=cart_item.menu_item_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.menu_item.price
        ))

    CartItem.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()

    return jsonify({'message': '下单成功', 'order_id': order.id}), 201


@orders_bp.route('/api/orders', methods=['GET'])
@login_required_json
def get_orders():
    orders = Order.query.filter_by(user_id=session['user_id'])\
        .order_by(Order.created_at.desc()).all()

    return jsonify({
        'orders': [{
            'id': o.id,
            'total_amount': float(o.total_amount),
            'status': o.status,
            'delivery_address': o.delivery_address,
            'created_at': o.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'item_count': o.items.count()
        } for o in orders]
    })


@orders_bp.route('/api/orders/<int:order_id>', methods=['GET'])
@login_required_json
def get_order_detail(order_id):
    order = Order.query.filter_by(id=order_id, user_id=session['user_id']).first()
    if not order:
        return jsonify({'error': '订单不存在'}), 404

    return jsonify({
        'order': {
            'id': order.id,
            'total_amount': float(order.total_amount),
            'status': order.status,
            'delivery_address': order.delivery_address,
            'notes': order.notes or '',
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': [{
                'id': item.id,
                'name': item.menu_item.name,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price),
                'subtotal': float(item.subtotal)
            } for item in order.items]
        }
    })
