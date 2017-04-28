from flask import Flask, session, redirect, url_for, escape, request

app=Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'



@app.route('/<city>', methods=['GET'])
def cityPage(city):
    return 'city page'

@app.route('/<city>/order', methods=['GET'])
def orderPage(city):
    return 'order page'  

@app.route('/<city>/orders', methods=['GET'])
def ordersPage(city):
    return 'orders page'  

@app.route('/<city>/order', methods=['POST'])
def newOrder(city):
    return 'new order' 

@app.route('/<city>/order/<id>', methods=['GET'])
def getOrderByID(city,id):
    return 'orders page'  

@app.route('/<city>/order/<id>', methods=['PUT'])
def updateOrderByID(city,id):
    return 'update order by ID' 

@app.route('/<city>/order/<id>', methods=['DELETE'])
def delOrderByID(city,id):
    return 'del order by ID' 

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)

