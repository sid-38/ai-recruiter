# DESIGN DECISIONS
## Machine Learning Model
An ML model is required for the question generation, and scoring the candidate based on the answers. Since an OpenAI API Key was offerred as part of the task, I went with the default model gpt-3.5-turbo 

## Resume parsing
There are two potential ways to achieve this. Either I could include the resume as a file attachment and query the OpenAI model in which case the model would parse out the information from the pdf. The next way is to use an already existing solution to parse out the text from the pdf before querying the ML Model. The first route, where the ML model parses out the pdf would have limitations on the token as well as possibly incur higher charges. So, I went with the second option and used the package PyMuPDF to parse out the text from the resume

## Frontend tech stack
The frontend aspect of this webpage is fairly simple and so I did not want to utilize libraries like ReactJS, as I thought it might be an overkill (this might be debatable). Using bootstrap css, jquery and html was enough to achieve the functionalities required. Another decision was whether to use a multi-page frontend or a single-page application. Since the task phrased it as "Create a Page", and because I thought that a single-page application logic for this particular task would not be too complicated, I implemented the frontend as a single page application using AJAX and JQuery to hide and show the relevant information.

# FUTURE WORKS
1. CORS should be made more restrictive. Right now Flask-CORS allows any origin, which during prod would be a security concern. At that point, depending on the manner of frontend hosting, CORS should be configured so that only the relevant origin would have access to the resource
2. Test cases must be written for the project.
3. The ML models could be utilized to confirm that the submitted pdf is in fact a resume. Right now, regardless of the content of the pdf, it is treated as a resume
4. Custom error messages should be displayed. At the moment, a generic "Could not process the request" error is displayed. 
