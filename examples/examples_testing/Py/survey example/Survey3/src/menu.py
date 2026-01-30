from survey import Survey
from output_handler import OutputHandler

class Menu:
    """Abstract base class for menus"""
    
    def display(self, current_survey):
        """Display a survey or test"""
        if current_survey is not None:
            current_survey.display()
        else:
            OutputHandler.output_line("Must have a survey or test loaded to display it.")

