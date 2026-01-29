from abc import ABC, abstractmethod
from input_handler import InputHandler
from output_handler import OutputHandler

class Question(ABC):
    """Abstract base class for all question types"""
    
    def __init__(self, prompt):
        self.prompt = prompt
        self.user_response = None
    
    @staticmethod
    def create():
        """Factory method to create a question"""
        OutputHandler.output_line("\nChoose from the options below for your new question:")
        OutputHandler.output_line("1. Add a new T/F question")
        OutputHandler.output_line("2. Add a new multiple choice question")
        OutputHandler.output_line("3. Add a new short answer question")
        OutputHandler.output_line("4. Add a new essay question")
        OutputHandler.output_line("5. Add a new date question")
        OutputHandler.output_line("6. Add a new matching question")
        OutputHandler.output_line("7. Cancel & Return to previous menu")
        
        selected_option = InputHandler.get_console_int_less_than(7)
        
        if selected_option == 1:
            from true_false_question import TrueFalseQuestion
            return TrueFalseQuestion.create()
        elif selected_option == 2:
            from multiple_choice_question import MultipleChoiceQuestion
            return MultipleChoiceQuestion.create()
        elif selected_option == 3:
            from short_answer_question import ShortAnswerQuestion
            return ShortAnswerQuestion.create()
        elif selected_option == 4:
            from essay_question import EssayQuestion
            return EssayQuestion.create()
        elif selected_option == 5:
            from valid_date_question import ValidDateQuestion
            return ValidDateQuestion.create()
        elif selected_option == 6:
            from matching_question import MatchingQuestion
            return MatchingQuestion.create()
        elif selected_option == 7:
            return None
        
        return None
    
    @abstractmethod
    def display(self):
        """Display the question"""
        pass
    
    @abstractmethod
    def tabulate(self):
        """Create a tabulation map of responses"""
        pass
    
    @abstractmethod
    def display_tabulation(self, this_question_map):
        """Display tabulation results"""
        pass
    
    @abstractmethod
    def obtain_user_response(self):
        """Get user response to the question"""
        pass
    
    @abstractmethod
    def is_valid_answer(self, answer):
        """Validate if an answer is valid for this question type"""
        pass
    
    @abstractmethod
    def modify_question(self):
        """Modify the question"""
        pass
    
    def get_prompt(self):
        """Get the question prompt"""
        return self.prompt
    
    def set_prompt(self, prompt):
        """Set the question prompt"""
        self.prompt = prompt
    
    def set_user_response(self, response):
        """Set the user response"""
        self.user_response = response
    
    def get_user_response(self):
        """Get the user response"""
        return self.user_response

