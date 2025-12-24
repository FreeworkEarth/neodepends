from menu import Menu
from test import Test
from serializer import Serializer
from tabulator import Tabulator
from grader import Grader
from input_handler import InputHandler
from output_handler import OutputHandler

class TestMenu(Menu):
    """Menu for test operations"""
    
    def __init__(self):
        self.serializer = Serializer()
        self.tabulator = Tabulator()
        self.grader = Grader()
        self.current_test = None
    
    def present_menu(self):
        """Present the test menu"""
        running = True
        
        while running:
            OutputHandler.output_line("\nYou selected Test. Please type the number of an option below:")
            OutputHandler.output_line("1. Create a test")
            OutputHandler.output_line("2. Display the current test (without correct answers)")
            OutputHandler.output_line("3. Display the current test (with correct answers)")
            OutputHandler.output_line("4. Load an existing test")
            OutputHandler.output_line("5. Save the current test")
            OutputHandler.output_line("6. Take the current test")
            OutputHandler.output_line("7. Modify the current test")
            OutputHandler.output_line("8. Tabulate a test")
            OutputHandler.output_line("9. Grade a test")
            OutputHandler.output_line("10. Go back")
            
            chosen_option = InputHandler.get_console_int()
            
            if chosen_option == 1:
                self.current_test = self.create()
            elif chosen_option == 2:
                self.display(self.current_test)
            elif chosen_option == 3:
                self.display_with_correct_answers()
            elif chosen_option == 4:
                self.current_test = self.load()
            elif chosen_option == 5:
                self.save()
            elif chosen_option == 6:
                self.take()
            elif chosen_option == 7:
                self.modify()
            elif chosen_option == 8:
                self.tabulate()
            elif chosen_option == 9:
                self.grade()
            elif chosen_option == 10:
                running = False
            else:
                OutputHandler.output_line("Unrecognized input. Please try again.\n")
    
    def create(self):
        """Create a new test"""
        our_new_test = Test.create()
        if our_new_test is not None:
            OutputHandler.output_line(f"\n{our_new_test.get_name()} has been created and is now the currently selected test!")
        return our_new_test
    
    def load(self):
        """Load a test"""
        return self.serializer.load_test()
    
    def display_with_correct_answers(self):
        """Display the test with correct answers"""
        if self.current_test is not None:
            self.current_test.display_with_correct_answers()
        else:
            OutputHandler.output_line("Test must be loaded before displayed.")
    
    def save(self):
        """Save the current test"""
        if self.current_test is not None:
            self.serializer.save(self.current_test, "test", False)
        else:
            OutputHandler.output_line("You must have a test loaded in order to save it.")
    
    def take(self):
        """Take the current test"""
        if self.current_test is not None:
            self.current_test.take()
            
            # Save the test with the responses attached
            self.serializer.save_test_response(self.current_test)
            
            self.current_test.set_times_taken(self.current_test.get_times_taken() + 1)
            
            # Remove the given answers from the original test (now that we've saved the response)
            self.current_test.remove_all_responses()
            
            self.serializer.save(self.current_test, "test", True)
        else:
            OutputHandler.output_line("You must have a test loaded in order to take it.")
    
    def modify(self):
        """Modify the current test"""
        if self.current_test is not None:
            self.current_test.modify()
        else:
            OutputHandler.output_line("You must have a test loaded in order to modify it.")
    
    def tabulate(self):
        """Tabulate a test"""
        file_name = self.tabulator.select_item_to_tabulate("test")
        if file_name:
            OutputHandler.output_line(f"Tabulating {file_name}....")
            self.tabulator.tabulate_survey(file_name)
    
    def grade(self):
        """Grade a test response"""
        test_name = self.grader.select_test_to_grade()
        if test_name:
            test_response_name = self.grader.select_test_response_to_grade(test_name)
            if test_response_name:
                test_to_grade = self.serializer.load_test_response(test_name, test_response_name)
                if test_to_grade is not None:
                    test_to_grade.grade()

