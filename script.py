from email import message
from flask import *
from flask_cors import CORS, cross_origin, crossdomain
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

my_client = pymongo.MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))

app = Flask(__name__) #creating the Flask class object   
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET']) #decorator drfines the   
def home():  
    db = my_client['Meeting-Organizer']
    meets = db["Meet"]
    
    all_meets = dumps(meets.find({}))

    return jsonify(
        all_meets
    )

@app.route('/add-meet', methods=['POST']) #decorator drfines the   
def add_meet():  
    request_parameters = request.json
    
    db = my_client['Meeting-Organizer']
    meet = db["Meet"]
    
    print(request_parameters)

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
  
@app.route('/edit-meet', methods=['PUT']) #decorator drfines the   
def edit_meet():      
    request_parameters = request.json

    print(request_parameters)

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

    print(meet)
    
    return jsonify(
        message= "Veri Güncellendi."
    )
  
@app.route('/edit-meet/<meet_id>', methods=['GET']) #decorator drfines the   
def get_meet(meet_id):      
    db = my_client['Meeting-Organizer']
    meets = db["Meet"]
    
    meet = dumps(meets.find_one({'_id': ObjectId(meet_id)}))
    
    return jsonify(
        message = meet
    )

@app.route('/delete-meet', methods=['POST']) #decorator drfines the   
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

if __name__ =='__main__':  
    app.run(debug = True)  