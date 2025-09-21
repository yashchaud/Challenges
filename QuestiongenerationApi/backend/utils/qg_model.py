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
    try:
        from backend.pipeline.question_pipeline import get_validated_questions
        return get_validated_questions(text, target_count=3)
    except Exception as e:
        print(f"pipeline failed, using fallback: {e}")
        return ["What is this about?", "Can you explain this topic?", "What are the main points here?"]