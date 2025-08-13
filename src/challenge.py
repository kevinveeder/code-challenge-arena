from typing import Dict, List, Callable, Any
from enum import Enum
import time

# Setting up the difficulty and category enums to organize challenges
class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4

class Category(Enum):
    BASICS = "basics"
    DATA_STRUCTURES = "data_structures"
    ALGORITHMS = "algorithms"
    PROBLEM_SOLVING = "problem_solving"
    DEBUGGING = "debugging"
    LEETCODE = "leetcode_style"

class Challenge:
    def __init__(self, id: str, title: str, description: str, category: Category, 
                 difficulty: Difficulty, solution_checker: Callable, hints: List[str] = None, 
                 expected_answer: str = None):
        # Basic challenge info
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.difficulty = difficulty
        self.solution_checker = solution_checker  # Function that validates user's solution
        self.hints = hints or []
        self.expected_answer = expected_answer  # What the correct solution should look like
        
        # Tracking stuff for scoring and attempts
        self.start_time = None
        self.hints_used = 0
        self.attempts = 0
        
    def start(self):
        # Mark when the challenge started for time tracking
        self.start_time = time.time()
        
    def get_hint(self) -> str:
        # Give player a hint if any are left
        if self.hints_used < len(self.hints):
            hint = self.hints[self.hints_used]
            self.hints_used += 1
            return hint
        return "No more hints available!"
        
    def check_solution(self, user_code: str) -> tuple[bool, str]:
        # Run the user's code through our checker function
        self.attempts += 1
        try:
            success, message = self.solution_checker(user_code)
            
            # If they failed and this is their 3rd attempt, show the expected answer
            if not success and self.attempts >= 3 and self.expected_answer:
                message += f"\n\nAfter 3 attempts, here's the expected solution:\n{self.expected_answer}"
            
            return success, message
        except Exception as e:
            error_msg = f"Error running your code: {e}"
            
            # Show expected answer after 3 failed attempts
            if self.attempts >= 3 and self.expected_answer:
                error_msg += f"\n\nAfter 3 attempts, here's the expected solution:\n{self.expected_answer}"
            
            return False, error_msg
            
    def get_time_taken(self) -> float:
        # Calculate how long they've been working on this
        if self.start_time:
            return time.time() - self.start_time
        return 0.0
        
    def calculate_score(self) -> int:
        # Score based on difficulty, time, and hints used
        base_score = self.difficulty.value * 100
        time_taken = self.get_time_taken()
        
        # Faster completion gives bonus points
        time_bonus = max(0, 50 - int(time_taken / 10))
        
        # Using hints reduces score
        hint_penalty = self.hints_used * 10
        
        # Make sure they always get some points
        return max(10, base_score + time_bonus - hint_penalty)