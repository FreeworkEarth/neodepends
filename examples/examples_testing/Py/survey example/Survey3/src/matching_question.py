from question import Question
from response_correct_answer import ResponseCorrectAnswer
from input_handler import InputHandler
from output_handler import OutputHandler
import random

class MatchingQuestion(Question):
    """Matching question type - match left items to right items"""
    
    def __init__(self, prompt, left_matches, right_matches):
        super().__init__(prompt)
        self.left_matches = left_matches
        self.right_matches = right_matches
    
    @staticmethod
    def create():
        """Create a new matching question"""
        OutputHandler.output("\nEnter Matching Question Prompt: ")
        prompt = InputHandler.get_console_string()
        
        OutputHandler.output("Enter Number of matching pairs you'd like: ")
        num_matching_pairs = InputHandler.get_console_int()
        
        left_matches = []
        right_matches = []
        OutputHandler.output_line("\nFor each matching pair please follow the format: LEFTMATCH , RIGHTMATCH")
        for c in range(num_matching_pairs):
            OutputHandler.output(f"Enter Matching Pair #{c + 1}: ")
            new_match = InputHandler.get_console_string()
            if InputHandler.safe_to_split(new_match):
                parts = new_match.split(",", 1)
                left_matches.append(parts[0].strip())
                right_matches.append(parts[1].strip())
        
        match_q = MatchingQuestion(prompt, left_matches, right_matches)
        return match_q
    
    def display(self):
        """Display the matching question with shuffled right side"""
        OutputHandler.output_line(self.prompt)
        
        # Create shuffled copy with fixed seed for consistency
        shuffled_right_matches = self.right_matches.copy()
        random.seed(10)
        random.shuffle(shuffled_right_matches)
        
        ch = ord('a')
        for i in range(len(self.left_matches)):
            left_side = f"{i + 1}) {self.left_matches[i].strip()}"
            right_side = f"{chr(ch + i)}) {shuffled_right_matches[i].strip()}"
            OutputHandler.output_spaced_strings(left_side, right_side)
    
    def tabulate(self):
        """Create tabulation map for matching responses"""
        tab_map = {}
        
        if self.user_response:
            responses = self.user_response.get_responses().copy()
            responses.sort()
            
            sb = []
            for element in responses:
                sb.append(f"| {element.upper()}\n")
            
            result = "".join(sb)
            tab_map[result] = 1
        
        return tab_map
    
    def display_tabulation(self, this_question_map):
        """Display tabulation results"""
        for response_str, count in this_question_map.items():
            OutputHandler.output_line(f"{count}\n{response_str}")
    
    def obtain_user_response(self):
        """Get user response to the matching question"""
        self.display()
        OutputHandler.output_line("Format your answer like: 1 A, where the number is first, followed by the letter.")
        
        user_answer = ResponseCorrectAnswer()
        for i in range(len(self.left_matches)):
            match_answer = self.get_valid_match_input(i + 1)
            user_answer.add_response(match_answer)
        
        self.set_user_response(user_answer)
    
    def is_valid_answer(self, answer):
        """Validate matching answer format"""
        str_split = answer.lower().split(",")
        str_list = [s.strip() for s in str_split if s.strip()]
        
        for match_str in str_list:
            split_input = match_str.split()
            if len(split_input) < 2:
                return False
            
            try:
                number = int(split_input[0])
                letter = split_input[1]
                
                if number > len(self.left_matches) or number < 1:
                    return False
                
                letter_index = ord(letter[0].lower()) - ord('a')
                if letter_index < 0 or letter_index >= len(self.left_matches):
                    return False
            except (ValueError, IndexError):
                return False
        
        return True
    
    def modify_question(self):
        """Modify the matching question"""
        OutputHandler.output_line("You selected to edit: ")
        OutputHandler.output_line(self.prompt)
        for i in range(len(self.left_matches)):
            left_side = f"{i + 1}) {self.left_matches[i]}"
            right_side = self.right_matches[i]
            OutputHandler.output_line(f"{left_side} , {right_side}")
        
        should_continue = True
        while should_continue:
            OutputHandler.output_line("\nChoose an option: ")
            OutputHandler.output_line("1. Modify Prompt")
            OutputHandler.output_line("2. Modify a Matching Pair")
            OutputHandler.output_line("3. Add a Matching Pair")
            OutputHandler.output_line("4. Remove a Matching Pair")
            OutputHandler.output_line("5. Done Modifying - Exit")
            
            choice = InputHandler.get_console_int()
            
            if choice == 1:
                OutputHandler.output("Enter new question prompt: ")
                new_prompt = InputHandler.get_console_string()
                self.set_prompt(new_prompt)
                OutputHandler.output_line("Prompt successfully updated.")
            elif choice == 2:
                OutputHandler.output("Enter number of pair to modify: ")
                pair_index_to_modify = InputHandler.get_console_int_less_than(len(self.left_matches))
                self.modify_pair(pair_index_to_modify - 1)
            elif choice == 3:
                self.add_pair()
            elif choice == 4:
                OutputHandler.output("Enter the number of the pair to delete: ")
                pair_index_to_delete = InputHandler.get_console_int_less_than(len(self.left_matches))
                self.remove_pair(pair_index_to_delete - 1)
            elif choice == 5:
                should_continue = False
            else:
                OutputHandler.output_line("Unrecognized input, please try again.")
    
    def add_pair(self):
        """Add a new matching pair"""
        OutputHandler.output("Enter new pair in format LEFT,RIGHT: ")
        new_pair = InputHandler.get_console_string()
        if InputHandler.safe_to_split(new_pair):
            parts = new_pair.split(",", 1)
            self.left_matches.append(parts[0].strip())
            self.right_matches.append(parts[1].strip())
            OutputHandler.output_line("New pair added successfully.")
        else:
            OutputHandler.output_line("Pair not formatted correctly.")
    
    def remove_pair(self, pair_index_to_delete):
        """Remove a matching pair"""
        if 0 <= pair_index_to_delete < len(self.left_matches):
            if len(self.left_matches) == 1:
                OutputHandler.output_line("Could not delete last remaining pair.")
            else:
                self.left_matches.pop(pair_index_to_delete)
                self.right_matches.pop(pair_index_to_delete)
                OutputHandler.output_line("Pair deleted successfully.")
        else:
            OutputHandler.output_line("Something went wrong trying to delete the pair.")
    
    def modify_pair(self, pair_index_to_modify):
        """Modify an existing matching pair"""
        OutputHandler.output("Enter updated pair in format LEFT,RIGHT: ")
        modified_pair = InputHandler.get_console_string()
        
        if InputHandler.safe_to_split(modified_pair) and 0 <= pair_index_to_modify < len(self.left_matches):
            parts = modified_pair.split(",", 1)
            self.left_matches[pair_index_to_modify] = parts[0].strip()
            self.right_matches[pair_index_to_modify] = parts[1].strip()
            OutputHandler.output_line("Pair updated successfully.")
        else:
            OutputHandler.output_line("Pair not formatted correctly. Cancelling...")
    
    def get_valid_match_input(self, pair_num):
        """Get valid match input from user"""
        while True:
            OutputHandler.output(f"Matching pair {pair_num}: ")
            given_input = InputHandler.get_console_string()
            try:
                if not self.is_valid_answer(given_input):
                    OutputHandler.output_line("Invalid input.")
                    continue
                return given_input
            except (IndexError, ValueError):
                OutputHandler.output_line("Invalid input. Make sure to put number first, separated by a space, then the letter.")
    
    def get_original_pairs(self):
        """Get the original matching pairs in display format"""
        shuffled_right_matches = self.right_matches.copy()
        random.seed(10)
        random.shuffle(shuffled_right_matches)
        
        original_pairs = []
        letter = ord('A')
        
        for i in range(len(self.left_matches)):
            # Find the index of the original right match in the shuffled list
            original_right_index = shuffled_right_matches.index(self.right_matches[i])
            pair_string = f"{i+1} {chr(letter + original_right_index)}"
            original_pairs.append(pair_string)
        
        return original_pairs

