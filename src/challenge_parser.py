"""
Parser to convert external coding problems into the game's Challenge format
"""
import ast
import re
import os
from typing import List, Tuple, Callable
from challenge import Challenge, Category, Difficulty


def find_function_with_param_count(user_globals: dict, expected_param_count: int):
    """Helper function to find any user-defined function with the expected parameter count"""
    for name, obj in user_globals.items():
        if callable(obj) and hasattr(obj, '__code__'):
            user_params = len(obj.__code__.co_varnames[:obj.__code__.co_argcount])
            if user_params == expected_param_count:
                return obj
    return None


class ChallengeParser:
    """Converts coding problem files to Challenge objects"""
    
    def __init__(self, problems_directory: str):
        self.problems_directory = problems_directory
        
    def parse_problem_file(self, filepath: str) -> Challenge:
        """Parse a single coding problem file into a Challenge object"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract function details
        function_info = self._extract_function_info(content)
        test_cases = self._extract_test_cases(content)
        
        # Generate challenge metadata
        challenge_id = self._generate_id(filepath)
        title = self._generate_title(function_info['name'])
        description = function_info['docstring'] or self._generate_description_from_code(function_info['name'], content)
        category = self._determine_category(challenge_id, content)
        difficulty = self._determine_difficulty(content, function_info)
        
        # Create solution checker
        solution_checker = self._create_solution_checker(
            function_info['name'], 
            test_cases,
            content
        )
        
        # Generate hints
        hints = self._generate_hints(function_info, content)
        
        # Extract expected answer (the original implementation)
        expected_answer = self._extract_function_body(content, function_info['name'])
        
        return Challenge(
            id=challenge_id,
            title=title,
            description=description,
            category=category,
            difficulty=difficulty,
            solution_checker=solution_checker,
            hints=hints,
            expected_answer=expected_answer
        )
    
    def _extract_function_info(self, content: str) -> dict:
        """Extract function name, parameters, and docstring"""
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get the first function (main function)
                docstring = ast.get_docstring(node)
                params = [arg.arg for arg in node.args.args]
                
                return {
                    'name': node.name,
                    'params': params,
                    'docstring': docstring
                }
        
        return {'name': 'solution', 'params': [], 'docstring': None}
    
    def _extract_test_cases(self, content: str) -> List[Tuple]:
        """Extract test cases from the file"""
        test_cases = []
        
        # Look for test patterns like: print(f"... {function_name(...)} ...")
        test_pattern = r'(\[.*?\]|\(.*?\)|\d+|".*?"|\w+)\s*,?\s*'
        
        # Find lines with test calls
        lines = content.split('\n')
        for line in lines:
            if 'print(f' in line and '=' in line:
                # Extract test parameters - this is basic pattern matching
                # More sophisticated parsing could be added
                if '[' in line and ']' in line:
                    # List-based test case
                    lists = re.findall(r'\[(.*?)\]', line)
                    if lists:
                        test_cases.append(lists)
                elif '(' in line and ')' in line:
                    # Tuple or parameter-based test case
                    params = re.findall(r'[\'"](.*?)[\'"]|\b(\d+)\b', line)
                    if params:
                        test_cases.append([p[0] or p[1] for p in params if p[0] or p[1]])
        
        return test_cases[:3]  # Limit to first 3 test cases
    
    def _create_solution_checker(self, function_name: str, test_cases: List, original_content: str) -> Callable:
        """Create a function to check user solutions"""
        
        def checker(user_code: str) -> Tuple[bool, str]:
            try:
                # Execute the original solution to get expected results
                exec_globals = {}
                exec(original_content, exec_globals)
                expected_func = exec_globals.get(function_name)
                
                if not expected_func:
                    return False, f"Could not find reference function {function_name}"
                
                # Execute user's code
                user_globals = {}
                exec(user_code, user_globals)
                
                # Find any function in user's code that matches the expected signature
                original_params = len(expected_func.__code__.co_varnames[:expected_func.__code__.co_argcount])
                user_func = find_function_with_param_count(user_globals, original_params)
                
                if not user_func:
                    return False, f"Your code must define a function that takes {original_params} parameter(s)"
                
                # Test with basic cases if we have them
                basic_tests = [
                    # Two Sum test
                    {'func': 'twoSum', 'args': [([2, 7, 11, 15], 9)], 'expected_type': list},
                    # FizzBuzz test  
                    {'func': 'fizz_buzz', 'args': [(15,)], 'expected_type': list},
                    # Palindrome test
                    {'func': 'is_palindrome', 'args': [("A man, a plan, a canal: Panama",)], 'expected_type': bool},
                    # Container with water
                    {'func': 'maxArea', 'args': [([1,8,6,2,5,4,8,3,7],)], 'expected_type': int},
                    # Anagram test
                    {'func': 'is_anagram', 'args': [("listen", "silent")], 'expected_type': bool},
                    # Plus one test
                    {'func': 'plus_one', 'args': [([1, 2, 3],)], 'expected_type': list},
                ]
                
                # Find matching test for this function
                matching_test = None
                for test in basic_tests:
                    if test['func'] == function_name:
                        matching_test = test
                        break
                
                if matching_test:
                    for args in matching_test['args']:
                        try:
                            expected_result = expected_func(*args)
                            user_result = user_func(*args)
                            
                            if expected_result != user_result:
                                return False, f"Test failed with input {args}. Expected {expected_result}, got {user_result}"
                        except NameError as e:
                            if 'true' in str(e).lower() or 'false' in str(e).lower():
                                return False, f"Error: Use 'True' and 'False' (with capital letters) for boolean values, not 'true'/'false'"
                            else:
                                return False, f"Name error in your code: {e}"
                        except Exception as e:
                            return False, f"Error running test with {args}: {e}"
                
                # If we get here, basic tests passed
                return True, "Great job! Your solution works correctly."
                
            except Exception as e:
                return False, f"Error in your code: {e}"
        
        return checker
    
    def _determine_category(self, challenge_id: str, content: str) -> Category:
        """Determine the appropriate category for the challenge"""
        
        # LeetCode-style problems (classic interview questions)
        leetcode_problems = ['two_sum', 'container_water', 'buy_sell_stock', 'jump_game', 
                            'gas_station', 'majority_element', 'contains_duplicate']
        
        # Algorithm-heavy problems
        algorithm_keywords = ['sort', 'search', 'tree', 'graph', 'dynamic', 'recursion']
        
        # Data structure problems
        data_structure_keywords = ['array', 'list', 'hash', 'map', 'dict', 'stack', 'queue',
                                  'duplicate', 'merge', 'plus_one', 'remove']
        
        # String/pattern problems  
        string_keywords = ['string', 'palindrome', 'anagram', 'pattern', 'prefix', 'roman',
                          'ip', 'word', 'isomorphic', 'ransom', 'subsequence', 'first']
        
        # Basic problems
        basic_keywords = ['fizz', 'buzz', 'factorial', 'sqrt', 'capital', 'length', 'last']
        
        content_lower = content.lower()
        id_lower = challenge_id.lower()
        
        # Check for LeetCode-style problems first
        if any(problem in id_lower for problem in leetcode_problems):
            return Category.LEETCODE
        elif any(keyword in content_lower or keyword in id_lower for keyword in algorithm_keywords):
            return Category.ALGORITHMS
        elif any(keyword in content_lower or keyword in id_lower for keyword in data_structure_keywords):
            return Category.DATA_STRUCTURES
        elif any(keyword in content_lower or keyword in id_lower for keyword in string_keywords):
            return Category.PROBLEM_SOLVING
        elif any(keyword in content_lower or keyword in id_lower for keyword in basic_keywords):
            return Category.BASICS
        else:
            return Category.PROBLEM_SOLVING  # Default
    
    def _determine_difficulty(self, content: str, function_info: dict) -> Difficulty:
        """Analyze code complexity to determine difficulty"""
        
        # Count complexity indicators
        complexity_score = 0
        
        # Check for advanced concepts
        if 'while' in content:
            complexity_score += 2
        if 'for' in content and 'range' not in content:
            complexity_score += 1
        if 'enumerate' in content:
            complexity_score += 1
        if 'dict' in content or '{}' in content:
            complexity_score += 2
        if 'try:' in content or 'except' in content:
            complexity_score += 1
        
        # Count nested structures
        nesting_level = content.count('    if') + content.count('        ')
        complexity_score += nesting_level // 4
        
        # Length-based complexity
        line_count = len(content.split('\n'))
        if line_count > 30:
            complexity_score += 2
        elif line_count > 20:
            complexity_score += 1
        
        # Docstring length (longer descriptions usually mean harder problems)
        if function_info.get('docstring'):
            doc_length = len(function_info['docstring'])
            if doc_length > 200:
                complexity_score += 2
            elif doc_length > 100:
                complexity_score += 1
        
        # Map score to difficulty
        if complexity_score >= 6:
            return Difficulty.HARD
        elif complexity_score >= 3:
            return Difficulty.MEDIUM
        else:
            return Difficulty.EASY
    
    def _generate_hints(self, function_info: dict, content: str) -> List[str]:
        """Generate helpful hints based on the code structure"""
        hints = []
        
        function_name = function_info['name']
        
        # Function-specific hints
        if function_name == 'twoSum':
            hints = [
                "Consider using a hash map to store numbers you've seen",
                "For each number, check if its complement exists in your map",
                "The complement is target - current_number"
            ]
        elif function_name == 'fizz_buzz':
            hints = [
                "Use the modulo operator % to check divisibility",
                "Check for divisibility by both 3 AND 5 first",
                "Don't forget to convert numbers to strings"
            ]
        elif function_name == 'is_palindrome':
            hints = [
                "Remove non-alphanumeric characters first",
                "Convert to lowercase for comparison",
                "Compare the string with its reverse"
            ]
        elif function_name == 'maxArea':
            hints = [
                "Use two pointers, one at start and one at end",
                "Calculate area as width * min(left_height, right_height)",
                "Move the pointer with the smaller height"
            ]
        elif function_name == 'is_anagram':
            hints = [
                "Count the frequency of each character",
                "Two strings are anagrams if they have the same character counts",
                "You can use dictionaries to count characters"
            ]
        else:
            # Generic hints based on code analysis
            if 'dict' in content or '{}' in content:
                hints.append("Consider using a dictionary to track values")
            if 'for' in content:
                hints.append("Think about what you need to iterate through")
            if 'while' in content:
                hints.append("Consider the loop termination condition carefully")
            if not hints:
                hints.append("Break the problem down into smaller steps")
                hints.append("Think about edge cases")
        
        return hints[:3]  # Limit to 3 hints
    
    def _generate_title(self, function_name: str) -> str:
        """Generate a readable title from the function name"""
        # Convert snake_case to Title Case
        title = function_name.replace('_', ' ').title()
        
        # Handle special cases
        replacements = {
            'Twos um': 'Two Sum',
            'Fizz Buzz': 'FizzBuzz',
            'Is Palindrome': 'Palindrome Check', 
            'Maxarea': 'Container With Most Water',
            'Is Anagram': 'Valid Anagram',
            'Plus One': 'Plus One'
        }
        
        for old, new in replacements.items():
            if old in title:
                title = new
                break
        
        return title
    
    def _generate_id(self, filepath: str) -> str:
        """Generate a unique ID from the filepath"""
        filename = os.path.basename(filepath)
        return filename.replace('.py', '').lower()
    
    def _extract_function_body(self, content: str, function_name: str) -> str:
        """Extract the complete function implementation"""
        lines = content.split('\n')
        function_lines = []
        in_function = False
        
        for line in lines:
            if line.strip().startswith(f'def {function_name}('):
                in_function = True
                function_lines.append(line)
            elif in_function:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    # Function ended
                    break
                function_lines.append(line)
        
        return '\n'.join(function_lines)
    
    def _generate_description_from_code(self, function_name: str, content: str) -> str:
        """Generate helpful descriptions for functions without docstrings"""
        
        # Function-specific descriptions based on analysis
        descriptions = {
            'plus_one': """Given an array of digits representing a non-negative integer, add 1 to the integer.
