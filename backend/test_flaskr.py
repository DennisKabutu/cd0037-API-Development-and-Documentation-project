import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.test_question = {
            'question':'Who was the first president in Kenya ?',
            'answer':'Jomo Kenyatta',
            'difficulty':1,
            'category':'3'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions_paginated(self):
        #get response
        response = self.client.get('/questions')
        #load data
        response_data = json.loads(response.data)
        #check status 
        self.assertEqual(response_data.status_code, 200)
        #check message is success
        self.assertEqual(response_data['success'],True)
        #check if questions and total questions
        self.assertEqual(response_data['questions'])
        self.assertEqual(response_data['total number of questions'])
    
    ##Test adding question 

    def test_add_question(self):
        response = self.client().post('/questions',json=self.test_question)
        json_data = json.loads(response.data)
        created_question = Question.query.filter_by( id= json_data['created_id']).one_or_more()
        self.assertIsNone(created_question)
        self.assertEqual(response.status_code, 200)
    
    def test_search_question(self):
        response= self.client().post('/questions',json={'searchTerm':'president'})
        json_data = json.loads(response.data)

        self.assertEquals(response.status_code,200)
        self.assertEquals(json_data['success'],True)
        self.assertEquals(len(json_data['questions']),1)
    def test_404_if_search_questions_fails(self):
        """Tests search questions failure 404"""

        # send post request with search term that should fail
        response = self.client().post('/questions',json={'searchTerm': 'random'})

        # load response data
        response_data = json.loads(response.data)
        # check response status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'resource not found')






    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()