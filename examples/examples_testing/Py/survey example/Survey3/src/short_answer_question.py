from essay_question import EssayQuestion
from output_handler import OutputHandler

class ShortAnswerQuestion(EssayQuestion):
    """Short answer question type - extends essay question with tabulation display"""
    
    def __init__(self, prompt):
        super().__init__(prompt)
    
    @staticmethod
    def create():
        """Create a new short answer question"""
        OutputHandler.output("\nEnter Short Answer Question Prompt: ")
        prompt = input()
        
        OutputHandler.output("How many answers should users be able to give: ")
        num_responses_allowed = InputHandler.get_console_int()
        
        sa_q = ShortAnswerQuestion(prompt)
        sa_q.set_response_limit(num_responses_allowed)
        return sa_q
    
    def display_tabulation(self, this_question_map):
        """Display tabulation results with counts"""
        for response, count in this_question_map.items():
            OutputHandler.output_line(f" | {response}: {count}")

