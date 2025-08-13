from challenge import Challenge, Category, Difficulty

def create_basic_challenges():
    """Set up the beginner challenges to get people started"""
    challenges = []
    
    # Simple variable challenge
    def check_hello_world(code):
        # Need to execute their code and check if it prints correctly
        try:
            exec_globals = {}
            exec(code, exec_globals)
            return True, "Great job! You've completed your first challenge."
        except:
            return False, "Make sure your code runs without errors."
    
    challenges.append(Challenge(
        id="hello_world",
        title="Hello, World!",
        description="Write a Python program that prints 'Hello, World!' to the console.",
        category=Category.BASICS,
        difficulty=Difficulty.EASY,
        solution_checker=check_hello_world,
        hints=["Use the print() function", "Don't forget the quotes around the text"]
    ))
    
    # Variable assignment challenge
    def check_variables(code):
        try:
            exec_globals = {}
            exec(code, exec_globals)
            # Check if they created the required variables
            if 'name' in exec_globals and 'age' in exec_globals:
                return True, "Perfect! You've learned about variables."
            return False, "Make sure you create both 'name' and 'age' variables."
        except:
            return False, "Check your syntax - something went wrong."
    
    challenges.append(Challenge(
        id="variables_basic",
        title="Working with Variables",
        description="Create two variables: 'name' (a string with your name) and 'age' (a number).",
        category=Category.BASICS,
        difficulty=Difficulty.EASY,
        solution_checker=check_variables,
        hints=["Variables are created with = sign", "Strings need quotes, numbers don't"]
    ))
    
    # Loop challenge
    def check_simple_loop(code):
        try:
            exec_globals = {}
            exec(code, exec_globals)
            # This is tricky to check but let's see if they used a loop keyword
            if 'for' in code or 'while' in code:
                return True, "Nice work with loops!"
            return False, "Try using a for loop or while loop."
        except:
            return False, "Something's not right with your loop syntax."
    
    challenges.append(Challenge(
        id="simple_loop",
        title="Count to Ten",
        description="Write a loop that prints numbers from 1 to 10.",
        category=Category.BASICS,
        difficulty=Difficulty.MEDIUM,
        solution_checker=check_simple_loop,
        hints=["Use 'for i in range(1, 11):'", "Don't forget to print(i) inside the loop"]
    ))
    
    return challenges

def create_data_structure_challenges():
    """Challenges focused on lists, dicts, and other data structures"""
    challenges = []
    
    # List manipulation
    def check_list_ops(code):
        try:
            exec_globals = {}
            exec(code, exec_globals)
            if 'my_list' in exec_globals and len(exec_globals['my_list']) > 0:
                return True, "Great work with lists!"
            return False, "Make sure you create and modify 'my_list'."
        except:
            return False, "Check your list syntax."
    
    challenges.append(Challenge(
        id="list_basics",
        title="List Operations",
        description="Create a list called 'my_list' with 5 numbers, then add one more number to it.",
        category=Category.DATA_STRUCTURES,
        difficulty=Difficulty.EASY,
        solution_checker=check_list_ops,
        hints=["Lists are created with square brackets []", "Use append() to add items"]
    ))
    
    return challenges

def create_algorithm_challenges():
    """More advanced algorithm challenges"""
    challenges = []
    
    # Simple sorting challenge
    def check_sort(code):
        try:
            exec_globals = {}
            exec(code, exec_globals)
            # Check if they have a function that can sort
            if 'sort_list' in exec_globals:
                test_result = exec_globals['sort_list']([3, 1, 4, 1, 5])
                if test_result == [1, 1, 3, 4, 5]:
                    return True, "Excellent sorting!"
                return False, "Your function doesn't sort correctly."
            return False, "Create a function called 'sort_list'."
        except Exception as e:
            return False, f"Error testing your function: {e}"
    
    challenges.append(Challenge(
        id="basic_sort",
        title="Sort a List",
        description="Write a function called 'sort_list' that takes a list of numbers and returns it sorted.",
        category=Category.ALGORITHMS,
        difficulty=Difficulty.MEDIUM,
        solution_checker=check_sort,
        hints=["You can use the built-in sorted() function", "Or implement bubble sort if you're feeling brave"]
    ))
    
    return challenges

def get_all_challenges():
    """Combine all challenge sets into one big list"""
    all_challenges = []
    all_challenges.extend(create_basic_challenges())
    all_challenges.extend(create_data_structure_challenges())
    all_challenges.extend(create_algorithm_challenges())
    return all_challenges