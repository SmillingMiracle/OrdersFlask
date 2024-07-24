from app import app, db
from models import Departaments, Employees, Title

from flask import Flask, render_template, session, redirect, url_for

from flask_login import login_required, current_user

from models.order.models import OrderTitle


@app.route('/add_to_cart/<int:title_id>')
@login_required
def add_to_cart(title_id):
    # Отримати продукт за його ідентифікатором
    title = Title.query.get(title_id)

    # Перевірити, чи кошик є в сесії
    if 'cart' not in session:
        session['cart'] = []

    # Додати продукт до кошика
    session['cart'].append({
        'title_id': title.id,
        'id_user': title.id_user,
        'description': title.description,
        'filename': title.filename
    })

    #return render_template('main.html')
    return redirect(url_for('show_cart'))


@app.route('/cart')
@login_required
def show_cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/orders')
@login_required
def orders():
    cart = session.get('cart', [])

    # Створити замовлення для кожного продукту в кошику
    for item in cart:
        orders = OrderTitle(
            user_id=current_user.get_id(),
            title_id=item['title_id'],
        )
        db.session.add(orders)

    db.session.commit()
    user_orders = OrderTitle.query.order_by(OrderTitle.id.desc()).all()
    return render_template('orders.html', orders=user_orders)
