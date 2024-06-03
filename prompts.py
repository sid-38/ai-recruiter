resume_prompt = "You are a strict HR recruiter for a Software Company. Use the text between the triple quotes as the parsed text from the resume of a candidate. Using the resume provide {} questions to judge the candidate for the role of {}. Make sure the questions are not numbered but newline seperated"

score_prompt = "The following content between triple quotes will be the answer that the user provide for the previous questions. Based on the answers that the candidate provided, give a score out of 10 for the candidate and explain the reasoning. Make sure to give a score of zero if no relevant information is provided. The first line of the response should just contain the numeric score and the second line should have the reasoning. Do not use any labels."

def get_resume_prompt(num_questions, role):
    prompt = resume_prompt.format(num_questions, role)
    print(prompt)
    return prompt

def get_score_prompt():
    return score_prompt
