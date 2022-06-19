from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
from functools import wraps

from numpy import product


app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///practice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '12345'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        print(request.headers['x-access-token'])

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        #payload= jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])

        #data = jwt.decode(token, app.config['SECRET_KEY'])
        try:
            payload = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])

        except:
            return jsonify({'Alert': 'Invalid Token'})
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    return "Wassup", 200

# public endpoints api/public/product/search?keyword="crocin"
# accessing through query parameters


@app.route('/api/public/product/search', methods=['GET'])
def getProducts():

    prod = (request.args.get('keyword'))
    prod.strip()

    rq = prod.replace('"', '')

    res = db.session.query(Product).join(Category).filter(
        Product.product_name == rq).first()

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

# remove get


@app.route('/api/public/login', methods=['POST', 'GET'])
def login():
    print("------------------>", request.get_json())
    json_data = request.get_json()
    userName_ = json_data["user_name"]
    passWord_ = json_data["password"]
    print("------------------>", userName_, "---------->", passWord_)
    user1 = User.query.filter_by(user_name=userName_).first()
    if user1:

        if user1.password == passWord_:

            token = jwt.encode({
                'user': userName_,
                'expiration': str(datetime.utcnow() + timedelta(minutes=30))

            }, app.config['SECRET_KEY'])
            #

            # return jsonify({'token':token.decode('utf-8')})
            return token, 200
        else:
            return {}, 401
    else:
        return {}, 401

# authentication endpoints
# api/auth/consumer/cart?"JWT"=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiamFjayIsImV4cGlyYXRpb24iOiIyMDIyLTA2LTE5IDA2OjMwOjI1Ljg5NTA4MiJ9.ZJob2W1Lloe2SIj2e7713vJEO-m8e6EboomeF7iEajI


@app.route('/api/auth/consumer/cart', methods=['GET'])
@token_required
def consumerCart():
    print("------------------------------::::::", "HELLO!!!!")
    res = db.session.query(CartProduct).join(Product).join(
        Cart).join(Category).filter(Cart.user_id == 1).first()
    print(res)

    cpId = res.cp_id
    cartId = res.cart_id
    prodId = res.product_id

    print(res.product_id)

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

    l = []

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

    return jsonify(l), 200


@app.route('/api/auth/consumer/cart', methods=['POST'])
@token_required
def postConsumerCart():

    prodId = request.get_json()["product_id"]
    quantity = request.get_json()["quantity"]

    return 'HEY THERE'


@app.route('/api/auth/consumer/cart', methods=['PUT'])
@token_required
def updateConsumerCart():
    json_data = request.get_json()
    productId = json_data['product_id']
    quantity = json_data['quantity']

    return 'HEY THERE'


@app.route('/api/auth/consumer/cart', methods=['DELETE'])
@token_required
def deleteConsumerCart():
    json_data = request.get_json()
    productId = json_data['product_id']

    return 'HEY THERE'

# SELLER ENDPOINTS


@app.route('/api/auth/seller/product', methods=['GET'])
@token_required
def getSellerProduct():

    res = db.session.query(CartProduct).join(Product).join(
        Cart).join(Category).filter(Cart.user_id == 5).first()
    print(res)

    cpId = res.cp_id
    cartId = res.cart_id
    prodId = res.product_id

    print(res.product_id)

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

    l = []

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

    return jsonify(l)

    return 'HEY THERE'


@app.route('/api/auth/consumer/product/<int:productId>', methods=['GET'])
@token_required
def getOneSellerProduct():

    return 'HEY THERE'

# working but jwt has to be verified


@app.route('/api/auth/seller/product', methods=['POST'])
@token_required
def postSellerProduct():

    json_data = request.get_json()
    productId_ = json_data['product_id']
    productName_ = json_data['product_name']
    price_ = json_data['price']
    category_ = json_data['category_id']

    p = Product.query.filter_by(product_id=productId_).first()

    if p:
        return jsonify(409)

    '''
    new_prod=Product(product_id=productId_, 
    
    
    _name=productName_,price=price_,
    category_id=category_)

    db.session.add(new_prod)
    db.session.commit()
    '''
    return jsonify(productId_)


@app.route('/api/auth/seller/product', methods=['PUT'])
@token_required
def updateSellerProduct():

    json_data = request.get_json()
    productId_ = json_data['product_id']

    price_ = json_data['price']

    return 'HEY THERE'


@app.route('/api/auth/seller/product/<int:prodid>', methods=['DELETE'])
@token_required
def deleteSellerProduct():

    todo = Product.query.get_or_404(int(id))
    db.session.delete(todo)
    db.session.commit()

    return jsonify({"Success": "Todo deleted."})


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


if __name__ == "__main__":
    app.run(debug=True)
