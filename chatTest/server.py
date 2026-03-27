from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import uuid

app = Flask(__name__)
CORS(app)

DATA_DIR = 'data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/room/<room_id>', methods=['GET'])
def get_room(room_id):
    file_path = os.path.join(DATA_DIR, f'{room_id}.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({'success': True, 'data': data})
    else:
        return jsonify({'success': False, 'message': '房间不存在'})

@app.route('/api/room', methods=['POST'])
def create_room():
    room_id = str(uuid.uuid4())[:8]
    data = request.json
    
    file_path = os.path.join(DATA_DIR, f'{room_id}.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return jsonify({'success': True, 'room_id': room_id})

@app.route('/api/room/<room_id>', methods=['PUT'])
def update_room(room_id):
    data = request.json
    
    file_path = os.path.join(DATA_DIR, f'{room_id}.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
