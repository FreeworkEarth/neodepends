import os
from input_handler import InputHandler
from output_handler import OutputHandler

class Grader:
    """Handles grading workflow for tests"""
    
    def select_test_to_grade(self):
        """Select which test to grade"""
        output_directory = "outputs/tests"
        
        if not os.path.exists(output_directory):
            OutputHandler.output_line("No tests found.")
            return None
        
        list_of_files = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
        
        if len(list_of_files) == 0:
            OutputHandler.output_line("No tests found.")
            return None
        
        OutputHandler.output_line("\nWhich test would you like to grade? Type the number next to the test name.")
        
        for i, filename in enumerate(list_of_files):
            OutputHandler.output_line(f"{i + 1}) {filename}")
        
        OutputHandler.output("\nFile number: ")
        file_index = InputHandler.get_console_int() - 1
        
        if 0 <= file_index < len(list_of_files):
            full_filename = list_of_files[file_index]
            return full_filename[:full_filename.rindex('.')]
        
        return None
    
    def select_test_response_to_grade(self, test_name):
        """Select which test response to grade"""
        output_directory = f"outputs/responses/{test_name}"
        
        if not os.path.exists(output_directory):
            OutputHandler.output_line("No test responses found.")
            return None
        
        list_of_files = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
        
        if len(list_of_files) == 0:
            OutputHandler.output_line("No test responses found.")
            return None
        
        OutputHandler.output_line("\nType the number of the response you'd like to grade.")
        
        for i, filename in enumerate(list_of_files):
            OutputHandler.output_line(f"{i + 1}) {filename}")
        
        OutputHandler.output("\nFile number: ")
        file_index = InputHandler.get_console_int() - 1
        
        if 0 <= file_index < len(list_of_files):
            return list_of_files[file_index]
        
        return None

