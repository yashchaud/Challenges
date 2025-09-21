from transformers import pipeline
import os

model_cache = None

def get_qa_pipeline():
    global model_cache
    if model_cache is None:
        try:
            print("loading model...")
            os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

            model_cache = pipeline(
                "text2text-generation",
                model="google/flan-t5-base",
                device=-1
            )
            print("model ready")
        except Exception as e:
            print(f"cant load model: {e}")
            return None
    return model_cache

def extract_questions(text):
    qa_pipe = get_qa_pipeline()
    if qa_pipe is None:
        return ["What is this about?", "Can you explain this topic?", "What are the main points here?"]

    try:
        prompts = [
        f"Generate a clear, fact-based question whose answer can be found in the following text:\n\n{text}\n\nQuestion:",
        f"Based only on the text below, create a single relevant question that tests comprehension:\n\n{text}\n\nQuestion:",
        f"Write one concise question that can be answered directly from this passage:\n\n{text}\n\nQuestion:",
        f"From the text provided, formulate a meaningful question (avoid yes/no, prefer informative):\n\n{text}\n\nQuestion:"
        ]


        questions = []
        for prompt in prompts:
            result = qa_pipe(prompt, max_length=100, do_sample=True, temperature=0.8)
            if result and len(result) > 0:
                question = result[0]['generated_text'].strip()
                if question and len(question) > 5:
                    if not question.endswith('?'):
                        question += '?'
                    if question not in questions:
                        questions.append(question)

            if len(questions) >= 3:
                break

        if len(questions) < 3:
            fallback_questions = [
                "What is this about?",
                "Can you explain this topic?",
                "What are the main points here?"
            ]
            for fallback in fallback_questions:
                if fallback not in questions:
                    questions.append(fallback)
                if len(questions) >= 3:
                    break

        return questions[:3]
    except Exception as e:
        print(f"error making questions: {e}")
        return ["What is this about?", "Can you explain this topic?", "What are the main points here?"]