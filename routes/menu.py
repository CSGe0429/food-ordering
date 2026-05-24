from flask import Blueprint, request, jsonify
from models import Category, MenuItem

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/api/menu/categories', methods=['GET'])
def get_categories():
    categories = Category.query.order_by(Category.sort_order).all()
    return jsonify({
        'categories': [{'id': c.id, 'name': c.name} for c in categories]
    })


@menu_bp.route('/api/menu/items', methods=['GET'])
def get_items():
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '').strip()

    query = MenuItem.query.filter_by(is_available=True)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(MenuItem.name.contains(search))

    items = query.order_by(MenuItem.category_id, MenuItem.id).all()
    return jsonify({
        'items': [{
            'id': item.id,
            'name': item.name,
            'description': item.description or '',
            'price': float(item.price),
            'category_id': item.category_id
        } for item in items]
    })
