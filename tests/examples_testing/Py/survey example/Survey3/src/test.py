from survey import Survey
from question import Question
from response_correct_answer import ResponseCorrectAnswer
from input_handler import InputHandler
from output_handler import OutputHandler
from multiple_choice_question import MultipleChoiceQuestion
from short_answer_question import ShortAnswerQuestion
from valid_date_question import ValidDateQuestion
from matching_question import MatchingQuestion

class Test(Survey):
    """Test class - extends Survey with correct answers and grading"""
    
    def __init__(self, name):
        super().__init__(name)
        self.correct_answers = []
    
    @staticmethod
    def create():
        """Create a new test"""
        OutputHandler.output("\nTime to create a new test. Please provide a test name: ")
        test_name = InputHandler.get_console_string()
        
        OutputHandler.output("How many questions would you like on your test: ")
        question_amount = InputHandler.get_console_int()
        if question_amount <= 0 or question_amount > 50:
            OutputHandler.output_line("Invalid question amount, we accept 1-50 questions. Cancelling test creation.")
            return None
        
        our_new_test = Test(test_name.replace(" ", "_"))
        
        for i in range(question_amount):
            new_question = Question.create()
            if new_question is not None:
                our_new_test.add_question(new_question)
            else:
                # Break out of loop
                break
        
        return our_new_test
    
    def modify(self):
        """Modify the test"""
        # Before modifying, delete old responses
        import os
        directory = f"outputs/responses/{self.survey_name}"
        self.delete_responses(directory)
        
        OutputHandler.output_line("\nChoose a modify option:")
        OutputHandler.output_line("1. Modify name")
        OutputHandler.output_line("2. Modify a question")
        OutputHandler.output_line("3. Modify a question's correct answer")
        OutputHandler.output_line("4. Add a question")
        OutputHandler.output_line("5. Delete a question")
        selected_option = InputHandler.get_console_int()
        
        if selected_option == 1:
            self.modify_survey_name()
        elif selected_option == 2:
            OutputHandler.output("\nEnter the number of the question you'd like to modify:")
            question_mod_index = InputHandler.get_console_int()
            self.modify_question(question_mod_index)
        elif selected_option == 3:
            OutputHandler.output("\nEnter the number of the question you'd like to modify the correct answer: ")
            question_ca_mod_index = InputHandler.get_console_int()
            if 1 <= question_ca_mod_index <= len(self.questions):
                self.modify_correct_answer(question_ca_mod_index - 1)
            else:
                OutputHandler.output_line("Invalid question number.")
        elif selected_option == 4:
            new_question = Question.create()
            if new_question is not None:
                self.add_question(new_question)
        elif selected_option == 5:
            OutputHandler.output("\nEnter the number of the question you'd like to remove: ")
            question_remove_number = InputHandler.get_console_int()
            self.remove_question(question_remove_number)
        else:
            OutputHandler.output_line("Unrecognized input. Please try again.\n")
    
    def add_question(self, question):
        """Add a question to the test and prompt for correct answer"""
        super().add_question(question)
        
        if isinstance(question, (ShortAnswerQuestion, ValidDateQuestion, MultipleChoiceQuestion)):
            OutputHandler.output_line("\nYour question will look like this: ")
            question.display()
            OutputHandler.output_line("")
            
            if isinstance(question, MultipleChoiceQuestion):
                OutputHandler.output("Please enter the letter of the correct answer(s). If multiple correct answers required, separate them by a comma: ")
                
                while True:
                    correct_answer_string = InputHandler.get_console_string()
                    
                    if question.is_valid_answer(correct_answer_string):
                        rca = ResponseCorrectAnswer()
                        str_split = correct_answer_string.lower().split(",")
                        
                        response_list = []
                        for choice_str in str_split:
                            choice_index = ord(choice_str.strip()[0]) - ord('a')
                            response_list.append(question.get_choices()[choice_index])
                        
                        rca.set_responses(response_list)
                        self.add_correct_answer(rca)
                        break
                    else:
                        OutputHandler.output("Invalid answer(s), try again: ")
            
            else:
                OutputHandler.output_line("Please enter the correct answer(s). If multiple correct answers required, separate them by a comma: ")
                
                while True:
                    correct_answer_string = InputHandler.get_console_string()
                    
                    if question.is_valid_answer(correct_answer_string):
                        rca = ResponseCorrectAnswer()
                        str_split = correct_answer_string.lower().split(",")
                        str_list = [s.strip() for s in str_split]
                        rca.set_responses(str_list)
                        
                        self.add_correct_answer(rca)
                        break
                    else:
                        OutputHandler.output("Invalid answer(s), try again: ")
        
        elif isinstance(question, MatchingQuestion):
            rca = ResponseCorrectAnswer()
            
            OutputHandler.output_line("\nYour question will look like this: ")
            question.display()
            OutputHandler.output_line("")
            
            original_pairs = question.get_original_pairs()
            
            OutputHandler.output_line("Correct Answers: ")
            for pair in original_pairs:
                OutputHandler.output_line(pair)
            
            rca.set_responses(original_pairs)
            self.add_correct_answer(rca)
        else:
            # Essay question: No correct answer
            self.add_correct_answer(None)
    
    def remove_question(self, question_num):
        """Remove a question by number"""
        index = question_num - 1
        if len(self.questions) == 1:
            OutputHandler.output_line("Cannot remove the only remaining question.")
        elif 0 <= index < len(self.questions):
            super().remove_question(question_num)
            self.correct_answers.pop(index)
        else:
            OutputHandler.output_line("Could not remove a question with that number. Try again")
    
    def display_with_correct_answers(self):
        """Display the test with correct answers"""
        OutputHandler.output_line(f"\n------ {self.survey_name} ------")
        for i, question in enumerate(self.questions):
            OutputHandler.output_line(f"\nQuestion #{i + 1}")
            question.display()
            
            if i < len(self.correct_answers) and self.correct_answers[i] is not None:
                responses = self.correct_answers[i].get_responses()
                result = ", ".join(responses)
                OutputHandler.output_line(f"Correct Answer: {result}")
        OutputHandler.output_line("\n------ the end -------")
    
    def modify_correct_answer(self, index):
        """Modify the correct answer for a question"""
        current_correct_answer = self.correct_answers[index]
        if current_correct_answer is None:
            OutputHandler.output_line("This question cannot have a correct answer.")
        else:
            self.questions[index].display()
            OutputHandler.output("Current correct answer(s):\n")
            current_correct_answer.display()
            OutputHandler.output("")
            
            new_answer_array = []
            if len(current_correct_answer.get_responses()) == 1:
                OutputHandler.output("Enter the new correct answer: ")
                while True:
                    new_answer = InputHandler.get_console_string()
                    if self.questions[index].is_valid_answer(new_answer):
                        if isinstance(self.questions[index], MultipleChoiceQuestion):
                            choice_index = ord(new_answer.lower()[0]) - ord('a')
                            new_answer_array.append(self.questions[index].get_choices()[choice_index])
                        else:
                            new_answer_array.append(new_answer)
                        self.correct_answers[index].set_responses(new_answer_array)
                        OutputHandler.output_line("Correct answer updated.")
                        break
                    else:
                        OutputHandler.output("Invalid input, try again: ")
            else:
                OutputHandler.output_line(f"This question has {len(current_correct_answer.get_responses())} correct answers.")
                for i, old_answer in enumerate(current_correct_answer.get_responses()):
                    OutputHandler.output_line(f"Modify correct answer #{i+1} (enter Y or N): ")
                    decision = InputHandler.get_yn_console_input()
                    if decision:
                        OutputHandler.output("Enter the new correct answer: ")
                        while True:
                            new_answer = InputHandler.get_console_string()
                            if self.questions[index].is_valid_answer(new_answer):
                                if isinstance(self.questions[index], MultipleChoiceQuestion):
                                    choice_index = ord(new_answer.lower()[0]) - ord('a')
                                    new_answer_array.append(self.questions[index].get_choices()[choice_index])
                                else:
                                    new_answer_array.append(new_answer)
                                OutputHandler.output_line("Correct answer updated.")
                                break
                            else:
                                OutputHandler.output("Invalid input, try again: ")
                    else:
                        new_answer_array.append(old_answer)
                self.correct_answers[index].set_responses(new_answer_array)
                OutputHandler.output_line("Correct answers updated.")
    
    def grade(self):
        """Grade the test"""
        gradable_points = 0.0
        points_scored = 0.0
        ungradable_questions = 0
        
        value_of_one_question = 100.0 / len(self.questions)
        
        for i, question in enumerate(self.questions):
            if i < len(self.correct_answers) and self.correct_answers[i] is not None:
                gradable_points += value_of_one_question
                
                if self.correct_answers[i] == question.get_user_response():
                    points_scored += value_of_one_question
            else:
                ungradable_questions += 1
        
        OutputHandler.output_line(f"You received a {points_scored:.2f} on the test.")
        if ungradable_questions > 0:
            OutputHandler.output_line(f"The test was worth 100 points, but only {gradable_points:.2f} of those points could be auto graded because there was {ungradable_questions} essay question(s).")
    
    def get_correct_answers(self):
        """Get the list of correct answers"""
        return self.correct_answers
    
    def set_correct_answers(self, correct_answers):
        """Set the list of correct answers"""
        self.correct_answers = correct_answers
    
    def add_correct_answer(self, rca):
        """Add a correct answer"""
        self.correct_answers.append(rca)

