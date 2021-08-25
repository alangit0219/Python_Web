# -*- coding:utf-8 -*-
######################################################
#        > File Name: flask_client.py
#      > Author: HsiehTungYuan
#     > Mail: xiedong0219@gmail.com
#     > Created Time: Wen 14 July 2021  11:52:00 AM CST
######################################################

from flask import Flask, send_file

app = Flask(__name__)


@app.route('/index')
def index():
    # 首页
    return send_file('templates/index.html')


@app.route('/introduction')
def introduction():
    # 商店介紹
    return send_file('templates/introduction.html')


@app.route('/products')
def products():
    # 所有商品
    return send_file('templates/products.html')


@app.route('/commodity/<c_id>')
def product(c_id):
    # 單一商品
    return send_file('templates/product.html')


@app.route('/shipping')
def shipping():
    # 運費政策
    return send_file('templates/shipping.html')


@app.route('/login')
def login():
    # 登錄
    return send_file('templates/login.html')


# 127.0.0.1:5000/('/<username>/user')
@app.route('/user/<username>')
def user(username):
    # 會員管理
    return send_file('templates/user.html')


@app.route('/user_order')
def user_order():
    # 會員管理
    return send_file('templates/user_order.html')


@app.route('/carts')
def carts():
    # 購物車
    return send_file('templates/carts.html')


@app.route('/order/<order_num>')
def order(order_num):
    # 會員管理
    return send_file('templates/order.html')


@app.route('/payment_completed')
def payment():
    # 付款完成
    return send_file('templates/payment_completed.html')


if __name__ == '__main__':
    app.run(debug=True)