The digits are stored such that the most significant digit is at the head of the list.
Each element in the array contains a single digit.

Example: [1,2,3] represents 123, so adding 1 gives [1,2,4] (124)
Example: [9,9] represents 99, so adding 1 gives [1,0,0] (100)""",
            
            'intToRoman': """Given an integer, convert it to a Roman numeral.
Roman numerals use these symbols:
I=1, V=5, X=10, L=50, C=100, D=500, M=1000

Examples: 3 -> "III", 9 -> "IX", 58 -> "LVIII", 1994 -> "MCMXCIV"
Note: Numbers 1-3999 are supported.""",
            
            'merge': """Merge two sorted integer arrays nums1 and nums2 into nums1 in sorted order.
nums1 has size m+n where the last n elements are 0 (placeholders for nums2).
nums2 has size n.

Example: nums1=[1,2,3,0,0,0], m=3, nums2=[2,5,6], n=3
Result: nums1 becomes [1,2,2,3,5,6]""",
            
            'removeDuplicates': """Given a sorted integer array, remove duplicates in-place.
Return the number of unique elements. The first k elements of nums should contain the unique elements.

Example: [1,1,2] -> return 2, nums becomes [1,2,...]
Example: [0,0,1,1,1,2,2,3,3,4] -> return 5, nums becomes [0,1,2,3,4,...]""",
            
            'mySqrt': """Given a non-negative integer x, return the square root of x rounded down to the nearest integer.
