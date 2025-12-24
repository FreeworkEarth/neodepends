from question import Question
from response_correct_answer import ResponseCorrectAnswer
from input_handler import InputHandler
from output_handler import OutputHandler
from datetime import datetime

class ValidDateQuestion(Question):
    """Valid date question type - requires date format MM-DD-YYYY"""
    
    def __init__(self, prompt):
        super().__init__(prompt)
        self.response_limit = 1
    
    @staticmethod
    def create():
        """Create a new valid date question"""
        OutputHandler.output("\nEnter Valid Date Question Prompt: ")
        prompt = input()
        
        OutputHandler.output("How many answers should users be able to give: ")
        num_responses_allowed = InputHandler.get_console_int()
        
        vd_q = ValidDateQuestion(prompt)
        vd_q.set_response_limit(num_responses_allowed)
        return vd_q
    
    def display(self):
        """Display the valid date question"""
        OutputHandler.output_line(self.prompt)
        OutputHandler.output_line("A date should be entered in the format: MM-DD-YYYY")
        if self.response_limit > 1:
            OutputHandler.output_line(f"(Allows {self.response_limit} responses)")
    
    def tabulate(self):
        """Create tabulation map for date responses"""
        tab_map = {}
        if self.user_response:
            for response in self.user_response.get_responses():
                tab_map[response] = tab_map.get(response, 0) + 1
        return tab_map
    
    def display_tabulation(self, this_question_map):
        """Display tabulation results"""
        for date, count in this_question_map.items():
            OutputHandler.output_line(f" | {date}: {count}")
    
    def obtain_user_response(self):
        """Get user response to the date question"""
        self.display()
        
        user_answer = ResponseCorrectAnswer()
        for i in range(self.response_limit):
            if self.response_limit == 1:
                OutputHandler.output("Response: ")
            else:
                OutputHandler.output(f"Response {i+1} of {self.response_limit}: ")
            answer = self.get_valid_date_input()
            user_answer.add_response(answer)
        
        self.set_user_response(user_answer)
    
    def is_valid_answer(self, answer):
        """Validate date format"""
        str_split = answer.lower().split(",")
        str_list = [s.strip() for s in str_split if s.strip()]
        
        if len(str_list) == 0:
            return False
        
        for date_str in str_list:
            if not self._is_valid_date(date_str):
                return False
        
        return True
    
    def _is_valid_date(self, date_str):
        """Check if a string is a valid date in MM-DD-YYYY format"""
        try:
            datetime.strptime(date_str, "%m-%d-%Y")
            return True
        except ValueError:
            return False
    
    def modify_question(self):
        """Modify the valid date question"""
        OutputHandler.output_line("You selected to edit: ")
        self.display()
        
        OutputHandler.output("\nModify Prompt? (Enter Y or N): ")
        decision = InputHandler.get_yn_console_input()
        
        if decision:
            OutputHandler.output("Enter new question prompt: ")
            new_prompt = input()
            self.set_prompt(new_prompt)
            OutputHandler.output_line("Prompt successfully updated.")
        
        OutputHandler.output("\nModify Number of Allowed Responses? (Enter Y or N): ")
        decision2 = InputHandler.get_yn_console_input()
        
        if decision2:
            OutputHandler.output("Enter new number of allowed responses: ")
            new_response_limit = InputHandler.get_console_int()
            self.set_response_limit(new_response_limit)
            OutputHandler.output_line("Response Limit successfully updated.")
    
    def get_valid_date_input(self):
        """Get a valid date input from user"""
        while True:
            inputted_string = InputHandler.get_console_string()
            if self._is_valid_date(inputted_string):
                return inputted_string
            OutputHandler.output_line("Date formatting error. Make sure you're using the format specified by the question. Try again...")
    
    def get_response_limit(self):
        """Get the response limit"""
        return self.response_limit
    
    def set_response_limit(self, response_limit):
        """Set the response limit"""
        self.response_limit = response_limit

