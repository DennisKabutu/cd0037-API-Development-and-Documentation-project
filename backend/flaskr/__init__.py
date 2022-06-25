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
    CORS(app, resources={r'/*:{"origins":"*"}'})
   

    """
     Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Header','GET,POST,PUT,PATCH,DELETE,OPTIONS')
        return response

    
    @app.route('/questions', methods = ['POST'])
    def post_route_handler():
        body = request.get_json()
        if ('searchTerm' in body):
            return search_questions()
        else:
            return create_question()

            
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
    An endpoint to handle GET requests for questions,including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
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
        #get categories ordered by category type 
            categories = Category.query.order_by(Category.type).all()
        ## check if categories is empty 
            if categories:
                all_categories = {}
        ## Populate the all_categories dict with Category ID and Category Type
                for category in categories:
                    all_categories[category.id] = category.type
            else:
                abort(404)
        except:
            abort(422)
        # return Jsonified paginated list of questions, Total of number of Questions and Categories   
        return jsonify({
            "success":True,
            "questions":paginated_questions,
            "totalQuestions":len(Question.query.all()),
            "categories":all_categories,
            ##"currentCategory":
        })
    
      

    """
    Create an endpoint to DELETE question using a question ID.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            #Try querying the database to get the specified question
            question = Question.query.filter(Question.id==question_id).one_or_none()
            #If question is None Throw a 404 error
            # If found delete it and return success message and deleted question id 
            if question is None:
                abort(404)
            else:
                Question.delete(question)   
            return jsonify({
                'success': True,
               'questionId':question.id,
            })
        except:
            abort(422)

    

    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """

    
   
    def create_question():
        #Get request Body using the get_json method.
        body = request.get_json()
        #Load request params into variables
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        # If any request params is None throw a 400 error
        if(new_question is None or new_answer is None or new_category is None or new_difficulty is None):
               return abort(400)

        try:
            #If all params are present create a Question
            question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                )
            # Insert the question to the database
            question.insert()

            return jsonify({
                    'success':True,
                    'created_id':question.id,
            })
        except :
            return abort(422)


    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """

    def search_questions():
        try:
            body_data = request.get_json()
            search_term = body_data.get('searchTerm', None)

            if search_term is not None:
                search_results = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()

                formatted_search_results = [question.format() for question in search_results]

                return jsonify({
                    'success': True,
                    'questions': formatted_search_results,
                    'totalQuestions': len(search_results),
                    #'currentCategory':formatted_search_results[0].category,// TODO 
                 })
            else:
                abort(404)
        except:
            abort(422)
        
       
        

    """
  
    Create a GET endpoint to get questions based on category.
    """
    @app.route('/categories/<int:category_id>/questions' ,methods = ['GET'])
    def get_questions_by_category(category_id):
        try:
            #Query for category based on category id.
            category = Category.query.filter_by(id=category_id).one_or_none()
            #If category is None throw a 404 error
            if category is None:
                abort(404)
            #Query questions based on category.
            questions_based_categories = Question.query.filter_by(category = category.id).all()
            #Format questions as a list.
            formatted_questions = [question.format() for question in questions_based_categories]

            return jsonify({
                'success':True,
                'questions':formatted_questions,
                'totalQuestions':len(Question.query.all()),
                'currentCategory':category.type
            })
        except:
            abort(422)
        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    
    #create a route to quizes '/quizzes with a POST Method
    @app.route('/quizzes', methods=['POST'])
    def play_quizes():
       
        # 
        # get the request body using get_json method from the request module
        body_data = request.get_json()
        # Check is the request body is empty and turn an 400 error if empty 
        if not body_data :
            abort(400)
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
            'question':random_questions_list
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

