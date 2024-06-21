# Tax Filing Assistant


## Junior AI Engineer Project Assignment

The objective of this project is to develop a simple tax filing assistant web application
using Python and modern web frameworks. 
It is part of the interview proccess for the position of Junior AI Engineer at Deloitte.
The application will leverage a generative AI model from
OpenAI to provide users with basic tax advice based on their input.

Each Branch is split into the different steps of the assessment

### 02-Implementing REST APIs

This branch contains the implementation of a basic form to handle the submition of data from the user. Additionally the branch containts the implementation of backend validation and storing the data in a local database in the form of sqlite file.

In order to run this locally you need to have `python 3.12` installed on your machine.

Additionaly you need to install the libraries described in the requirements.txt using `pip install -r requirements.txt`

Finally you can run the server using `uvicorn app.main:app --reload` or by using one of the provided scripts depending on your operating system.

If using a unix operating system make sure to make the script excecutable by running `chmod +x run.sh` And start the application using `./run.sh`

Navigate to the browser at the address `http://127.0.0.1:8000`.