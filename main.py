from email import message
from flask import *
from flask_cors import CORS, cross_origin
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

my_client = pymongo.MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))

app = Flask(__name__) 
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000/"}})

@app.route('/', methods=['GET']) 
@cross_origin()
def home():  
    db = my_client['Meeting-Organizer']
    meets = db["Meet"]
    
    all_meets = dumps(meets.find({}))

    return jsonify(
        all_meets
    )

@app.route('/add-meet', methods=['POST'])
@cross_origin() 
def add_meet():  
    request_parameters = request.json
    
    db = my_client['Meeting-Organizer']
    meet = db["Meet"]
    
    meet_to_insert = { 
        "topic_of_meet": request_parameters["meet"]["topic_of_meet"],
        "date": request_parameters["meet"]["date"],
        "start_time": request_parameters["meet"]["start_time"],
        "finish_time": request_parameters["meet"]["finish_time"],
        "participants": request_parameters["meet"]["participants"] 
    }

    meet.insert_one(meet_to_insert)
    return jsonify(
        message= "Toplantı Başarıyla Kaydedildi."
    )
  
@app.route('/edit-meet', methods=['PUT'])
@cross_origin()
def edit_meet():      
    request_parameters = request.json

    db = my_client['Meeting-Organizer']
    meets = db["Meet"]
    
    meet = meets.update_one({'_id': ObjectId(request_parameters["meet"]["id"])}, 
                                     {"$set": {
                                        "topic_of_meet": request_parameters["meet"]["topic_of_meet"],
                                        "date": request_parameters["meet"]["date"],
                                        "start_time": request_parameters["meet"]["start_time"],
                                        "finish_time": request_parameters["meet"]["finish_time"],
                                        "participants": request_parameters["meet"]["participants"] 
                                     }}, upsert=True)
    
    return jsonify(
        message= "Veri Güncellendi."
    )
  
@app.route('/edit-meet/<meet_id>', methods=['GET'])
@cross_origin()
def get_meet(meet_id):      
    db = my_client['Meeting-Organizer']
    meets = db["Meet"]
    
    meet = dumps(meets.find_one({'_id': ObjectId(meet_id)}))
    
    return jsonify(
        message = meet
    )

@app.route('/delete-meet', methods=['POST'])
@cross_origin()
def delete_meet():  
    request_parameters = request.json
    
    db = my_client['Meeting-Organizer']
    meet = db["Meet"]
    
    meet_to_delete = { 
        "_id":  ObjectId(request_parameters["meet"]["id"]),
    }

    meet.delete_one(meet_to_delete)

    return jsonify(
        message= "Toplantı Başarıyla Silindi."
    )
