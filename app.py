import base64
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from numpy import cumsum
import app
from datetime import datetime, timedelta
import jwt
from functools import wraps

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///practice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '12345'


class Role(db.Model):

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50))

    # For one to one relationship
    user = db.relationship('User', backref='role', uselist=False)

    def __repr__(self):
        return 'Role ' + str(self.role_id)+" " + str(self.role_name)


class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    password = db.Column(db.String(50))

    # 1-1
    user_role = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    product = db.relationship('Product', backref='user')
    cart = db.relationship('Cart', backref='user', uselist=False)

    def __repr__(self):
        return 'User  ' + str(self.user_id)+" " + str(self.user_name)+" "+str(self.password)+" "+str(self.user_role)


class Category(db.Model):

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50))

    # 1-Many
    product = db.relationship('Product', backref='category')

    def __repr__(self):
        return 'Category  ' + str(self.category_id)+" " + str(self.category_name)


class Product(db.Model):

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50))
    price = db.Column(db.Float)

    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    cart_product = db.relationship('CartProduct', backref='product')

    def __repr__(self):
        return 'Product ' + str(self.product_id)+" " + str(self.product_name)+" " + str(self.price)+" " + str(self.category_id)+" " + str(self.seller_id)


class Cart(db.Model):

    cart_id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    cart_product = db.relationship('CartProduct', backref='cart')

    def __repr__(self):
        return 'Cart  ' + str(self.cart_id)+" " + str(self.total_amount)+" "+str(self.user_id)


