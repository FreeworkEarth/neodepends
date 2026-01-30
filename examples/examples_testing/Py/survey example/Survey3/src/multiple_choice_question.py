from question import Question
from response_correct_answer import ResponseCorrectAnswer
from input_handler import InputHandler
from output_handler import OutputHandler

class MultipleChoiceQuestion(Question):
    """Multiple choice question type"""
    
    def __init__(self, prompt, choices):
        super().__init__(prompt)
        self.choices = choices
        self.response_limit = 1
    
    @staticmethod
    def create():
        """Create a new multiple choice question"""
        new_choices = []
        OutputHandler.output("\nEnter Multiple Choice Question Prompt: ")
        prompt = InputHandler.get_console_string()
        
        OutputHandler.output("Enter Number of Choices: ")
        num_choices = InputHandler.get_console_int_less_than(10)
        
        for c in range(num_choices):
            OutputHandler.output(f"Enter Choice #{c + 1}: ")
            new_choice = InputHandler.get_console_string()
            new_choices.append(new_choice)
        
        OutputHandler.output("Last, how many answers should users be able to give: ")
        num_responses_allowed = InputHandler.get_console_int()
        if num_responses_allowed < 1:
            OutputHandler.output_line("Must allow at least 1 response. Setting response limit to 1.")
            num_responses_allowed = 1
        
        mc_question = MultipleChoiceQuestion(prompt, new_choices)
        mc_question.set_response_limit(num_responses_allowed)
        return mc_question
    
    def display(self):
        """Display the multiple choice question"""
        OutputHandler.output_line(self.prompt)
        ch = ord('a')
        for i, choice in enumerate(self.choices):
            OutputHandler.output_line(f"{chr(ch + i)}) {choice}")
        if self.response_limit > 1:
            OutputHandler.output_line(f"(Allows {self.response_limit} responses)")
    
    def tabulate(self):
        """Create tabulation map for multiple choice responses"""
        tab_map = {choice: 0 for choice in self.choices}
        
        if self.user_response:
            for response in self.user_response.get_responses():
                if response in tab_map:
                    tab_map[response] = tab_map.get(response, 0) + 1
        
        return tab_map
    
    def display_tabulation(self, this_question_map):
        """Display tabulation results"""
        for choice, count in this_question_map.items():
            OutputHandler.output_line(f" | {choice}: {count}")
    
    def obtain_user_response(self):
        """Get user response to the multiple choice question"""
        self.display()
        
        user_answer = ResponseCorrectAnswer()
        for i in range(self.response_limit):
            if self.response_limit == 1:
                OutputHandler.output("Response: ")
            else:
                OutputHandler.output(f"Response {i+1} of {self.response_limit}: ")
            decision = InputHandler.get_multiple_choice_input(len(self.choices))
            # Convert letter to choice text
            choice_index = ord(decision[0]) - ord('a')
            user_answer.add_response(self.choices[choice_index])
        
        self.set_user_response(user_answer)
    
    def is_valid_answer(self, answer):
        """Validate answer format for multiple choice"""
        str_split = answer.lower().split(",")
        str_list = [s.strip() for s in str_split if s.strip()]
        
        if len(str_list) == 0:
            return False
        
        for choice_str in str_list:
            if len(choice_str) != 1:
                return False
            index = ord(choice_str[0]) - ord('a')
            if not (0 <= index < len(self.choices)):
                return False
        
        return True
    
    def modify_question(self):
        """Modify the multiple choice question"""
        OutputHandler.output_line("You selected to edit: ")
        self.display()
        
        should_continue = True
        while should_continue:
            OutputHandler.output_line("\nChoose an option: ")
            OutputHandler.output_line("1. Modify Prompt")
            OutputHandler.output_line("2. Modify an Answer Choice")
            OutputHandler.output_line("3. Add an Answer Choice")
            OutputHandler.output_line("4. Remove an Answer Choice")
            OutputHandler.output_line("5. Modify Number of Allowed Responses")
            OutputHandler.output_line("6. Done Modifying - Exit")
            
            choice = InputHandler.get_console_int()
            
            if choice == 1:
                OutputHandler.output("Enter new question prompt: ")
                new_prompt = InputHandler.get_console_string()
                self.set_prompt(new_prompt)
                OutputHandler.output_line("Prompt successfully updated.")
            elif choice == 2:
                OutputHandler.output("Enter letter of choice to modify: ")
                choice_letter_to_modify = InputHandler.get_console_string()
                if self.is_valid_answer(choice_letter_to_modify):
                    index = ord(choice_letter_to_modify[0].lower()) - ord('a')
                    OutputHandler.output("Enter the new choice: ")
                    new_choice_text = InputHandler.get_console_string()
                    self.choices[index] = new_choice_text
                else:
                    OutputHandler.output_line("Invalid Choice")
            elif choice == 3:
                OutputHandler.output("Enter new choice: ")
                new_choice = InputHandler.get_console_string()
                self.add_choice(new_choice)
                OutputHandler.output_line("Choice added to question successfully.")
            elif choice == 4:
                OutputHandler.output("Enter the letter of the choice to delete: ")
                choice_letter_to_delete = InputHandler.get_console_string()
                index = ord(choice_letter_to_delete[0].lower()) - ord('a')
                if 0 <= index < len(self.choices):
                    self.choices.pop(index)
                    OutputHandler.output_line("Choice removed from the question.")
            elif choice == 5:
                OutputHandler.output("Enter new number of allowed responses: ")
                new_response_limit = InputHandler.get_console_int_less_than(len(self.choices))
                if new_response_limit < 1:
                    OutputHandler.output_line("Must allow at least one response.")
                else:
                    self.response_limit = new_response_limit
                    OutputHandler.output_line("Response Limit successfully updated.")
            elif choice == 6:
                should_continue = False
            else:
                OutputHandler.output_line("Unrecognized input, please try again.")
    
    def remove_choice(self, index):
        """Remove a choice by index"""
        if 0 <= index < len(self.choices):
            self.choices.pop(index)
    
    def add_choice(self, new_choice):
        """Add a new choice"""
        self.choices.append(new_choice)
    
    def get_response_limit(self):
        """Get the response limit"""
        return self.response_limit
    
    def set_response_limit(self, response_limit):
        """Set the response limit"""
        if response_limit < 1:
            OutputHandler.output_line("Must allow at least one response. Setting limit to 1.")
            self.response_limit = 1
        else:
            self.response_limit = response_limit
    
    def get_choices(self):
        """Get the list of choices"""
        return self.choices

