# Tax Filing Assistant


## Junior AI Engineer Project Assignment

The objective of this project is to develop a simple tax filing assistant web application
using Python and modern web frameworks. 
It is part of the interview proccess for the position of Junior AI Engineer at Deloitte.
The application will leverage a generative AI model from
OpenAI to provide users with basic tax advice based on their input.

Each Branch is split into the different steps of the assessment

### 06-Documentation

This branch aims to provide documentation about the project and provide a presentation of the implementation of the various tasks

## AI Integration

Open integration is achieved by maaking a GET request to the `/get_all_advice` endpoint. As long as the `OPENAI-API-KEY` enviromental variable is set to a valid OpenAI key, a model is created with instructions to give financial advice based on the entries present in the database. A response is generated and forwarded to the `advice.html` page where it is displayed.


## Github workflow 

- Added workflow to run some tests at the `full_tests.yml` file. They run on every push request and any pull requests and branching of the main branch.

## Tests

- Added tests which test the validation functions and mock the connection to the datapase to test the endpoints. You can manually run the tests using the included scripts `run_tests` or by using the command `python -B -m pytest`


## Endpoints

### Home Page

**GET /**

- **Description:** Displays the home page with a form to submit tax information and a table of current entries.
- **Response:** HTML page

### Submit Tax Information

**POST /submit/**

- **Description:** Submits tax information to be saved in the database.
- **Form Data:**
  - `income` (float, required): The income amount.
  - `expenses` (float, required): The expenses amount.
  - `tax_rate` (float, optional, default=24): The tax rate percentage.
  - `description` (str, optional): A description of the income or expense.
- **Response:** Redirects to the home page.
- **Example Request:**

    ```bash
    curl -X POST "http://127.0.0.1:8000/submit/" -F "income=1000" -F "expenses=500" -F "tax_rate=24" -F "description=Office Supplies"
    ```

### Delete Entry

**POST /delete/{entry_id}**

- **Description:** Deletes a specific tax entry by its ID.
- **Path Parameter:**
  - `entry_id` (int, required): The ID of the entry to delete.
- **Response:** Redirects to the home page.
- **Example Request:**

    ```bash
    curl -X POST "http://127.0.0.1:8000/delete/1"
    ```

### Clear All Entries

**POST /clear_all/**

- **Description:** Deletes all tax entries from the database.
- **Response:** Redirects to the home page.
- **Example Request:**

    ```bash
    curl -X POST "http://127.0.0.1:8000/clear_all/"
    ```

### Get All Advice

**GET /get_all_advice**

- **Description:** Fetches tax advice based on all the current entries in the database.
- **Response:**
  - **200 OK**
    - `advice` (List[str]): A list of advice generated based on the tax entries.

## Database Schema

The database schema includes the following fields:

- `id` (int, primary key): The unique identifier for each entry.
- `income` (float, not nullable): The income amount.
- `expenses` (float, not nullable): The expenses amount.
- `tax_amount` (float, not nullable): The calculated tax amount.
- `tax_rate` (float, not nullable): The tax rate percentage.
- `description` (str, nullable): A description of the income or expense.

### Running the Application

- In order to run this locally you need to have `docker` installed on your machine and running.

- Set up enviromental variables at the file `.env.local` and place the file next to the dockerfile.
```
DATABASE_URL=sqlite:///./app/db.sqlite
```
```
OPENAI-API-KEY=YOUR API KEY
```
- Create the image by running `docker-compose build`
- Run the container `docker-compose up`
- Navigate to the browser at the address `http://127.0.0.1:8000`.

- To stop the container run the commant `docker-compose down`

Alternatively you can run the provided scripts to start `go.bat or go.sh` and stop the service `stop.bat or stop.sh`.