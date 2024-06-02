import os
import pymupdf
from openai import OpenAI

file_path = "./Sidharth_Anil_resume.pdf"

# Parsing out the resume pdf
doc = pymupdf.open(file_path)
text = ""
for page in doc:
    text += page.get_text()
    
print(text)

client = OpenAI()

#Generating the questions
prompt = f'"""{text}"""\nGive 2 questions to judge the candidate\'s capability that can be used to score him later on'

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an HR employee for a Software Company. Use the text between the triple quotes as the parsed text from the resume of a candidate to answer the question"},
    {"role": "user", "content": prompt},
  ]
)
questions = response.choices[0].message.content
print(questions)

#Generating the score from the answers
answers = input("Provide the answers to the questions")


response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an HR employee for a Software Company. Use the text between the triple quotes as the parsed text from the resume of a candidate to answer the question"},
    {"role": "user", "content": prompt},
    {"role": "assistant", "content":questions},
    {"role": "system", "content": "The content between the triple quotes will be the answer that the user provided for the previous questions"},
    {"role": "user", "content": f'"""{answers}"""\nGive a score out of 10 for the candidate based on his answers and explain the reasoning'},
  ]
)
print(response)