class CartProduct(db.Model):

    cp_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.String(50), db.ForeignKey('cart.cart_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return 'Cart Product ' + str(self.cp_id)+" " + str(self.cart_id)+" " + str(self.product_id)+" " + str(self.quantity)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print("token is "+token)

        if not token:
            return jsonify({'Message': 'Token is missing'}), 401

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms='HS256')
            print("Decoded JWT : ", data)
            current_user = User.query.filter_by(user_name=data['user']).first()
        except:
            return jsonify({'Message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/public/login', methods=['POST', 'GET'])
def login():
    a = request.headers.get('Authorization')
    b = a.split(" ")
    c = b[1]
    l = base64.b64decode(c).decode('UTF-8')
    print("l is "+l)
    m = l.split(":")
    print(l)
    userName_ = m[0]
    passWord_ = m[1]
    print(a)
    user1 = User.query.filter_by(user_name=userName_).first()
    if user1:
        if user1.password == passWord_:
            token = jwt.encode({
                'user': userName_,
                'expiration': str(datetime.utcnow() + timedelta(minutes=30))

            }, app.config['SECRET_KEY'])
            #
            # return jsonify({'token': token.decode('utf-8')})
            return jsonify({'token': token}), 200

        else:
            return {}, 401
    else:
        return {}, 401


@app.route('/api/public/loginPostman', methods=['POST', 'GET'])
def loginPostman():
    userName_ = request.headers.get('user_name')
    passWord_ = request.headers.get("password")
    user1 = User.query.filter_by(user_name=userName_).first()
    if user1:
        if user1.password == passWord_:
            token = jwt.encode({
                'user': userName_,
                'expiration': str(datetime.utcnow() + timedelta(minutes=30))

            }, app.config['SECRET_KEY'])
            #
            # return jsonify({'token': token.decode('utf-8')})
            return jsonify({'token': token}), 200

        else:
            return {}, 401
    else:
        return {}, 401


# fp
# public endpoints api/public/product/search?keyword="crocin"
# accessing through query parameters
@app.route('/api/public/product/search', methods=['GET'])
def getProducts():

    prod = (request.args.get('keyword'))
    prod.strip()

    rq = prod.replace('"', '')

    res = db.session.query(Product).join(Category).filter(
        Product.product_name == rq).first()
    print(res)
    if not res:
        return {}, 400
    print(res)
    prodId = res.product_id
    price = res.price
    name = res.product_name
    categoryId = res.category_id

    categoryDetails = Category.query.filter_by(category_id=categoryId).first()
    catId = categoryDetails.category_id
    catName = categoryDetails.category_name

    print(catId)
    print(catName)

    sellerId = res.seller_id

    print(price)
    print(name)
    print(categoryId)
    print(sellerId)

    f = []
    d = {}

    d["category"] = {"category_id": catId, "category_name": catName}
    d["price"] = price
    d["product_id"] = prodId
    d["product_name"] = name
    d["seller_id"] = sellerId

    f.append(d)

    return jsonify(f)

# fp
# remove get


# authentication endpoints
# api/auth/consumer/cart?"JWT"=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiamFjayIsImV4cGlyYXRpb24iOiIyMDIyLTA2LTE5IDA2OjMwOjI1Ljg5NTA4MiJ9.ZJob2W1Lloe2SIj2e7713vJEO-m8e6EboomeF7iEajI
@app.route('/api/auth/consumer/cart', methods=['GET'])
@token_required
def consumerCart(cu):


    userRole = cu.user_role
    roleDetails = Role.query.filter_by(role_id=cu.user_role).first()
    print("role detials are,",roleDetails)
    roleName =roleDetails.role_name

    if roleName != "CONSUMER":
        return {}, 403

    crt_id = Cart.query.filter_by(user_id=cu.user_id).first().cart_id
    res = CartProduct.query.filter_by(cart_id=crt_id)
    print(res)

    if not res:
        return '', 403

    l=[]
    for i in res:


        cpId = i.cp_id
        cartId = i.cart_id
        prodId = i.product_id

        print(i.product_id)

        cartDetails = Cart.query.filter_by(cart_id=cartId).first()
        amount = cartDetails.total_amount

        productDetails = Product.query.filter_by(product_id=prodId).first()
        productName = productDetails.product_name
        pricE = productDetails.price

        categoryId = productDetails.category_id
        print(productDetails)

        catDetails = Category.query.filter_by(category_id=categoryId).first()
        catId = catDetails.category_id
        catName = catDetails.category_name

        print(catId)
        print(catName)

        d = {}

        d["cartproducts"] = {
                "product": {
                    "product_id": prodId,
                    "price": pricE,
                    "product_name": productName,
                    "category": {
                        "category_name": catName,
                        "category_id": catId
                    }
                },
                "cp_id": cpId

        }

        d["cart_id"] = cartId
        d["total_amount"] = amount

        l.append(d)
        print(l)

    return jsonify(l)


@app.route('/api/auth/consumer/cart', methods=['POST'])
@token_required
def postConsumerCart(cu):

    prodId = request.get_json()["product_id"]
    quantitY = request.get_json()["quantity"]

    userRole = cu.user_role
   
    roleDetails = Role.query.filter_by(role_id=userRole).first()
    roleName = roleDetails.role_name
   
    if roleName!="CONSUMER":
        return '',403

    p = Product.query.filter_by(product_id=prodId).first()

    if p:
        return '',409


    cartDetails = Cart.query.filter_by(user_id=cu.user_id).first()
    cartId = cartDetails.cart_id

    productDetails = Product.query.filter_by(product_id=prodId).first()
    prodPrice = productDetails.price

    ta = prodPrice*quantitY

    cp = CartProduct(cart_id=cartId, product_id=prodId, quantity=quantitY)

        #c=Cart(cart_id=cartId, product_id=prodId,quantity=quantitY)

    totalAmount = cartDetails.total_amount+ta

    cartDetails.total_amount = totalAmount

    db.session.add(cartDetails)
    db.session.add(cp)
    db.session.commit()

    return str(totalAmount)

    

   # payload= jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])

    # return 'HEY THERE'


@app.route('/api/auth/consumer/cart', methods=['PUT'])
@token_required
def updateConsumerCart(cu):

    json_data = request.get_json()
    productId = json_data['product_id']
    quantitY = json_data['quantity']

    userId = cu.user_id
    userRole = cu.user_role
    print(userRole)

    roleDetails = Role.query.filter_by(role_id=userRole).first()
    roleName = roleDetails.role_name
    print(roleName)

    if roleName!="CONSUMER":
        return '',403

    cartprodDetails = CartProduct.query.filter_by(product_id=productId).first()
    
    if not cartprodDetails:
        return '',409 

    cartId = cartprodDetails.cart_id

    cartDetails = Cart.query.filter_by(
        cart_id=cartId).first()

    if cartDetails.user_id != userId:
        return '',409

    if not cartDetails:
        return '',409

    prodDetails = Product.query.filter_by(product_id=productId).first()
    pricE = prodDetails.price

    #cartProduct me update krna hai ki nhi vo nhi pta
    cartprodDetails.quantity = quantitY

    tamount = pricE*quantitY

    cartDetails.total_amount = tamount

    db.session.add(cartprodDetails)
    db.session.add(cartDetails)
    db.session.commit()

    return str(tamount), 200

   

       
  


@app.route('/api/auth/consumer/cart', methods=['DELETE'])
@token_required
def deleteConsumerCart(cu):

    json_data = request.get_json()
    productId = json_data['product_id']
 
    userId = cu.user_id
    userRole = cu.user_role
    print(userRole)

    roleDetails = Role.query.filter_by(role_id=userRole).first()
    roleName = roleDetails.role_name
  
    if roleName!= "CONSUMER":
        return 'aaa',403

    print("aa")
    prodDetails = Product.query.filter_by(product_id = productId).first()
    #17....2
    print("prodDET",prodDetails.seller_id)
    print("proUserT",not(prodDetails.seller_id==userId))
    if not prodDetails:
        return '',401
    
    

    if not (prodDetails.seller_id == userId):
        print("bb")
        return '',401

    print("cc")

  

    cartprodDetails = CartProduct.query.filter_by(product_id=productId).first()
    cc=cartprodDetails.cart_id
    if not cartprodDetails:
            print("Hey")
            return {},401

    cartDetails = Cart.query.filter_by(cart_id = cc).first()

    if not cartDetails:
        return '',403

    print("dd")
   
    tamount = cartDetails.total_amount

            # removing from cartProduct table
    db.session.delete(cartprodDetails)
    db.session.commit()

    db.session.delete(cartDetails)
    db.session.commit()

    return str(tamount), 200

   
    
   


# SELLER ENDPOINTS
@app.route('/api/auth/seller/product', methods=['GET'])
@token_required
def getSellerProduct(cu):
    userName = cu.user_name
    userId = cu.user_id
    userRole = cu.user_role
    roleDetails = Role.query.filter_by(role_id=userRole).first()
    roleName = roleDetails.role_name

    if roleName != "SELLER":
        return {}, 403

    res = Product.query.filter_by(seller_id=userId)

    if not res:
        return '', 403

    l = []
    for prod in res:
        prodId = prod.product_id
        cpres = CartProduct.query.filter_by(product_id=prodId).first()
        if cpres:
            prodId = cpres.product_id
            productName = prod.product_name
            pricE = prod.price
            sellerId = prod.seller_id
            categoryId = prod.category_id
            catDetails = Category.query.filter_by(
                category_id=categoryId).first()
            catId = catDetails.category_id
            catName = catDetails.category_name
            d = {}
            prodId = prod.product_id
            d["category"] = {
                "category_name": catName,
                "category_id": catId
            }

            d["price"] = pricE
            d["product_id"] = prodId
            d["product_name"] = productName
            d["seller_id"] = sellerId

            l.append(d)

    return jsonify(l), 200


@app.route('/api/auth/seller/product/<productId>', methods=['GET'])
@token_required
def getOneSellerProduct(cu, productId):

   # incomplete
    print(cu)

    userRole = cu.user_role
    print(userRole)

    roleDetails = Role.query.filter_by(role_id=userRole).first()
    roleName = roleDetails.role_name
  
    if roleName != "SELLER":
        return {}, 403

    res = Product.query.filter_by(product_id=productId).first()

    if not res:
        return '',409

    if not (res.seller_id == cu.user_id):
        return '',404

    pricE = res.price
    sellerId = res.seller_id
    cId = res.category_id
    prodId = res.product_id
    productName=res.product_name

    catDetails = Category.query.filter_by(category_id=cId).first()
    catId = catDetails.category_id
    catName = catDetails.category_name

    l = []

    d = {}

    d["category"] = {

        "category_name": catName,
        "category_id": catId
    }

    d["price"] = pricE

    d["product_id"] = prodId

    d["product_name"] = productName

    d["seller_id"] = sellerId

    l.append(d)

    return jsonify(l), 200


@app.route('/api/auth/seller/product', methods=['POST'])
@token_required
def postSellerProduct(cu):
   
    daata = request.get_json()
    print(daata)
    productId_ = daata['product_id']
    productName_ = daata['product_name']
    price_ = daata['price']
    catId_ = daata['category_id']
   
    userRole = cu.user_role
 
    roleDetails = Role.query.filter_by(role_id=userRole).first()
    roleName = roleDetails.role_name
    roleId = userRole
    print(roleName)

    if roleName != "SELLER":
        return {}, 403

    prod = Product.query.filter_by(product_id=productId_).first()

    if prod:
        return {}, 409

    p = Product(product_id=productId_, product_name=productName_,
                price=price_, category_id=catId_, seller_id=cu.user_id)

    db.session.add(p)
    db.session.commit()

    return str(productId_), 201


@app.route('/api/auth/seller/product', methods=['PUT'])
@token_required
def updateSellerProduct(cu):

    json_data = request.get_json()
    productId_ = json_data['product_id']
    price_ = json_data['price']

    userRole = cu.user_role
    print(userRole)

    roleDetails = Role.query.filter_by(role_id=userRole).first()
    roleName = roleDetails.role_name
    

    if roleName != "SELLER":
        return {}, 403

    prodDetails = Product.query.filter_by(
        product_id=productId_ and Product.seller_id == cu.user_id).first()

    if prodDetails:

        prodDetails.price = price_

        db.session.add(prodDetails)
        db.session.commit()

        return {}, 200

    else:
        return {}, 404


@app.route('/api/auth/seller/product/<int:prodid>', methods=['DELETE'])
@token_required
def deleteSellerProduct(cu,prodid):

   
    productId_ = prodid

    prod = Product.query.filter_by(product_id=productId_).first()
    sellerId = prod.seller_id

    if not prod:
        return {}, 409

    userDetails = User.query.filter_by(user_id=cu.user_id).first()

    if not (userDetails.user_id ==sellerId):
        return '',404
    
    userRole = userDetails.user_role

    roleDetails = Role.query.filter_by(role_id=userRole).first()
    roleName = roleDetails.role_name

    if roleName!="SELLER":
        return '',403

    
    db.session.delete(prod)
    db.session.commit()

    return {}, 200

    


if __name__ == "__main__":
    app.run(debug=True)
