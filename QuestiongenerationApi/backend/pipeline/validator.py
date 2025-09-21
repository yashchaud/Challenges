from backend.utils.qg_model import get_qa_pipeline

def is_echo_response(question, text):
    text_lower = text.lower().strip()
    question_lower = question.lower().strip().replace('?', '').replace('.', '')

    if question_lower == text_lower:
        return True

    if text_lower in question_lower or question_lower in text_lower:
        if len(question_lower) - len(text_lower) < 3:
            return True

    text_words = set(text_lower.split())
    question_words = set(question_lower.split())

    if len(text_words) > 0:
        similarity = len(text_words.intersection(question_words)) / len(text_words)
        if similarity > 0.75:
            return True

    return False

def is_question_relevant(question, text):
    if is_echo_response(question, text):
        return False

    text_lower = text.lower()
    question_lower = question.lower()

    question_words = ['what', 'how', 'why', 'where', 'who', 'when', 'which', 'whose', 'can', 'does', 'is', 'are']
    if not any(question_lower.startswith(word) for word in question_words):
        return False

    if len(question.split()) < 4:
        return False

    words_in_text = set(text_lower.split())
    words_in_question = set(question_lower.replace('?', '').split())

    common_words = words_in_text.intersection(words_in_question)
    if len(common_words) >= 1:
        return True

    return False

def makes_sense(question):
    if not question or len(question.strip()) < 5:
        return False

    question = question.strip()

    bad_patterns = [
        'generate',
        'create question',
        'text:',
        'passage:',
        'following text',
        'based on the'
    ]

    question_lower = question.lower()
    for pattern in bad_patterns:
        if pattern in question_lower:
            return False

    if not question.endswith('?'):
        return False

    if question.count('?') > 1:
        return False

    words = question.split()
    if len(words) < 2:
        return False

    return True

def are_semantically_similar(q1, q2):
    q1_clean = q1.lower().replace('?', '').strip()
    q2_clean = q2.lower().replace('?', '').strip()

    q1_words = set(q1_clean.split())
    q2_words = set(q2_clean.split())

    overlap = len(q1_words.intersection(q2_words)) / max(len(q1_words), len(q2_words))
    return overlap > 0.65

def validate_questions(questions, text):
    good_questions = []
    bad_questions = []

    for question in questions:
        if makes_sense(question) and is_question_relevant(question, text):
       
            is_duplicate = False
            for existing in good_questions:
                if are_semantically_similar(question, existing):
                    is_duplicate = True
                    break

            if not is_duplicate:
                good_questions.append(question)
            else:
                bad_questions.append(question)
        else:
            bad_questions.append(question)

    return good_questions, bad_questions