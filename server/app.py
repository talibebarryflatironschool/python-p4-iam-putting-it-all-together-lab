# #!/usr/bin/env python3

# from flask import request, session
# from flask_restful import Resource
# from sqlalchemy.exc import IntegrityError

# from config import app, db, api
# from models import User, Recipe

# class Signup(Resource):
#     pass

# class CheckSession(Resource):
#     pass

# class Login(Resource):
#     pass

# class Logout(Resource):
#     pass

# class RecipeIndex(Resource):
#     pass

# api.add_resource(Signup, '/signup', endpoint='signup')
# api.add_resource(CheckSession, '/check_session', endpoint='check_session')
# api.add_resource(Login, '/login', endpoint='login')
# api.add_resource(Logout, '/logout', endpoint='logout')
# api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)






#!/usr/bin/env python3

from flask import request, session, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        image_url = data.get('image_url')
        bio = data.get('bio')
        
        errors = {}
        if not username:
            errors['username'] = ["Username is required."]
        if not password:
            errors['password'] = ["Password is required."]
        if errors:
            return {"errors": errors}, 422
        
        try:
            user = User(username=username, image_url=image_url, bio=bio)
            user.password = password  # Hash the password.
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return user.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            errors['username'] = ["Username already exists."]
            return {"errors": errors}, 422
        except Exception as e:
            db.session.rollback()
            return {"errors": {"error": str(e)}}, 422

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
        return {"error": "Unauthorized"}, 401

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {"error": "Username and password required."}, 422
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {"error": "Invalid username or password."}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session.pop('user_id')
            return "", 204
        else:
            return {"error": "Unauthorized"}, 401

class RecipeIndex(Resource):
    def get(self):
        if not session.get('user_id'):
            return {"error": "Unauthorized"}, 401
        
        recipes = Recipe.query.all()
        recipes_data = [recipe.to_dict() for recipe in recipes]
        return recipes_data, 200
    
    def post(self):
        if not session.get('user_id'):
            return {"error": "Unauthorized"}, 401
        
        data = request.get_json()
        title = data.get('title')
        instructions = data.get('instructions')
        minutes_to_complete = data.get('minutes_to_complete')
        
        errors = {}
        if not title:
            errors['title'] = ["Title is required."]
        if not instructions or len(instructions) < 50:
            errors['instructions'] = ["Instructions are required and must be at least 50 characters long."]
        if errors:
            return {"errors": errors}, 422
        
        try:
            recipe = Recipe(
                title=title,
                instructions=instructions,
                minutes_to_complete=minutes_to_complete,
                user_id=session.get('user_id')
            )
            db.session.add(recipe)
            db.session.commit()
            return recipe.to_dict(), 201
        except (IntegrityError, ValueError) as e:
            db.session.rollback()
            return {"errors": {"error": str(e)}}, 422

# Set up API endpoints.
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
