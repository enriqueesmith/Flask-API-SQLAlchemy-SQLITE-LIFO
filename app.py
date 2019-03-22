import os
from flask import Flask, jsonify, request
import sqlalchemy 
from flask_migrate import Migrate
from models import db, Item
from sqlalchemy import desc
  
app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/change_this_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)

  
@app.route('/')
def hello():
    items = Item.query.all()
    response =[]
    for i in items:
        response.append("%s" % i)
        
    return jsonify(response)
    
@app.route('/add', methods=['POST'])
def add():
    info = request.get_json() or {}
    item = Item(text=info['text'])
    db.session.add(item)
    db.session.commit()
    return jsonify({'response': 'ok'})
    
@app.route('/lifo-pop', methods=['GET'])
def pop():
    last = Item.query.order_by(desc(Item.created_on)).first()
    if last is not None:
        db.session.delete(last)
        db.session.commit()
    return jsonify({"deleted": "%s" % last})
    
@app.route('/delete-all', methods=['GET'])
def deleteAll():
    items = Item.query.all()
    for i in items:
        db.session.delete(i)
        db.session.commit()
    return jsonify({'deleted': '%s' % items})
  
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))