class InputHandler:
    """Handles console input with validation"""
    
    @staticmethod
    def get_console_int():
        """Get an integer from console input"""
        while True:
            try:
                value = int(input())
                return value
            except ValueError:
                print("Please input a number! Try again..")
    
    @staticmethod
    def get_console_int_less_than(integer_limit):
        """Get an integer from console input that is less than the limit"""
        while True:
            try:
                value = int(input())
                if value > integer_limit:
                    print(f"Maximum value is {integer_limit}! Try again..")
                    continue
                return value
            except ValueError:
                print("Please input a number! Try again..")
    
    @staticmethod
    def get_console_string():
        """Get a non-empty string from console input"""
        while True:
            value = input().strip()
            if value:
                return value
    
    @staticmethod
    def safe_to_split(input_str):
        """Check if a string can be safely split by comma"""
        try:
            parts = input_str.split(",")
            if len(parts) >= 2:
                return True
            return False
        except (IndexError, AttributeError):
            return False
    
    @staticmethod
    def get_yn_console_input():
        """Get Y/N input from console"""
        while True:
            decision = input().strip().lower()
            if decision == "y":
                return True
            elif decision == "n":
                return False
            print("Please input Y or N! Try again..")
    
    @staticmethod
    def get_multiple_choice_input(choice_amt):
        """Get a multiple choice letter input"""
        possible_choices = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        valid_choices = possible_choices[:choice_amt]
        
        while True:
            decision = input().strip().lower()
            if decision in valid_choices:
                return decision
            print("Please input a letter in the range of choices..")

