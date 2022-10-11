from django.db import models


# Answers must be written out within 200 characters of text.
# An answer may be pulled randomly for any question as a false answer.
class Answer(models.Model):
    answer_text: = models.CharField(max_length=200)

    def __str__(self):
        return self.answer_text


# The question must be phrased and written in less than 200 characters of text.
# The correct_answer will be pulled along with 3 decoy answers.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    correct_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
    
    def _get_correct_answer(self):
        return self.correct_answer

