# Contextual Prompting
#### Video Demo:  https://youtu.be/oCg5UzCPkCQ
#### Description:
##### html sites:
In the file i created there are 6 html files. They are named in the following paragraph with an explanation of what each of them does.
"layout.html" - Layout file for the entire page. imports the used javascript and css libraries.
"login.html" - The login page for the site
"register.html" - The register page for the site
"index.html" - The page for uploading your files to a directory named after your session id.
"chat.html" - The page used to chat with the AI about the file(s) you've uploaded.
"error.html" - page getting rendered if an error occurs with the attached error message.

##### Database setup
The database used for the program has 2 tables. The first one is called "users" and stores the id, username and hash value of the password for each user.
The second table is called "paragraphs". This database stores each question asked to the AI aswell as the received response. The table also records the id of the user that uses the chat and the time at which the question/response was received.

##### AI communication
Communication with the AI is done through the OpenAI API.
To give the AI contextual data, a RAG (Retrieval Augmented Generation) python package named llama-index is used. This package changes reads through the files content and combines the appropriate data into the prompt sent to the AI.

##### Improvements
To improve the project, features for deleting some specific files you've uploaded should be implemented. As of the current state, once uploaded to the server, the files cannot be deleted by the user.
Another improvement should be to update the questions through JavaScript instead of rendering new templates. This would make the chat more elegant and responsive.