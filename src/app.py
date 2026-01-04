"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"msg": "Miembro no encontrado"}), 400

@app.route('/members', methods=['POST'])
def create_member():
    new_member_data = request.get_json()
    
    if not new_member_data:
         return jsonify({"msg": "Debes enviar datos en el body"}), 400

    member_created = jackson_family.add_member(new_member_data)
    
    return jsonify(member_created), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    eliminated = jackson_family.delete_member(member_id)
    
    if eliminated:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"msg": "No se encontró el miembro para eliminar"}), 400

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)