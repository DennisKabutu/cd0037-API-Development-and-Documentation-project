# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
### Getting Started

* Base URL: This application is hosted locally at `http://127.0.0.1:5000/`
* Authentication: This version does not require API keys.

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable

### Endpoints

#### GET /categories

* General: Returns a list of categories ordered by Category ID.
* Sample: `curl http://127.0.0.1:5000/categories`<br>

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "success": true
        }


#### GET /questions

* General:
  * Returns a list questions,list of categories and total number of questions.
  * Results are paginated 10 per group.
* Sample: `curl http://127.0.0.1:5000/questions`<br>

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "questions": [
                {
                    "answer": "Mardid", 
                    "category": 3, 
                    "difficulty": 1, 
                    "id": 164, 
                    "question": "What is the capital city of Spain?"
                }, 
                {
                    "answer": "10,000", 
                    "category": 1, 
                    "difficulty": 1, 
                    "id": 9, 
                    "question": "About how many taste buds does the average human tongue have?"
                }, 
                {
                    "answer": "Bing", 
                    "category": 5, 
                    "difficulty": 4, 
                    "id": 2, 
                    "question": "What is Chandler’s last name in the sitcom Friends?"
                }, 
                {
                    "answer": "Red, white, and blue.", 
                    "category": 3, 
                    "difficulty": 4, 
                    "id": 4, 
                    "question": "What colors are the Norwegian flag?"
                }, 
                {
                    "answer": "Daintree Forest north of Cairns, Australia.", 
                    "category": 5, 
                    "difficulty": 3, 
                    "id": 6, 
                    "question": "Where would you find the world’s most ancient forest?"
                }, 
                {
                    "answer": "Brazil", 
                    "category": 6, 
                    "difficulty": 3, 
                    "id": 10, 
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                }, 
                {
                    "answer": "Fleming.", 
                    "category": 1, 
                    "difficulty": 2, 
                    "id": 11, 
                    "question": " Who discovered penicillin?"
                }, 
                {
                    "answer": "7", 
                    "category": 4, 
                    "difficulty": 2, 
                    "id": 12, 
                    "question": "Pure water has a pH level of around?"
                }, 
                {
                    "answer": "Lake Victoria", 
                    "category": 3, 
                    "difficulty": 2, 
                    "id": 13, 
                    "question": "What is the largest lake in Africa?"
                }, 
                {
                    "answer": "P Diddy", 
                    "category": 6, 
                    "difficulty": 3, 
                    "id": 23, 
                    "question":"Which name is rapper Sean Combs better known by?"
                }
            ], 
            "success": true, 
            "total_questions": 19
        }

#### DELETE /questions/\<int:id\>

* General:
  * Deletes a question of the specified id in request parameters in the JSON object.
  * Returns id of deleted question upon success alongside with the message success.
* Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`<br>

        {
            "deleted_id": 6, 
            "success": true
        }

#### POST /questions

This endpoint either creates a new question or returns search results.

1. If <strong>no</strong> search term is included in request the create new question request will run
2. Bad request <strong> 404 error</strong> will be return with the correct JSON request params are ommitted.

* General:
  * Creates a new question using JSON request parameters.
  * Returns JSON object with newly created question, as well as paginated questions.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "Who starts first in chess?",
            "answer": "White",
            "difficulty": 6,
            "category": "3"
        }'`<br>

         {
            "created_id": 36, 
            "success": true
        }

2. If search term <strong>is</strong> included in JSON request parameters:

* General:
  * Searches for questions using search term in the JSON request parameter.
  * Returns JSON object with paginated search results that match the query.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Youtube"}'`<br>

        {
            "questions": [
                {
                    "answer": "Despacito", 
                    "category": 2, 
                    "difficulty": 4, 
                    "id": 13, 
                    "question": " Which song by Luis Fonsi and Daddy Yankee has the most views (of all time) on YouTube"
                }, 
               
        {       
               
            "success": true
        }

## Authors

Dennis Kimani Kabutu authored  the following files
1. API (`__init__.py`),
2. test suite (`test_flaskr.py`) *not yet completed*
3. and this README.<br>


All other project files, including the models and frontend, were created by the [Udacity] team (https://www.udacity.com/) as a project template for the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) for the Trivia Project to test API Development and Documentation.

Free feel to leave any feedback and tips for improvement 