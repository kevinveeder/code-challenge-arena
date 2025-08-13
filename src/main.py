#!/usr/bin/env python3

from game_engine import GameEngine
from ui import GameUI
from challenges_data import get_all_challenges

class Game:
    def __init__(self):
        # Set up the main game components
        self.engine = GameEngine()
        self.ui = GameUI()
        self.running = True
        
        # Load all the challenges into our game engine
        for challenge in get_all_challenges():
            self.engine.add_challenge(challenge)
    
    def run(self):
        # Main game loop - keep going until player quits
        self.ui.clear_screen()
        self.ui.print_header()
        
        while self.running:
            self.show_main_menu()
    
    def show_main_menu(self):
        # Handle the main menu interactions
        self.ui.show_main_menu()
        choice = self.ui.get_user_choice(4)
        
        if choice == 1:
            self.start_challenge()
        elif choice == 2:
            self.show_progress()
        elif choice == 3:
            self.show_categories()
        elif choice == 4:
            self.quit_game()
        elif choice is None:  # Ctrl+C handling
            self.quit_game()
    
    def start_challenge(self):
        # Let player pick and attempt a challenge
        available_challenges = self.engine.get_available_challenges()
        
        if not available_challenges:
            self.ui.show_challenges(available_challenges)
            self.ui.pause()
            return
        
        self.ui.clear_screen()
        self.ui.print_header()
        self.ui.show_challenges(available_challenges)
        
        print(f"\nChoose a challenge (1-{len(available_challenges)}) or 0 to go back: ", end="")
        choice = self.ui.get_user_choice(len(available_challenges))
        
        if choice is None or choice == 0:
            return
        
        # Start the selected challenge
        selected_challenge = available_challenges[choice - 1]
        self.play_challenge(selected_challenge)
    
    def play_challenge(self, challenge):
        # Handle the actual challenge gameplay
        challenge.start()
        self.ui.show_challenge_details(challenge)
        
        while True:
            user_input = self.ui.get_user_code()
            
            if user_input == 'QUIT':
                break
            elif user_input == 'HINT':
                hint = challenge.get_hint()
                self.ui.show_hint(hint)
                continue
            
            # Check if their solution is correct
            success, message = challenge.check_solution(user_input)
            
            if success:
                # They got it right! Award points and mark complete
                score = self.engine.complete_challenge(challenge)
                self.ui.show_result(True, message, score)
                
                # Check if they unlocked anything new
                self.check_for_unlocks()
                self.ui.pause()
                break
            else:
                # Not quite right, let them try again
                self.ui.show_result(False, message)
                print("\nTry again, or type QUIT to return to menu.")
    
    def check_for_unlocks(self):
        # See if player unlocked new categories and let them know
        stats = self.engine.get_player_stats()
        current_level = stats['level']
        
        # This is a simple way to show level up messages
        # In a real game might want to track this better
        if current_level > 1:
            print(f"\nYou're now level {current_level}! Keep up the great work!")
    
    def show_progress(self):
        # Display current player stats
        self.ui.clear_screen()
        self.ui.print_header()
        stats = self.engine.get_player_stats()
        self.ui.show_progress(stats)
        self.ui.pause()
    
    def show_categories(self):
        # Show what challenge categories are available
        self.ui.clear_screen()
        self.ui.print_header()
        stats = self.engine.get_player_stats()
        
        print("\nChallenge Categories:")
        print("=" * 30)
        
        all_categories = {
            "basics": "Fundamentals - Variables, loops, basic syntax",
            "data_structures": "Lists, dictionaries, and data manipulation", 
            "algorithms": "Sorting, searching, and algorithmic thinking",
            "problem_solving": "Real-world coding challenges",
            "debugging": "Find and fix broken code",
            "leetcode_style": "Classic interview questions and LeetCode problems"
        }
        
        for category, description in all_categories.items():
            if category in stats['unlocked_categories']:
                print(f"✓ {category.replace('_', ' ').title()}: {description}")
            else:
                print(f"🔒 {category.replace('_', ' ').title()}: {description} (Locked)")
        
        self.ui.pause()
    
    def quit_game(self):
        # Clean exit from the game
        print(f"\nThanks for playing Code Challenge Arena!")
        print("Keep practicing and you'll be a coding master in no time!")
        self.running = False

def main():
    # Entry point - start up the game
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\nThanks for playing!")
    except Exception as e:
        print(f"Oops, something went wrong: {e}")
        print("Please report this bug so I can fix it!")

if __name__ == "__main__":
    main()