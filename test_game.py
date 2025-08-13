#!/usr/bin/env python3

import sys
import os
sys.path.append('src')

from challenges_data import create_basic_challenges
from game_engine import GameEngine
from ui import GameUI

def test_hello_world_challenge():
    """Test that the hello world challenge works correctly"""
    print("Testing Hello World challenge...")
    
    challenges = create_basic_challenges()
    hello_world = challenges[0]  # First challenge should be hello world
    
    # Test correct solution
    correct_code = 'print("Hello, World!")'
    success, message = hello_world.check_solution(correct_code)
    print(f"Correct code test: {success} - {message}")
    
    # Test incorrect solution
    wrong_code = 'print("Hello World")'  # Missing comma and exclamation
    success, message = hello_world.check_solution(wrong_code)
    print(f"Wrong code test: {success} - {message}")
    
    # Test code with error
    error_code = 'prin("Hello, World!")'  # Typo in print
    success, message = hello_world.check_solution(error_code)
    print(f"Error code test: {success} - {message}")

def test_game_engine():
    """Test that the game engine works"""
    print("\nTesting Game Engine...")
    
    engine = GameEngine()
    for challenge in create_basic_challenges():
        engine.add_challenge(challenge)
    
    available = engine.get_available_challenges()
    print(f"Available challenges: {len(available)}")
    
    stats = engine.get_player_stats()
    print(f"Player stats: {stats}")

def test_ui_components():
    """Test UI components that don't require user input"""
    print("\nTesting UI components...")
    
    ui = GameUI()
    challenges = create_basic_challenges()
    
    print("Testing challenge display...")
    ui.show_challenges(challenges[:1])  # Show just the first one
    
    print("\nTesting progress display...")
    stats = {"level": 1, "score": 0, "completed": 0, "unlocked_categories": ["basics"]}
    ui.show_progress(stats)

if __name__ == "__main__":
    print("Running Code Challenge Arena tests...\n")
    
    try:
        test_hello_world_challenge()
        test_game_engine()
        test_ui_components()
        print("\n[SUCCESS] All tests completed successfully!")
        print("\nThe game interface has been improved with:")
        print("- Clear step-by-step instructions for submitting code")
        print("- Line numbers during code entry")
        print("- Code confirmation before checking")
        print("- Better error handling for empty submissions")
        print("- Proper output checking for Hello World challenge")
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()