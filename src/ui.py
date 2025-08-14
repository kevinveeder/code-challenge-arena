import os
from typing import List
from colorama import init, Fore, Back, Style
from challenge import Challenge, Category, Difficulty

# Initialize colorama for cross-platform colored output
init()

class GameUI:
    def __init__(self):
        # Set up colors and styling for better user experience
        self.colors = {
            'header': Fore.CYAN + Style.BRIGHT,
            'success': Fore.GREEN + Style.BRIGHT,
            'error': Fore.RED + Style.BRIGHT,
            'warning': Fore.YELLOW + Style.BRIGHT,
            'info': Fore.BLUE,
            'reset': Style.RESET_ALL
        }
    
    def clear_screen(self):
        # Clear terminal for cleaner display
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        # Main game title and branding
        print(f"\n{self.colors['header']}")
        print("=" * 50)
        print("     CODE CHALLENGE ARENA")
        print("   Level up your coding skills!")
        print("=" * 50)
        print(f"{self.colors['reset']}")
    
    def show_main_menu(self):
        # Display the main menu options
        print(f"\n{self.colors['info']}What would you like to do?{self.colors['reset']}")
        print("1. Start a challenge")
        print("2. View your progress")
        print("3. View available categories")
        print("4. Quit")
        print(f"\n{self.colors['warning']}Enter your choice (1-4): {self.colors['reset']}", end="")
    
    def show_challenges(self, challenges: List[Challenge]):
        # Display available challenges in a nice format
        if not challenges:
            print(f"\n{self.colors['warning']}No challenges available right now!{self.colors['reset']}")
            return
        
        print(f"\n{self.colors['header']}Available Challenges:{self.colors['reset']}")
        print("-" * 40)
        
        for i, challenge in enumerate(challenges, 1):
            # Color code by difficulty
            difficulty_color = self._get_difficulty_color(challenge.difficulty)
            print(f"{i}. {challenge.title}")
            print(f"   Category: {challenge.category.value.replace('_', ' ').title()}")
            print(f"   Difficulty: {difficulty_color}{challenge.difficulty.name}{self.colors['reset']}")
            print(f"   {challenge.description[:60]}...")
            print()
    
    def _get_difficulty_color(self, difficulty: Difficulty):
        # Return appropriate color for each difficulty level
        colors = {
            Difficulty.EASY: self.colors['success'],
            Difficulty.MEDIUM: self.colors['warning'],
            Difficulty.HARD: Fore.MAGENTA,
            Difficulty.EXPERT: self.colors['error']
        }
        return colors.get(difficulty, self.colors['reset'])
    
    def show_challenge_details(self, challenge: Challenge):
        # Show full challenge description and rules
        self.clear_screen()
        print(f"\n{self.colors['header']}Challenge: {challenge.title}{self.colors['reset']}")
        print("=" * 50)
        print(f"\nCategory: {challenge.category.value.replace('_', ' ').title()}")
        difficulty_color = self._get_difficulty_color(challenge.difficulty)
        print(f"Difficulty: {difficulty_color}{challenge.difficulty.name}{self.colors['reset']}")
        print(f"\nDescription:")
        print(challenge.description)
        print(f"\n{self.colors['info']}Available hints: {len(challenge.hints)}{self.colors['reset']}")
        print(f"\n{self.colors['warning']}HOW TO SUBMIT:{self.colors['reset']}")
        print("1. Type your Python code (multiple lines allowed)")
        print("2. When done, press Enter to go to a new line")
        print(f"3. Type {self.colors['success']}SUBMIT{self.colors['reset']} and press Enter to check your solution")
        print(f"\nOther commands: {self.colors['info']}HINT{self.colors['reset']} (for a hint), {self.colors['info']}QUIT{self.colors['reset']} (return to menu)")
        print("-" * 50)
    
    def get_user_code(self):
        # Multi-line code input from user
        print(f"\n{self.colors['info']}Enter your code (type SUBMIT when done):{self.colors['reset']}")
        print(f"{self.colors['warning']}Tips: Use 2 spaces for indentation. Auto-indent will help you!{self.colors['reset']}")
        lines = []
        line_number = 1
        current_indent = 0
        
        while True:
            try:
                # Show line numbers and auto-indent prompt
                prompt = f"{line_number:2d}> " + " " * current_indent
                
                line = input(prompt)
                
                if line.strip().upper() == 'SUBMIT':
                    if lines:  # Make sure they actually wrote some code
                        break
                    else:
                        print(f"{self.colors['warning']}Please write some code first, then type SUBMIT{self.colors['reset']}")
                        continue
                elif line.strip().upper() == 'HINT':
                    return 'HINT'
                elif line.strip().upper() == 'QUIT':
                    return 'QUIT'
                
                # Store the line exactly as typed (including any leading spaces from the prompt)
                # The prompt already provides the correct indentation, so we just need the user's input
                actual_line = " " * current_indent + line.strip() if line.strip() else ""
                lines.append(actual_line)
                
                # Update indentation level for next line based on what they just typed
                stripped_line = line.strip()
                if stripped_line.endswith(':'):
                    # Increase indent after colons (functions, loops, if statements, etc.)
                    current_indent += 2
                elif stripped_line == '' and current_indent > 0:
                    # Blank line reduces indent (end of block)
                    current_indent = max(0, current_indent - 2)
                elif stripped_line in ['pass', 'break', 'continue', 'return'] or stripped_line.startswith('return '):
                    # These statements often end a block
                    current_indent = max(0, current_indent - 2)
                
                line_number += 1
            except KeyboardInterrupt:
                return 'QUIT'
        
        # Show what they submitted for confirmation
        print(f"\n{self.colors['info']}Code submitted:{self.colors['reset']}")
        print("-" * 30)
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line}")
        print("-" * 30)
        
        return '\n'.join(lines)
    
    def show_hint(self, hint: str):
        # Display hint with special formatting
        print(f"\n{self.colors['warning']}HINT: {hint}{self.colors['reset']}")
        print(f"{self.colors['info']}(Note: Using hints will reduce your final score){self.colors['reset']}\n")
    
    def show_result(self, success: bool, message: str, score: int = None):
        # Show challenge completion result
        if success:
            print(f"\n{self.colors['success']}SUCCESS! {message}{self.colors['reset']}")
            if score:
                print(f"{self.colors['success']}Score earned: {score} points!{self.colors['reset']}")
        else:
            print(f"\n{self.colors['error']}Not quite right: {message}{self.colors['reset']}")
            print(f"{self.colors['info']}Try again! You can do this.{self.colors['reset']}")
    
    def show_progress(self, stats: dict):
        # Display player progress and achievements
        print(f"\n{self.colors['header']}Your Progress:{self.colors['reset']}")
        print("=" * 30)
        print(f"Level: {self.colors['success']}{stats['level']}{self.colors['reset']}")
        print(f"Total Score: {self.colors['success']}{stats['score']}{self.colors['reset']}")
        print(f"Challenges Completed: {self.colors['success']}{stats['completed']}{self.colors['reset']}")
        print(f"\nUnlocked Categories:")
        for category in stats['unlocked_categories']:
            print(f"  - {category.replace('_', ' ').title()}")
    
    def get_user_choice(self, max_choice: int):
        # Get and validate user input for menu choices
        while True:
            try:
                choice = input().strip()
                choice_num = int(choice)
                if 1 <= choice_num <= max_choice:
                    return choice_num
                else:
                    print(f"{self.colors['error']}Please enter a number between 1 and {max_choice}: {self.colors['reset']}", end="")
            except ValueError:
                print(f"{self.colors['error']}Please enter a valid number: {self.colors['reset']}", end="")
            except KeyboardInterrupt:
                return None
    
    def pause(self):
        # Wait for user before continuing
        print(f"\n{self.colors['info']}Press Enter to continue...{self.colors['reset']}")
        input()