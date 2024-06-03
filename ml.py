import os
import time
import pymupdf
import sys
import json
from openai import OpenAI
import prompts

with open("./config.json", 'r') as f:
    CONFIG = json.load(f)


if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OpenAI API key as the environment variable OPENAI_API_KEY")
    sys.exit(1)

client = OpenAI()

class AIRecruiter:
    def __init__(self, file_path, role):
        self.file_path = file_path
        self.role = role

        # Parsing the PDF
        # TODO: CHECK IF PDF AND CHECK IF PARSABLE
        doc = pymupdf.open(self.file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.text = text

    def generate_questions(self):
        self.prompt = f'"""{self.text}"""'
        system_prompt = prompts.get_resume_prompt(CONFIG['NUM_QUESTIONS'], self.role)

        # Storing the messages in the object, to recall later during the score generation phase
        self.messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": self.prompt},
        ]

        response = client.chat.completions.create(
          model=CONFIG["OPENAI_MODEL"],
          messages=self.messages
        )

        # Questions_text is required later in the chat history when asking AI for score
        self.questions_text = response.choices[0].message.content
        self.questions = [line for line in self.questions_text.splitlines() if line.strip()]
        return(self.questions)

    def generate_score(self, answers):
        system_prompt = prompts.get_score_prompt()
        self.messages=[
            *(self.messages),
            {"role": "assistant", "content":self.questions_text},
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f'"""{answers}"""'},
        ]
        response = client.chat.completions.create(
          model=CONFIG["OPENAI_MODEL"],
          messages = self.messages
        )
        score_analysis = response.choices[0].message.content.splitlines()
        self.score_analysis = {'score':score_analysis[0], 'reason':score_analysis[1]}
        return(self.score_analysis)

class MockAIRecruiter:
    def __init__(self, file_path, role):
        self.file_path = file_path
        self.role = role
    
    def generate_questions(self):
        time.sleep(5)
        self.questions = [line for line in "Question 1\n\n\nQuestion 2".splitlines() if line.strip()]
        return(self.questions)
    
    def generate_score(self,answers):
        time.sleep(5)
        score_analysis="7\nThe reason for your score is blah blah".splitlines()
        return({'score':score_analysis[0], 'reason':score_analysis[1]})

