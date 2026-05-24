from flask import Flask, render_template, session, redirect, url_for
from config import Config
from models import db, Category, MenuItem
from routes.auth import auth_bp
from routes.menu import menu_bp
from routes.cart import cart_bp
from routes.orders import orders_bp
from utils import login_required_page, guest_only


def seed_database():
    if Category.query.first():
        return
    categories = [
        (1, '经典面食', 1),
        (2, '盖饭/套餐', 2),
        (3, '风味小食', 3),
        (4, '饮品', 4),
        (5, '甜品', 5),
    ]
    for cid, name, sort_order in categories:
        db.session.add(Category(id=cid, name=name, sort_order=sort_order))

    items = [
        (1, '红烧牛肉面', '大块牛腱肉配浓郁骨汤，手工拉面劲道十足', 26.00, 1),
        (2, '番茄鸡蛋面', '酸甜番茄汤底，爽滑面条配嫩滑鸡蛋', 16.00, 1),
        (3, '重庆小面', '麻辣鲜香，花生碎加葱花，地道重庆味', 18.00, 1),
        (4, '炸酱面', '老北京炸酱，肉丁酱香浓郁，配黄瓜丝', 20.00, 1),
        (5, '酸辣粉', '酸辣开胃，红薯粉爽滑Q弹，花生香菜提香', 14.00, 1),
        (6, '葱油拌面', '葱油飘香，简单却令人回味', 12.00, 1),
        (7, '宫保鸡丁饭', '经典川味，鸡丁嫩滑配花生，麻辣鲜香', 24.00, 2),
        (8, '红烧排骨饭', '秘制酱料慢炖排骨，骨香浓郁配白米饭', 30.00, 2),
        (9, '番茄鸡蛋盖饭', '酸甜可口家常味，盖满整碗', 17.00, 2),
        (10, '鱼香肉丝饭', '正宗鱼香味，肉丝嫩滑配木耳胡萝卜', 22.00, 2),
        (11, '蛋炒饭', '粒粒金包银，简单即经典', 13.00, 2),
        (12, '咖喱鸡块饭', '日式咖喱浓郁醇厚，鸡块土豆胡萝卜慢炖', 26.00, 2),
        (13, '炸鸡翅', '外酥里嫩金黄鸡翅（4只），配甜辣酱', 16.00, 3),
        (14, '黄金薯条', '现炸粗薯条撒海盐，外酥内软', 10.00, 3),
        (15, '盐酥鸡', '台式盐酥鸡，九层塔提香，外酥内多汁', 15.00, 3),
        (16, '春卷', '酥脆春卷（4个），猪肉白菜馅，配甜辣酱', 12.00, 3),
        (17, '凉拌黄瓜', '蒜泥拍黄瓜，清脆爽口解腻', 8.00, 3),
        (18, '毛豆', '盐水煮毛豆，越嚼越香', 9.00, 3),
        (19, '珍珠奶茶', '台式经典，Q弹黑糖珍珠配浓郁奶茶', 15.00, 4),
        (20, '冰美式咖啡', '精选阿拉比卡豆，清爽醇苦', 16.00, 4),
        (21, '冰镇可乐', '可口可乐 330ml，加冰', 5.00, 4),
        (22, '柠檬绿茶', '鲜柠檬配茉莉绿茶，清爽解腻', 10.00, 4),
        (23, '杨枝甘露', '芒果椰奶西柚粒，港式经典', 18.00, 4),
        (24, '酸梅汤', '古法熬制冰镇酸梅汤，生津止渴', 8.00, 4),
        (25, '芒果冰沙', '新鲜芒果现打制成，冰爽甜蜜', 22.00, 5),
        (26, '提拉米苏', '经典意式甜点，咖啡与马斯卡彭的完美融合', 26.00, 5),
        (27, '双皮奶', '顺德传统甜品，奶香浓郁口感嫩滑', 16.00, 5),
        (28, '红豆沙', '陈皮红豆沙，绵密香甜暖胃', 12.00, 5),
        (29, '抹茶冰淇淋', '日式抹茶冰淇淋两球，微苦回甘', 18.00, 5),
        (30, '芒果糯米饭', '泰式经典，椰浆糯米配新鲜芒果', 20.00, 5),
    ]
    for item_id, name, desc, price, cat_id in items:
        db.session.add(MenuItem(id=item_id, name=name, description=desc, price=price, category_id=cat_id, is_available=True))

    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # 注册 API 蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)

    # ── 页面路由 ──

    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('page_menu'))
        return redirect(url_for('page_login'))

    @app.route('/login')
    @guest_only
    def page_login():
        return render_template('login.html')

    @app.route('/register')
    @guest_only
    def page_register():
        return render_template('register.html')

    @app.route('/menu')
    @login_required_page
    def page_menu():
        return render_template('menu.html')

    @app.route('/cart')
    @login_required_page
    def page_cart():
        return render_template('cart.html')

    @app.route('/orders')
    @login_required_page
    def page_orders():
        return render_template('orders.html')

    # 自动建表与种子数据（首次运行）
    with app.app_context():
        db.create_all()
        seed_database()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
