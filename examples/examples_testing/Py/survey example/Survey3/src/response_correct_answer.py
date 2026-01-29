from output_handler import OutputHandler

class ResponseCorrectAnswer:
    """Represents a response or correct answer with multiple string values"""
    
    def __init__(self):
        self.responses = []
    
    def display(self):
        """Display all responses"""
        for response in self.responses:
            OutputHandler.output_line(response)
    
    def get_responses(self):
        """Get the list of responses"""
        return self.responses
    
    def add_response(self, new_response):
        """Add a response and sort the list"""
        self.responses.append(new_response)
        self.responses.sort()
    
    def set_responses(self, responses):
        """Set the responses list"""
        self.responses = responses
    
    def __eq__(self, other):
        """Compare two ResponseCorrectAnswer objects"""
        if self is other:
            return True
        if other is None or not isinstance(other, ResponseCorrectAnswer):
            return False
        
        # Remove duplicates and lowercase everything to eliminate case sensitivity
        set1 = {str(r).lower() for r in self.responses}
        set2 = {str(r).lower() for r in other.responses}
        
        # Check if the two sets are the same size and contain all the same responses
        return len(set1) == len(set2) and set1 == set2

