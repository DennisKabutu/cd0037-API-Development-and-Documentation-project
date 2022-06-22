from ast import Pass
import re
from tracemalloc import start
from unicodedata import category
from click import Abort
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selected_list):
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    paginated_questions = [question.format() for question in selected_list]
    return paginated_questions[start:end] 



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
     Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'api/*:{"origins":"*"}'})
   

    """
     Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Header','GET,POST,PUT,PATCH,DELETE,OPTIONS')
        return response

    #an endpoint to handle GET requests for all available categories.
    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        try:
            ## query the database for all categories 
            categories = Category.query.order_by(Category.type).all()
            ##  Check list is not empty  loop through it and format as result 
            ##  if empty throw a 404 error 
            if categories:

                all_categories = {}
                for category in categories:
                #Append category with ID as the  Key and type as Value 
                    all_categories[category.id] = category.type
                return jsonify({
                    'success':True,
                    'categories':all_categories
                })
            else:
                 abort(404)
        except:
              abort(422)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions',methods=['GET'])
    def get_all_questions():
        try:
        ##get list of questions paginated 10 question
            questions = Question.query.order_by(Question.id).all()
            if questions:
                paginated_questions = paginate_questions(request,questions)
            else:
                abort(404)
        #get categories using the get_all_categories method 
            categories = Category.query.order_by(Category.type).all()
            if categories:
           ## all_categories = [category.format() for category in categories]
                all_categories = {}
                for category in categories:
                    all_categories[category.id] = category.type
            else:
                abort(404)
        except:
            abort(422)


            # return list of questions  
        return jsonify({
            "success":True,
            "question":paginated_questions,
            "number of total questions":len(Question.query.all()),
            "category":all_categories,
        })
    
      

    """
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def get_specific_plant(question_id):

        question = Question.query.filter(Question.id==question_id).one_or_none()

        if question is None:
            abort(404)
        else:
            Question.delete(question)  

            return jsonify({
                'success': True,
               ## 'question': question.format(),
            })

    

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods = ['POST'])
    def create_question():
        data = request.get_json()

        try:
            question = Question(
                question = data.get('question',None),
                answer = data.get('answer',None),
                category = data.get('category',None),
                difficulty= data.get('difficulty',None)
            )

            Question.insert(question)

            selected_questions = Question.query.order_by(Question.id).all()
            #@ TODO Paginated question function not added
            formatted_questions = [ question.format() for question in selected_questions]

            return jsonify({
                'success':True,
                'questions': formatted_questions,
                'created':question.id,
                'total_question':len(selected_questions)
            })
        except:
            Abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions',methods = ['POST'])
    def search_question():

        body = request.get_json()
        if (body.get('searchTerm')):
            search_term = body.get('searchTerm')

            selection = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')
            ).all()

            if (len(selection) == 0):
                abort(404)
            
            formatted_question = paginate_questions(request,selection)

            return jsonify({
                'success':True,
                'question':formatted_question,
                'total_question':len(Question.query.all())

            })
        

    """
  
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions' ,methods = ['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category is None:
            abort(400)
        data = Question.query.filter_by(category = category.id).all()
        formatted_questions = paginate_questions(request=request,selected_list=data)
        return jsonify({
            'success':True,
            'questions':formatted_questions,
            'total_questions':len(data),
            'current_category':category.type
        })
        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    
    #create a route to quizes '/quizzes with a POST Method
    @app.route('/quizzes', methods=['POST'])
    def play_quizes():
       
        # 
        # get the request body using get_json method from the request module
        body_data = request.get_json()
        # Check is the request body is empty and turn an 400 error if empty 
        if not body_data :
            Abort(400)
        # Get the previous_question from the request body and return None if empty.
        # Get the current_category from the request body and return None if empty
        previous_questions_list = body_data.get('previous_questions',None)
        current_category = body_data.get('category',None)
      
        ## if previous questions list is empty and the categories is available
        # return any question from that category.
        
        if not previous_questions_list:
            if current_category:
                question_data_raw = Question.query.filter(Question.category == str(current_category['id'])).all()
            else:
                question_data_raw = Question.query.all()
        # if previous questions list is available and category return,
        # questions from the specified category and not in the previous questions list.
        else:
            if current_category:
                question_data_raw = (Question.query
                .filter(Question.category == str(current_category['id']))
                .filter(Question.id.notin_(previous_questions_list)).all())
            else:

                question_data_raw = (Question.query
                .filter(Question.id.notin_(previous_questions_list)).all())
    
        formatted_questions_list = [question.format() for question in question_data_raw]
        random_questions_list = formatted_questions_list[random.randint(0, len(formatted_questions_list))]

        return jsonify({
            'success': True,
            'quiz_questions':random_questions_list
        })
        
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """


    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_request(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app

