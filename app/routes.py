# app/routes.py

from flask import Blueprint, render_template, request, jsonify, current_app
from app import db
from app.models import User
from app.utills import extract_img_from_pdf, extract_text_from_pdf

from werkzeug.utils import secure_filename
import os

bp = Blueprint('main', __name__)

@bp.route('/upload/<int:id>', methods=['GET'])
def upload_template(id):
    user = User.query.get_or_404(id)
    return render_template('upload_file.html', user_id=user.id)

# Route to handle file upload
@bp.route('/upload/<int:id>', methods=['POST'])
def upload_file(id):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Update user information
        user = User.query.get_or_404(id)
        user.pdf_file = filepath
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully'}), 201
    return jsonify({'error': 'File type not allowed'}), 400

@bp.route('/extract_text/<int:id>', methods=['GET'])
def extract_text(id):
    user = User.query.get_or_404(id)
    if not user.pdf_file:
        return jsonify({'error': 'No PDF file uploaded for this user'}), 400

    image_b64_list, texts = extract_img_from_pdf(user.pdf_file)
    text_data = extract_text_from_pdf(user.pdf_file)



    return render_template('display.html', images=image_b64_list, texts=texts, text_data=text_data)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        sent_mails=data['sent_mails'],
        activity_time=data['activity_time'],
        status=data['status']
    )
    db.session.add(new_user)
    db.session.commit()



    return jsonify({'message': 'User created successfully'}), 201


@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'sent_mails': user.sent_mails,
            'activity_time': user.activity_time,
            'status': user.status
        })
    return jsonify(users_list), 200


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'sent_mails': user.sent_mails,
        'activity_time': user.activity_time,
        'status': user.status
    }
    return jsonify(user_data), 200


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.sent_mails = data.get('sent_mails', user.sent_mails)
    user.activity_time = data.get('activity_time', user.activity_time)
    user.status = data.get('status', user.status)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


@bp.route('/', methods=['GET', 'POST'])
def dashboard():
    query = request.form.get('search') if request.method == 'POST' else ''
    date_range = request.form.get('date_range') if request.method == 'POST' else 'Last 30 days'

    # Filter users based on the search query
    filtered_users = User.query.filter(User.username.ilike(f"%{query}%")).all()

    return render_template('dashboard.html', users=filtered_users, query=query, date_range=date_range)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']