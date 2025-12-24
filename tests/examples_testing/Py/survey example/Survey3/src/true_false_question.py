from multiple_choice_question import MultipleChoiceQuestion
from input_handler import InputHandler
from output_handler import OutputHandler

class TrueFalseQuestion(MultipleChoiceQuestion):
    """True/False question type - extends multiple choice with fixed choices"""
    
    def __init__(self, prompt, choices):
        super().__init__(prompt, choices)
    
    @staticmethod
    def create():
        """Create a new true/false question"""
        choices = ["True", "False"]
        
        OutputHandler.output("\nEnter True/False Question Prompt: ")
        prompt = input()
        
        tf_q = TrueFalseQuestion(prompt, choices)
        return tf_q
    
    def modify_question(self):
        """Modify the true/false question"""
        OutputHandler.output_line("You selected to edit: ")
        self.display()
        
        OutputHandler.output("\nModify Prompt? (Enter Y or N): ")
        decision = InputHandler.get_yn_console_input()
        
        if decision:
            OutputHandler.output("Enter new question prompt: ")
            new_prompt = input()
            self.set_prompt(new_prompt)
            OutputHandler.output_line("Prompt successfully updated.")
    
    def get_response_limit(self):
        """Get the response limit (always 1 for T/F)"""
        return 1

