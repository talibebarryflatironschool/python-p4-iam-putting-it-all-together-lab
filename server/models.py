# from sqlalchemy.orm import validates
# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy_serializer import SerializerMixin

# from config import db, bcrypt

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'

#     pass

# class Recipe(db.Model, SerializerMixin):
#     __tablename__ = 'recipes'
    
#     pass




from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(SerializerMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    _password_hash = db.Column(db.String(128), nullable=False, default="")  # Added default=""
    image_url = db.Column(db.String(200))
    bio = db.Column(db.String(500))
    
    recipes = db.relationship('Recipe', backref='user', lazy=True)

    
    # Password is write‑only. Attempting to read it raises an AttributeError.
    @hybrid_property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")
    
    @password.setter
    def password(self, plaintext):
        self._password_hash = bcrypt.generate_password_hash(plaintext).decode('utf-8')
    
    # Also support assignment to "password_hash" for convenience (e.g. in seeding)
    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hash is not directly readable.")
    
    @password_hash.setter
    def password_hash(self, plaintext):
        self._password_hash = bcrypt.generate_password_hash(plaintext).decode('utf-8')
    
    def verify_password(self, plaintext):
        return bcrypt.check_password_hash(self._password_hash, plaintext)
    
    def authenticate(self, password):
        return self.verify_password(password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'image_url': self.image_url,
            'bio': self.bio
        }

class Recipe(SerializerMixin, db.Model):
    __tablename__ = 'recipes'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    
    # Validation: ensure instructions are at least 50 characters long.
    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long.")
        return instructions
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'instructions': self.instructions,
            'minutes_to_complete': self.minutes_to_complete,
            'user': self.user.to_dict() if self.user else None
        }




