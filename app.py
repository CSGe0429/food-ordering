from flask import Flask, render_template, session, redirect, url_for
from config import Config
from models import db
from routes.auth import auth_bp
from routes.menu import menu_bp
from routes.cart import cart_bp
from routes.orders import orders_bp
from utils import login_required_page, guest_only


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

    # 自动建表（首次运行）
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