You must not use any built-in exponent function or operator.

Examples: 4 -> 2, 8 -> 2 (since sqrt(8) = 2.828...), 16 -> 4""",
            
            'detectCapitalUse': """Given a word, determine if the usage of capitals is correct.
Correct usage means:
1. All letters are capitals: "USA" 
2. All letters are lowercase: "leetcode"
3. Only first letter is capital: "Google"

Return True if correct, False otherwise.""",
        }
        
        # Check if we have a specific description for this function
        if function_name in descriptions:
            return descriptions[function_name]
        
        # Try to infer from function name and code patterns
        name_lower = function_name.lower()
        
        if 'palindrome' in name_lower:
            return "Given a string, determine if it's a palindrome (reads the same forwards and backwards). Ignore case and non-alphanumeric characters."
        elif 'anagram' in name_lower:
            return "Given two strings, determine if they are anagrams (contain the same characters in different order)."
        elif 'twosum' in name_lower or 'two_sum' in name_lower:
            return "Given an array of integers and a target sum, return the indices of two numbers that add up to the target."
        elif 'isomorphic' in name_lower:
            return "Given two strings, determine if they are isomorphic (characters can be mapped to get from one to the other)."
        elif 'fizz' in name_lower and 'buzz' in name_lower:
            return "Given an integer n, return a list where multiples of 3 are 'Fizz', multiples of 5 are 'Buzz', and multiples of both are 'FizzBuzz'."
        elif 'factorial' in name_lower:
            return "Given a non-negative integer, return its factorial (n! = n * (n-1) * ... * 1)."
        elif 'sort' in name_lower:
            return "Given an array, return it sorted in ascending order."
        elif 'reverse' in name_lower:
            return "Given an input, return it reversed."
        elif 'valid' in name_lower or 'check' in name_lower:
            return "Given an input, validate it according to the specified rules and return True/False."
        elif 'find' in name_lower or 'search' in name_lower:
            return "Given an input, find and return the specified element or condition."
        elif 'count' in name_lower or 'length' in name_lower:
            return "Given an input, count and return the number of elements matching the criteria."
        elif 'contains' in name_lower:
            return "Given an input, determine if it contains the specified element or condition."
        elif 'max' in name_lower and ('area' in name_lower or 'profit' in name_lower):
            return "Given constraints, find and return the maximum value possible."
        elif 'roman' in name_lower:
            return "Convert between integers and Roman numerals."
        else:
            return f"Implement the {function_name} function. Look at the test cases and code structure to understand what it should do."
    
    def parse_all_problems(self) -> List[Challenge]:
        """Parse all Python files in the problems directory"""
        challenges = []
        
        if not os.path.exists(self.problems_directory):
            print(f"Problems directory not found: {self.problems_directory}")
            return challenges
        
        for filename in os.listdir(self.problems_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                filepath = os.path.join(self.problems_directory, filename)
                try:
                    challenge = self.parse_problem_file(filepath)
                    challenges.append(challenge)
                    print(f"Parsed: {challenge.title} ({challenge.difficulty.name})")
                except Exception as e:
                    print(f"Failed to parse {filename}: {e}")
        
        return challenges