"""
MODULE: Question System (Hệ Thống Câu Hỏi)
Quản lý câu hỏi Python và hệ thống kiểm tra
"""
import random

QUESTIONS_DB = {
    'basic': [
        ("2 + 2", "4"),
        ("len('hello')", "5"),
        ("3 * 4", "12"),
        ("abs(-7)", "7"),
        ("10 - 5", "5"),
        ("20 / 4", "5"),
        ("2 ** 3", "8"),
    ],
    'intermediate': [
        ("max(1, 5, 3)", "5"),
        ("min(10, 3, 7)", "3"),
        ("int('42')", "42"),
        ("str(123)", "123"),
        ("5 % 3", "2"),
        ("10 ** 2", "100"),
    ],
    'advanced': [
        ("len([1,2,3,4])", "4"),
        ("'hello'.upper()", "HELLO"),
        ("sum([1,2,3])", "6"),
        ("sorted([3,1,2])", "[1, 2, 3]"),
    ]
}

class QuestionSystem:
    """Hệ thống quản lý câu hỏi"""
    
    def __init__(self):
        self.current_question = None
        self.correct_answer = None
        self.user_answer = ""
    
    def get_question(self, difficulty="Normal"):
        """Lấy câu hỏi theo mức độ khó"""
        if difficulty in ("Hard", "Insane"):
            pool = QUESTIONS_DB['advanced'] + QUESTIONS_DB['intermediate']
        elif difficulty == "Easy":
            pool = QUESTIONS_DB['basic']
        else:  # Normal
            pool = QUESTIONS_DB['basic'] + QUESTIONS_DB['intermediate']
        
        question, answer = random.choice(pool)
        self.current_question = question
        self.correct_answer = answer
        self.user_answer = ""
        
        return question
    
    def add_character(self, char):
        """Thêm ký tự vào câu trả lời"""
        if len(self.user_answer) < 50:
            self.user_answer += char
    
    def remove_character(self):
        """Xóa ký tự cuối cùng"""
        self.user_answer = self.user_answer[:-1]
    
    def check_answer(self):
        """Kiểm tra câu trả lời"""
        return self.user_answer.strip() == self.correct_answer
    
    def get_display_question(self):
        """Lấy text để hiển thị câu hỏi"""
        if self.current_question:
            return f"{self.current_question} = ?"
        return ""
    
    def get_display_answer(self):
        """Lấy text để hiển thị câu trả lời"""
        return f"Câu trả lời: {self.user_answer}"
    
    def reset(self):
        """Đặt lại hệ thống"""
        self.current_question = None
        self.correct_answer = None
        self.user_answer = ""
