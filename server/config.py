from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)

api = Api(app)



# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_restful import Api

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # You can also use an environment variable here.
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a strong secret key in production.

# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# api = Api(app)
