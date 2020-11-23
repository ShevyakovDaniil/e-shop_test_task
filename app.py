from flask import Flask, request, jsonify
import pymongo

app = Flask(__name__)
PARAMETERS = {'database': 'e-shop', 'collection': 'product'}


def connection():
    client = pymongo.MongoClient('localhost', 27017)
    return client[PARAMETERS['database']][PARAMETERS['collection']]


def insert_document(collection, data):
    return collection.insert_one(data).inserted_id


def find_document(elements, projection):
    collection = connection()
    results = collection.find(elements, projection)
    return [r for r in results]


@app.route('/create', methods=['GET'])
def create():
    """The function receives as input a set of documents in json format and adds them to the database.
    The output is a list of id of the added documents in json format"""
    response = []
    collection = connection()
    if bool(request.get_json().get('data', '')):
        for element in request.get_json().get('data', ''):
            response.append(insert_document(collection, element))
    return jsonify(str(response))


@app.route('/find_by_id', methods=['GET'])
def find_by_id():
    """The function receives the id of the required document in json format as input.
    Output document details in json format"""
    results = find_document(request.get_json().get('id', ''), {'_id': 0})
    return jsonify(str(results))


@app.route('/find', methods=['GET'])
def find():
    """The function receives search parameters in json format as input.
    Output names and ids of documents in json format"""
    result = find_document(request.get_json().get('elements', ''), {"name": 1, "_id": 1})
    return jsonify(str(result))


if __name__ == '__main__':
    app.run()
