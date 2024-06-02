import os
import pymupdf
from openai import OpenAI

client = OpenAI()

class AIRecruiter:
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
        self.prompt = f'"""{self.text}"""\nGive 2 questions to judge the candidate\'s capability that can be used to score him later on'
        self.messages=[
        {"role": "system", "content": "You are an HR employee for a Software Company. Use the text between the triple quotes as the parsed text from the resume of a candidate to answer the question"},
        {"role": "user", "content": self.prompt},
        ]

        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=self.messages
        )
        self.questions = response.choices[0].message.content
        return(self.questions)

    def generate_score(self, answers):
        self.messages=[
            *(self.messages),
            {"role": "assistant", "content":self.questions},
            {"role": "system", "content": "The content between the triple quotes will be the answer that the user provided for the previous questions"},
            {"role": "user", "content": f'"""{answers}"""\nGive a score out of 10 for the candidate based on his answers and explain the reasoning'},
        ]
        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages = self.messages
        )
        self.score_analysis = response.choices[0].message.content
        return(self.score_analysis)

class MockAIRecruiter:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def generate_questions(self):
        self.questions = "1.Question 1\n2.Question 2"
        return(self.questions)
    
    def generate_score(self,answers):
        return("Here's your score")



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

