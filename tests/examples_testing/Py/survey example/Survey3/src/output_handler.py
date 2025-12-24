class OutputHandler:
    """Handles console output formatting"""
    
    @staticmethod
    def output_line(output):
        """Print a line to console"""
        print(output)
    
    @staticmethod
    def output(output_str):
        """Print without newline"""
        print(output_str, end="")
    
    @staticmethod
    def output_spaced_strings(output1, output2):
        """Print two strings with spacing"""
        formatted_output1 = f"{output1:<20}"
        OutputHandler.output_line(formatted_output1 + output2)

