from flask import Flask, session, redirect, url_for, escape, request
#from flask_pymongo import PyMongo
from bson import Binary, Code
from bson.json_util import dumps
import json
from pymongo import MongoClient
from pymongo import ReturnDocument
import urlparse
from urllib import urlencode
client = MongoClient()

app=Flask(__name__)
#
# mongo init
#app.config.update(
#    MONGO_URI='mongodb://localhost:27017/cmpe281',
#    MONGO_TEST_URI='mongodb://localhost:27017/test'
#)
#mongo = PyMongo(app)
client = MongoClient('localhost', 27017)
db = client.cmpe281
collection = db.orders
currentID = db.currentID
@app.route('/',methods=['GET'])
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'
 


@app.route('/<city>', methods=['GET'])
def cityPage(city):
    return 'city page'

@app.route('/<city>/orders', methods=['GET'])
def ordersPage(city):
    # get all orders
    result=collection.find({},{'_id':0})
    return dumps(result)

@app.route('/<city>/order', methods=['POST'])
def createOrder(city):
    # req new post from front end
    post = request.get_json()
    print "> get Post: "+json.dumps(post)
    # convert to json
    order = json.loads(json.dumps(post))
    #create new id and save id for this new order
    currend_id=currentID.find_one_and_update({},{'$inc':{'currentID':int(1)}},upsert=True,return_document=ReturnDocument.AFTER)
    oldID = json.loads(dumps(currend_id))['currentID']
    print "> current ID: " + str(oldID)

    #set up all infos
    thisId =int(oldID)
    name =order['name']
    ice = order['ice']
    size   =order['size']
    price   =order['price']
    number  =order['number']
  
    # setup json
    newOrder = {'id': thisId,'name':name,'ice':ice, 'size':size, 'price': price,'number':number}
    #insert into mongodb
    result = collection.insert_one(newOrder)
    return "goog"

@app.route('/<city>/order/<int:id>', methods=['GET'])
def getOrderByID(city,id):
    #print "got id:" + id
    
    task = collection.find_one({"id":id},{'_id':0})
    print "> get order by id: " + str(task)
    #return 'orders page'  
    return json.dumps(task)


@app.route('/<city>/order/<int:id>', methods=['PUT'])
def updateOrderByID(city,id):
    # req new post from front end
    post = request.get_json()
    print "> get Update: "+str(id)
    print ">             "+json.dumps(post)
    # convert to json
    order = json.loads(json.dumps(post))
    # get order id
    thisId = id
    name =order['name']
    ice = order['ice']
    size   =order['size']
    price   =order['price']
    number  =order['number']
    updateOrder = {'id':id,'name':name,'ice':ice, 'size':size, 'price': price,'number':number}
    result = collection.find_one_and_update({'id':id},{'$set':updateOrder},return_document=ReturnDocument.AFTER)
    returnVal=json.loads(dumps(result))
    return  json.dumps(returnVal)  # when ==1 then successful update
    

@app.route('/<city>/order/<int:id>', methods=['DELETE'])
def delOrderByID(city,id):
    result = collection.find_one_and_delete({'id':id},{'_id':0})
    returnVal =json.loads(dumps(result))
    print "> delete order by id: " + str(returnVal)
    return json.dumps(returnVal)

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)

