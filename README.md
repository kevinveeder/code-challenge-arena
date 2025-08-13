# Code Challenge Arena

A Python game designed to help improve coding skills through interactive challenges.

## Features

- Multiple challenge categories (Basics, Data Structures, Algorithms, Problem Solving, Debugging)
- Progressive difficulty scaling
- Time-based scoring with hint system
- Progress tracking and unlockables
- Clear submission interface with line numbers
- Colorized terminal output for better experience

## Getting Started

### Clone and Run

```bash
# Clone the repository
git clone https://github.com/kevinveeder/code-challenge-arena.git
cd code-challenge-arena

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start playing!
python src/main.py
```

### What Playing Looks Like

When you start the game, you'll see the main menu:

```
==================================================
     CODE CHALLENGE ARENA
   Level up your coding skills!
==================================================

What would you like to do?
1. Start a challenge
2. View your progress
3. View available categories
4. Quit
```

**Starting a Challenge:**
```
Available Challenges:
----------------------------------------
1. Hello, World!
   Category: Basics
   Difficulty: EASY
   Write a Python program that prints 'Hello, World!' to the co...

Choose a challenge (1-1) or 0 to go back: 1
```

**Writing Your Solution:**
```
Challenge: Hello, World!
==================================================

Category: Basics
Difficulty: EASY

Description:
Write a Python program that prints 'Hello, World!' to the console.

HOW TO SUBMIT:
1. Type your Python code (multiple lines allowed)
2. When done, press Enter to go to a new line
3. Type SUBMIT and press Enter to check your solution

Other commands: HINT (for a hint), QUIT (return to menu)
--------------------------------------------------

Enter your code (type SUBMIT when done):
 1> print("Hello, World!")
 2> SUBMIT

Code submitted:
------------------------------
 1: print("Hello, World!")
------------------------------

SUCCESS! Perfect! You've mastered your first print statement.
Score earned: 140 points!
```

**Progression System:**
- Complete challenges to earn points and level up
- Unlock new categories as you progress (Data Structures at level 2, Algorithms at level 4, etc.)
- Use hints if you get stuck (but they reduce your score)
- Track your progress and see your improvement over time

## Project Structure

```
code-challenge-arena/
├── src/           # Source code
├── tests/         # Unit tests
├── data/          # Challenge data and configs
└── README.md      # This file
```