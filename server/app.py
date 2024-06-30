from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        body = request.form.get('body')
        username = request.form.get('username')
        message = Message(body=body, username=username)
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 201
    else:
        messages = Message.query.all()
        return jsonify([message.to_dict() for message in messages])

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    if message:
        if request.method == 'PATCH':
            body = request.form.get('body')
            username = request.form.get('username')
            if body:
                message.body = body
            if username:
                message.username = username
            db.session.commit()
            return jsonify(message.to_dict())
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()
            return jsonify({'message': 'Message deleted successfully'}), 200
        else:
            return jsonify(message.to_dict())
    else:
        return jsonify({'error': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(port=5555)
