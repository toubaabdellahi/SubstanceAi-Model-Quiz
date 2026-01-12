import fitz
import json
from mistralai import Mistral

class QuizEngine:
    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)

        self.quiz_storage = {
            "questions": [],
            "current_idx": 0,
            "score": 0,
            "user_history": []
        }

    def start_quiz(self, pdf_path: str):
        # 1. Extraction texte
        doc = fitz.open(pdf_path)
        text = "".join([page.get_text() for page in doc])[:12000]

        # 2. Prompt Mistral (IDENTIQUE à ton code)
        prompt = (
            "Génère un quiz JSON de 5 questions sur ce texte : "
            f"{text}. "
            "Structure: {'questions': "
            "[{'question': '...', 'options': ['...', '...', '...', '...'], "
            "'correct_index': 0, 'explanation': '...'}]}"
        )

        res = self.client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        data = json.loads(res.choices[0].message.content)

        self.quiz_storage["questions"] = data["questions"]
        self.quiz_storage["current_idx"] = 0
        self.quiz_storage["score"] = 0
        self.quiz_storage["user_history"] = []

        return self._get_current_question()

    def answer_question(self, user_choice: int):
        q = self.quiz_storage["questions"][self.quiz_storage["current_idx"]]
        is_correct = user_choice == q["correct_index"]

        if is_correct:
            self.quiz_storage["score"] += 1

        self.quiz_storage["user_history"].append({
            "question": q["question"],
            "user_ans": q["options"][user_choice],
            "correct_ans": q["options"][q["correct_index"]],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

        self.quiz_storage["current_idx"] += 1

        # FIN DU QUIZ
        if self.quiz_storage["current_idx"] >= len(self.quiz_storage["questions"]):
            return {"finished": True, "result": self._build_summary()}

        return {"finished": False, "question": self._get_current_question()}

    def _get_current_question(self):
        q = self.quiz_storage["questions"][self.quiz_storage["current_idx"]]
        return {
            "index": self.quiz_storage["current_idx"] + 1,
            "question": q["question"],
            "options": q["options"]
        }

    def _build_summary(self):
        return {
            "score": self.quiz_storage["score"],
            "total": len(self.quiz_storage["questions"]),
            "details": self.quiz_storage["user_history"]
        }
