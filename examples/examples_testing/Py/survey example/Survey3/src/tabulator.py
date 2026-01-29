import os
from serializer import Serializer
from input_handler import InputHandler
from output_handler import OutputHandler

class Tabulator:
    """Handles tabulation of survey/test responses"""
    
    def __init__(self):
        self.survey_responses = []
        self.serializer = Serializer()
    
    def select_item_to_tabulate(self, item_type):
        """Select which survey/test to tabulate"""
        output_directory = f"outputs/{item_type}s"
        
        if not os.path.exists(output_directory):
            OutputHandler.output_line(f"No {item_type}s found.")
            return None
        
        list_of_files = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
        
        if len(list_of_files) == 0:
            OutputHandler.output_line(f"No {item_type}s found.")
            return None
        
        OutputHandler.output_line(f"Which {item_type} would you like to tabulate? Type the number next to the {item_type} name.")
        
        for i, filename in enumerate(list_of_files):
            OutputHandler.output_line(f"{i + 1}) {filename}")
        
        OutputHandler.output("\nFile number: ")
        file_index = InputHandler.get_console_int() - 1
        
        if 0 <= file_index < len(list_of_files):
            full_filename = list_of_files[file_index]
            return full_filename[:full_filename.rindex('.')]
        
        return None
    
    def tabulate_survey(self, folder_name):
        """Tabulate responses for a survey/test"""
        self.survey_responses = self.serializer.deserialize_surveys(folder_name)
        
        if len(self.survey_responses) == 0:
            return
        
        number_of_surveys = len(self.survey_responses)
        number_of_questions = len(self.survey_responses[0].get_questions())
        
        for question_number in range(number_of_questions):
            # For each question, get the answer from each response
            this_question_map = {}
            
            OutputHandler.output_line(f"\nQuestion {question_number + 1}: ")
            OutputHandler.output_line(self.survey_responses[0].get_questions()[question_number].get_prompt())
            
            # Loop through each survey and merge the question tabulation with this_question_map
            for survey_number in range(number_of_surveys):
                tab_map = self.survey_responses[survey_number].get_questions()[question_number].tabulate()
                
                if tab_map:
                    for key, value in tab_map.items():
                        this_question_map[key] = this_question_map.get(key, 0) + value
            
            self.survey_responses[0].get_questions()[question_number].display_tabulation(this_question_map)

