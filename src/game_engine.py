from typing import Dict, List
import json
import os
from challenge import Challenge, Category, Difficulty

class GameEngine:
    def __init__(self):
        # Set up the main game state - keeping track of all challenges and player data
        self.challenges: Dict[str, Challenge] = {}
        self.player_progress = {
            "score": 0,
            "completed_challenges": [],
            "unlocked_categories": [Category.BASICS.value],  # Everyone starts with basics
            "current_level": 1
        }
        self.load_progress()
        
    def load_progress(self):
        # Try to load existing save data if it exists
        progress_file = "player_progress.json"
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                self.player_progress = json.load(f)
                
    def save_progress(self):
        # Write current progress to disk so we don't lose it
        with open("player_progress.json", 'w') as f:
            json.dump(self.player_progress, f, indent=2)
            
    def add_challenge(self, challenge: Challenge):
        # Register a new challenge in our system
        self.challenges[challenge.id] = challenge
        
    def get_available_challenges(self) -> List[Challenge]:
        # Only show challenges the player has unlocked and hasn't completed yet
        available = []
        for challenge in self.challenges.values():
            if (challenge.category.value in self.player_progress["unlocked_categories"] and
                challenge.id not in self.player_progress["completed_challenges"]):
                available.append(challenge)
        return available
        
    def complete_challenge(self, challenge: Challenge) -> int:
        # Handle when player finishes a challenge - award points and check for unlocks
        score = challenge.calculate_score()
        self.player_progress["score"] += score
        self.player_progress["completed_challenges"].append(challenge.id)
        
        # See if they leveled up or unlocked new stuff
        self._check_progression()
        self.save_progress()
        
        return score
        
    def _check_progression(self):
        # Figure out if player should level up based on completed challenges
        completed_count = len(self.player_progress["completed_challenges"])
        new_level = completed_count // 3 + 1  # Level up every 3 challenges
        
        if new_level > self.player_progress["current_level"]:
            self.player_progress["current_level"] = new_level
            
            # Unlock new categories as player progresses - don't want to overwhelm beginners
            if new_level >= 2 and Category.DATA_STRUCTURES.value not in self.player_progress["unlocked_categories"]:
                self.player_progress["unlocked_categories"].append(Category.DATA_STRUCTURES.value)
            if new_level >= 4 and Category.ALGORITHMS.value not in self.player_progress["unlocked_categories"]:
                self.player_progress["unlocked_categories"].append(Category.ALGORITHMS.value)
            if new_level >= 6 and Category.PROBLEM_SOLVING.value not in self.player_progress["unlocked_categories"]:
                self.player_progress["unlocked_categories"].append(Category.PROBLEM_SOLVING.value)
            if new_level >= 8 and Category.DEBUGGING.value not in self.player_progress["unlocked_categories"]:
                self.player_progress["unlocked_categories"].append(Category.DEBUGGING.value)
            if new_level >= 10 and Category.LEETCODE.value not in self.player_progress["unlocked_categories"]:
                self.player_progress["unlocked_categories"].append(Category.LEETCODE.value)
                
    def get_player_stats(self) -> Dict:
        # Return current player info for display
        return {
            "level": self.player_progress["current_level"],
            "score": self.player_progress["score"],
            "completed": len(self.player_progress["completed_challenges"]),
            "unlocked_categories": self.player_progress["unlocked_categories"]
        }