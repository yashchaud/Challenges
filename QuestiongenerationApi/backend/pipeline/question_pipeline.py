from backend.utils.qg_model import get_qa_pipeline
from backend.pipeline.validator import validate_questions

def generate_single_question(text, attempt_num=1, rejected_questions=[]):
    qa_pipe = get_qa_pipeline()
    if qa_pipe is None:
        return None

    try:
        basic_prompts = [
            f"question: {text}",
            f"generate question: {text}",
            f"ask: {text}"
        ]

        alternative_prompts = [
            f"different question: {text}",
            f"another question: {text}",
            f"new question: {text}"
        ]

        follow_up_prompts = [
            f"why question: {text}",
            f"how question: {text}",
            f"what question: {text}"
        ]

        if attempt_num <= 3:
            prompts = basic_prompts
        elif attempt_num <= 7:
            prompts = alternative_prompts
        else:
            prompts = follow_up_prompts

        prompt_idx = (attempt_num - 1) % len(prompts)
        prompt = prompts[prompt_idx]

        temperature = 0.8 + (attempt_num * 0.1)
        if temperature > 1.4:
            temperature = 1.4

        result = qa_pipe(
            prompt,
            max_length=50,
            do_sample=True,
            temperature=temperature,
            num_return_sequences=1
        )

        if result and len(result) > 0:
            question = result[0]['generated_text'].strip()
            if question and len(question) > 5:
                if not question.endswith('?'):
                    question += '?'

                if question not in rejected_questions:
                    return question

        return None
    except Exception as e:
        print(f"error making single question: {e}")
        return None

def get_validated_questions(text, target_count=3, max_attempts=10):
    good_questions = []
    rejected_questions = []
    attempts = 0

    while len(good_questions) < target_count and attempts < max_attempts:
        attempts += 1

        new_question = generate_single_question(text, attempts, rejected_questions)
        if new_question:
            validated_good, validated_bad = validate_questions([new_question], text)

            if validated_good and validated_good[0] not in good_questions:
                good_questions.append(validated_good[0])
                print(f"question {len(good_questions)}: {validated_good[0]}")
            else:
                rejected_questions.append(new_question)
                print(f"attempt {attempts} rejected: {new_question}")

    if len(good_questions) < target_count:
        generic_fallbacks = [
            "What is the main topic?",
            "What information is provided?",
            "What are the key details?",
            "What can be learned from this?",
            "What is being described?",
            "What does this explain?"
        ]

        for fallback in generic_fallbacks:
            if fallback not in good_questions:
                good_questions.append(fallback)
            if len(good_questions) >= target_count:
                break

    return good_questions[:target_count]