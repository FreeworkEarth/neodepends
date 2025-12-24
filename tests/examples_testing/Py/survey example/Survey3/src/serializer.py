import os
import pickle
from survey import Survey
from test import Test
from input_handler import InputHandler
from output_handler import OutputHandler

class Serializer:
    """Handles serialization and deserialization of surveys and tests"""
    
    def load_survey(self):
        """Load a survey from file"""
        loaded_survey = None
        try:
            output_directory = "outputs/surveys"
            if not os.path.exists(output_directory):
                OutputHandler.output_line("No saved surveys found (outputs/surveys directory empty)")
                return None
            
            list_of_files = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
            
            if len(list_of_files) == 0:
                OutputHandler.output_line("No saved surveys found (outputs/surveys directory empty)")
                return None
            
            OutputHandler.output_line("Which file would you like to load from? Type the number next to the file name.")
            
            for i, filename in enumerate(list_of_files):
                OutputHandler.output_line(f"{i + 1}) {filename}")
            
            OutputHandler.output("\nFile number: ")
            file_index = InputHandler.get_console_int() - 1
            
            if 0 <= file_index < len(list_of_files):
                input_file = os.path.join(output_directory, list_of_files[file_index])
                
                with open(input_file, 'rb') as f:
                    loaded_survey = pickle.load(f)
                
                OutputHandler.output_line(f"{loaded_survey.get_name()} is now the current survey!")
                return loaded_survey
            else:
                OutputHandler.output_line("Invalid file number.")
                return None
        
        except FileNotFoundError:
            OutputHandler.output_line("We encountered a problem trying to load the survey. (FileException)")
        except Exception as e:
            OutputHandler.output_line(f"We encountered a problem trying to load the survey. ({str(e)})")
        
        return loaded_survey
    
    def load_test(self):
        """Load a test from file"""
        loaded_test = None
        try:
            output_directory = "outputs/tests"
            if not os.path.exists(output_directory):
                OutputHandler.output_line("No saved tests found (outputs/tests directory empty)")
                return None
            
            list_of_files = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
            
            if len(list_of_files) == 0:
                OutputHandler.output_line("No saved tests found (outputs/tests directory empty)")
                return None
            
            OutputHandler.output_line("Which file would you like to load from? Type the number next to the file name.")
            
            for i, filename in enumerate(list_of_files):
                OutputHandler.output_line(f"{i + 1}) {filename}")
            
            OutputHandler.output("\nFile number: ")
            file_index = InputHandler.get_console_int() - 1
            
            if 0 <= file_index < len(list_of_files):
                input_file = os.path.join(output_directory, list_of_files[file_index])
                
                with open(input_file, 'rb') as f:
                    loaded_test = pickle.load(f)
                
                OutputHandler.output_line(f"{loaded_test.get_name()} is now the current test!")
                return loaded_test
            else:
                OutputHandler.output_line("Invalid file number.")
                return None
        
        except FileNotFoundError:
            OutputHandler.output_line("We encountered a problem trying to load the test. (FileException)")
        except Exception as e:
            OutputHandler.output_line(f"We encountered a problem trying to load the test. ({str(e)})")
        
        return loaded_test
    
    def load_test_response(self, test_name, test_response_name):
        """Load a test response from file"""
        loaded_test = None
        try:
            output_directory = f"outputs/responses/{test_name}"
            input_file = os.path.join(output_directory, test_response_name)
            
            with open(input_file, 'rb') as f:
                loaded_test = pickle.load(f)
            
            return loaded_test
        
        except FileNotFoundError:
            OutputHandler.output_line("We encountered a problem trying to load the test. (FileException)")
        except Exception as e:
            OutputHandler.output_line(f"We encountered a problem trying to load the test. ({str(e)})")
        
        return loaded_test
    
    def deserialize_surveys(self, folder_name):
        """Deserialize all survey responses from a folder"""
        surveys = []
        
        output_directory = f"outputs/responses/{folder_name}"
        if not os.path.exists(output_directory):
            OutputHandler.output_line("No survey responses found for your selection.")
            return []
        
        try:
            list_of_files = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
            
            for filename in list_of_files:
                input_file = os.path.join(output_directory, filename)
                
                with open(input_file, 'rb') as f:
                    loaded_survey = pickle.load(f)
                    surveys.append(loaded_survey)
        
        except Exception as e:
            OutputHandler.output_line(f"We encountered a problem trying to load the survey. ({str(e)})")
        
        OutputHandler.output_line(f"{len(surveys)} responses found.")
        return surveys
    
    def save(self, survey_to_save, save_type, silent=False):
        """Save a survey or test to file"""
        try:
            output_directory = f"outputs/{save_type}s"
            os.makedirs(output_directory, exist_ok=True)
            
            output_file = os.path.join(output_directory, f"{survey_to_save.get_name()}.{save_type}")
            
            with open(output_file, 'wb') as f:
                pickle.dump(survey_to_save, f)
            
            if not silent:
                OutputHandler.output_line(f"Success! Your {save_type} has been saved as a file named: {survey_to_save.get_name()}.{save_type}")
        
        except Exception as e:
            OutputHandler.output_line(f"We encountered a problem trying to save. ({str(e)})")
    
    def save_survey_response(self, survey_response_to_save):
        """Save a survey response to file"""
        try:
            output_directory = f"outputs/responses/{survey_response_to_save.get_name()}"
            os.makedirs(output_directory, exist_ok=True)
            
            response_filename = f"{survey_response_to_save.get_name()}-resp-{survey_response_to_save.get_times_taken() + 1}.response"
            output_file = os.path.join(output_directory, response_filename)
            
            with open(output_file, 'wb') as f:
                pickle.dump(survey_response_to_save, f)
            
            OutputHandler.output_line(f"\nAll Done! Your response has been saved as a file named: {response_filename}")
        
        except Exception as e:
            OutputHandler.output_line(f"We encountered a problem trying to save the survey. ({str(e)})")
    
    def save_test_response(self, test_response_to_save):
        """Save a test response to file"""
        try:
            output_directory = f"outputs/responses/{test_response_to_save.get_name()}"
            os.makedirs(output_directory, exist_ok=True)
            
            response_filename = f"{test_response_to_save.get_name()}-resp-{test_response_to_save.get_times_taken() + 1}.response"
            output_file = os.path.join(output_directory, response_filename)
            
            with open(output_file, 'wb') as f:
                pickle.dump(test_response_to_save, f)
            
            OutputHandler.output_line(f"\nAll Done! Your response has been saved as a file named: {response_filename}")
        
        except Exception as e:
            OutputHandler.output_line(f"We encountered a problem trying to save the test. ({str(e)})")

