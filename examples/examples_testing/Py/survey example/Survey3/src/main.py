from survey_menu import SurveyMenu
from test_menu import TestMenu
from input_handler import InputHandler
from output_handler import OutputHandler

def main():
    """Main entry point for the Survey System"""
    while True:
        OutputHandler.output_line("\nWelcome. Please type the number of an option below:")
        OutputHandler.output_line("1. Survey")
        OutputHandler.output_line("2. Test")
        
        chosen_option = InputHandler.get_console_int()
        
        if chosen_option == 1:
            sm = SurveyMenu()
            sm.present_menu()
        elif chosen_option == 2:
            tm = TestMenu()
            tm.present_menu()
        else:
            OutputHandler.output_line("Unrecognized input. Please try again.\n")

if __name__ == "__main__":
    main()

