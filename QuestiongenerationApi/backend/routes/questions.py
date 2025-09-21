from flask import Blueprint, request, jsonify
from backend.utils.qg_model import extract_questions

bp = Blueprint('questions', __name__)

@bp.route('/generate-question', methods=['GET'])
def fetch_questions():
    text = request.args.get('text')

    if not text:
        return jsonify({'error': 'need text parameter'}), 400

    if len(text.strip()) < 5:
        return jsonify({'error': 'text is too short'}), 400

    questions = extract_questions(text)

    if not questions:
        return jsonify({'error': 'couldnt make questions from this text'}), 500

    return jsonify({
        'questions': questions,
        'count': len(questions)
    })