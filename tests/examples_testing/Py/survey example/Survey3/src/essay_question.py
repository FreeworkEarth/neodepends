from question import Question
from response_correct_answer import ResponseCorrectAnswer
from input_handler import InputHandler
from output_handler import OutputHandler

class EssayQuestion(Question):
    """Essay question type - allows free-form text responses"""
    
    def __init__(self, prompt):
        super().__init__(prompt)
        self.response_limit = 1
    
    @staticmethod
    def create():
        """Create a new essay question"""
        OutputHandler.output("\nEnter Essay Question Prompt: ")
        prompt = input()
        
        OutputHandler.output("How many answers should users be able to give: ")
        num_responses_allowed = InputHandler.get_console_int()
        
        essay_q = EssayQuestion(prompt)
        essay_q.set_response_limit(num_responses_allowed)
        return essay_q
    
    def display(self):
        """Display the essay question"""
        OutputHandler.output_line(self.prompt)
        if self.response_limit > 1:
            OutputHandler.output_line(f"(Allows {self.response_limit} responses.)")
    
    def tabulate(self):
        """Create tabulation map for essay responses"""
        tab_map = {}
        if self.user_response:
            for response in self.user_response.get_responses():
                tab_map[response] = tab_map.get(response, 0) + 1
        return tab_map
    
    def display_tabulation(self, this_question_map):
        """Display tabulation results"""
        for response, count in this_question_map.items():
            OutputHandler.output_line(f" | {response}")
    
    def obtain_user_response(self):
        """Get user response to the essay question"""
        self.display()
        
        user_answer = ResponseCorrectAnswer()
        for i in range(self.response_limit):
            if self.response_limit == 1:
                OutputHandler.output("Response: ")
            else:
                OutputHandler.output(f"Response {i+1} of {self.response_limit}: ")
            answer = InputHandler.get_console_string()
            user_answer.add_response(answer)
        
        self.set_user_response(user_answer)
    
    def is_valid_answer(self, answer):
        """Validate answer format"""
        str_split = answer.lower().split(",")
        str_list = [s.strip() for s in str_split if s.strip()]
        
        if len(str_list) == 0:
            return False
        
        return True
    
    def modify_question(self):
        """Modify the essay question"""
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

