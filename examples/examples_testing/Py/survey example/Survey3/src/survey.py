import os
import shutil
from question import Question
from response_correct_answer import ResponseCorrectAnswer
from input_handler import InputHandler
from output_handler import OutputHandler

class Survey:
    """Base class for surveys"""
    
    def __init__(self, name):
        self.survey_name = name
        self.questions = []
        self.times_taken = 0
    
    @staticmethod
    def create():
        """Create a new survey"""
        OutputHandler.output("\nTime to create a new survey. Please provide a survey name: ")
        survey_name = InputHandler.get_console_string()
        
        OutputHandler.output("How many questions would you like on your survey: ")
        question_amount = InputHandler.get_console_int()
        if question_amount <= 0 or question_amount > 50:
            OutputHandler.output_line("Invalid question amount, we accept 1-50 questions. Cancelling survey creation.")
            return None
        
        our_new_survey = Survey(survey_name.replace(" ", "_"))
        
        for i in range(question_amount):
            new_question = Question.create()
            if new_question is not None:
                our_new_survey.add_question(new_question)
            else:
                # Break out of loop
                break
        
        return our_new_survey
    
    def modify(self):
        """Modify the survey"""
        # Before modifying, delete old responses
        directory = f"outputs/responses/{self.survey_name}"
        self.delete_responses(directory)
        
        OutputHandler.output_line("\nChoose a modify option:")
        OutputHandler.output_line("1. Modify name")
        OutputHandler.output_line("2. Modify a question")
        OutputHandler.output_line("3. Add a question")
        OutputHandler.output_line("4. Delete a question")
        selected_option = InputHandler.get_console_int()
        
        if selected_option == 1:
            self.modify_survey_name()
        elif selected_option == 2:
            OutputHandler.output("\nEnter the number of the question you'd like to modify:")
            question_mod_index = InputHandler.get_console_int()
            self.modify_question(question_mod_index)
        elif selected_option == 3:
            new_question = Question.create()
            if new_question is not None:
                self.add_question(new_question)
        elif selected_option == 4:
            OutputHandler.output("\nEnter the number of the question you'd like to remove: ")
            question_remove_number = InputHandler.get_console_int()
            self.remove_question(question_remove_number)
        else:
            OutputHandler.output_line("Unrecognized input. Please try again.\n")
    
    def display(self):
        """Display the survey"""
        OutputHandler.output_line(f"\n------ {self.survey_name} ------")
        for i, question in enumerate(self.questions):
            OutputHandler.output_line(f"\nQuestion #{i + 1}")
            question.display()
        OutputHandler.output_line("\n------ the end -------")
    
    def take(self):
        """Take the survey"""
        for i, question in enumerate(self.questions):
            OutputHandler.output_line(f"\nQuestion #{i + 1}")
            question.obtain_user_response()
    
    def remove_all_responses(self):
        """Remove all user responses from questions"""
        for question in self.questions:
            blank = ResponseCorrectAnswer()
            question.set_user_response(blank)
    
    def delete_responses(self, directory):
        """Delete all response files in a directory"""
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
            except Exception as e:
                OutputHandler.output_line(f"Error deleting responses: {e}")
    
    def get_questions(self):
        """Get the list of questions"""
        return self.questions
    
    def add_question(self, question):
        """Add a question to the survey"""
        self.questions.append(question)
    
    def remove_question(self, question_num):
        """Remove a question by number"""
        index = question_num - 1
        if len(self.questions) == 1:
            OutputHandler.output_line("Cannot remove the only remaining question.")
        elif 0 <= index < len(self.questions):
            self.questions.pop(index)
        else:
            OutputHandler.output_line("Could not remove a question with that number. Try again")
    
    def modify_question(self, index):
        """Modify a question by index"""
        try:
            self.questions[index - 1].modify_question()
        except IndexError:
            OutputHandler.output_line("Question number not found.")
    
    def get_name(self):
        """Get the survey name"""
        return self.survey_name
    
    def modify_survey_name(self):
        """Modify the survey name"""
        OutputHandler.output("\nEnter new name: ")
        new_survey_name = InputHandler.get_console_string()
        if new_survey_name.strip() == "":
            OutputHandler.output_line("Name cannot be blank.")
        else:
            accepted_name = new_survey_name.replace(" ", "_")
            self.survey_name = accepted_name
            OutputHandler.output_line(f"Name updated to: {self.get_name()}")
    
    def get_times_taken(self):
        """Get the number of times the survey has been taken"""
        return self.times_taken
    
    def set_times_taken(self, responses):
        """Set the number of times the survey has been taken"""
        self.times_taken = responses

