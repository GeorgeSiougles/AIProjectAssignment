# Tax Filing Assistant

## 01-Web Application Setup

This branch contains the implementation of a basic form to handle the submition of data from the user.

In order to run this locally you need to have `python 3.12` installed on your machine.

Additionaly you need to install the libraries described in the requirements.txt using pip
`pip install fastapi uvicorn jinja2 pydantic`

Finally you can run the server using `uvicorn app.main:app --reload` or by using one of the provided scripts depending on your operating system.

If using a unix operating system make sure to make the script excecutable by running `chmod +x run.sh` And start the application using `./run.sh`

Navigate to the browser at the address `http://127.0.0.1:8000`.