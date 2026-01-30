from menu import Menu
from survey import Survey
from serializer import Serializer
from tabulator import Tabulator
from input_handler import InputHandler
from output_handler import OutputHandler

class SurveyMenu(Menu):
    """Menu for survey operations"""
    
    def __init__(self):
        self.serializer = Serializer()
        self.tabulator = Tabulator()
        self.current_survey = None
    
    def present_menu(self):
        """Present the survey menu"""
        running = True
        
        while running:
            OutputHandler.output_line("\nYou selected Survey. Please type the number of an option below:")
            OutputHandler.output_line("1. Create a survey")
            OutputHandler.output_line("2. Display the current survey")
            OutputHandler.output_line("3. Load an existing survey")
            OutputHandler.output_line("4. Save the current survey")
            OutputHandler.output_line("5. Take the current survey")
            OutputHandler.output_line("6. Modify the current survey")
            OutputHandler.output_line("7. Tabulate a survey")
            OutputHandler.output_line("8. Go back")
            
            chosen_option = InputHandler.get_console_int()
            
            if chosen_option == 1:
                self.current_survey = self.create()
            elif chosen_option == 2:
                self.display(self.current_survey)
            elif chosen_option == 3:
                self.current_survey = self.load()
            elif chosen_option == 4:
                self.save()
            elif chosen_option == 5:
                self.take()
            elif chosen_option == 6:
                self.modify()
            elif chosen_option == 7:
                self.tabulate()
            elif chosen_option == 8:
                running = False
            else:
                OutputHandler.output_line("Unrecognized input. Please try again.\n")
    
    def create(self):
        """Create a new survey"""
        our_new_survey = Survey.create()
        if our_new_survey is not None:
            OutputHandler.output_line(f"\n{our_new_survey.get_name()} has been created and is now the currently selected survey!")
        return our_new_survey
    
    def save(self):
        """Save the current survey"""
        if self.current_survey is not None:
            self.serializer.save(self.current_survey, "survey", False)
        else:
            OutputHandler.output_line("You must have a survey loaded in order to save it.")
    
    def load(self):
        """Load a survey"""
        return self.serializer.load_survey()
    
    def take(self):
        """Take the current survey"""
        if self.current_survey is not None:
            self.current_survey.take()
            
            # Save the survey with the responses attached
            self.serializer.save_survey_response(self.current_survey)
            
            self.current_survey.set_times_taken(self.current_survey.get_times_taken() + 1)
            
            # Remove the given answers from the original survey (now that we've saved the response)
            self.current_survey.remove_all_responses()
            
            self.serializer.save(self.current_survey, "survey", True)
        else:
            OutputHandler.output_line("You must have a survey loaded in order to take it.")
    
    def modify(self):
        """Modify the current survey"""
        if self.current_survey is not None:
            self.current_survey.modify()
        else:
            OutputHandler.output_line("You must have a survey loaded in order to modify it.")
    
    def tabulate(self):
        """Tabulate a survey"""
        file_name = self.tabulator.select_item_to_tabulate("survey")
        if file_name:
            OutputHandler.output_line(f"Tabulating {file_name}....")
            self.tabulator.tabulate_survey(file_name)

