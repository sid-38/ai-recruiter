import os
import pymupdf
from openai import OpenAI

client = OpenAI()

class AIRecruiter:
    num_questions = 2
    def __init__(self, file_path):
        self.file_path = file_path
        # CHECK IF PDF AND CHECK IF PARSABLE
        doc = pymupdf.open(self.file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.text = text

    def generate_questions(self):
        #Generating the questions
        # self.prompt = f'"""{self.text}"""\nGive 2 questions to judge the candidate\'s capability that can be used to score him later on'
        self.prompt = f'"""{self.text}"""'
        self.messages=[
                {"role": "system", "content": f"You are an HR employee for a Software Company. Use the text between the triple quotes as the parsed text from the resume of a candidate. Using the resume provide {AIRecruiter.num_questions} questions to judge the candidate for the role of Software Developer. Make sure the questions are not numbered but newline seperated"},
        {"role": "user", "content": self.prompt},
        ]

        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=self.messages
        )
        # Questions_text is required later in the chat history when asking AI for score
        self.questions_text = response.choices[0].message.content
        self.questions = [line for line in self.questions_text.splitlines() if line.strip()]
        print(self.questions)
        return(self.questions)

    def generate_score(self, answers):
        self.messages=[
            *(self.messages),
            {"role": "assistant", "content":self.questions_text},
            {"role": "system", "content": "The content between the triple quotes will be the answer that the user provided for the previous questions. Using the resume, the questions asked and the answers that the candidate provided, give a score out of 10 for the candidate and explain the reasoning. The first line of the response should just contain the score and the second line should have the reasoning"},
            {"role": "user", "content": f'"""{answers}"""'},
        ]
        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages = self.messages
        )
        score_analysis = response.choices[0].message.content.splitlines()
        self.score_analysis = {'score':score_analysis[0], 'reason':score_analysis[1]}
        return(self.score_analysis)

class MockAIRecruiter:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def generate_questions(self):
        self.questions = [line for line in "Question 1\n\n\nQuestion 2".splitlines() if line.strip()]
        return(self.questions)
    
    def generate_score(self,answers):
        score_analysis="7\nThe reason for your score is blah blah".splitlines()
        return({'score':score_analysis[0], 'reason':score_analysis[1]})



#file_path = "./Sidharth_Anil_resume.pdf"

## Parsing out the resume pdf
#doc = pymupdf.open(file_path)
#text = ""
#for page in doc:
#    text += page.get_text()
    
#print(text)

#client = OpenAI()

##Generating the questions
#prompt = f'"""{text}"""\nGive 2 questions to judge the candidate\'s capability that can be used to score him later on'

#response = client.chat.completions.create(
#  model="gpt-3.5-turbo",
#  messages=[
#    {"role": "system", "content": "You are an HR employee for a Software Company. Use the text between the triple quotes as the parsed text from the resume of a candidate to answer the question"},
#    {"role": "user", "content": prompt},
#  ]
#)
#questions = response.choices[0].message.content
#print(questions)

##Generating the score from the answers
#answers = input("Provide the answers to the questions")


#response = client.chat.completions.create(
#  model="gpt-3.5-turbo",
#  messages=[
#    {"role": "system", "content": "You are an HR employee for a Software Company. Use the text between the triple quotes as the parsed text from the resume of a candidate to answer the question"},
#    {"role": "user", "content": prompt},
#    {"role": "assistant", "content":questions},
#    {"role": "system", "content": "The content between the triple quotes will be the answer that the user provided for the previous questions"},
#    {"role": "user", "content": f'"""{answers}"""\nGive a score out of 10 for the candidate based on his answers and explain the reasoning'},
#  ]
#)
#print(response)

