# app.py (Entry point)
from flask import Flask
from Controller.UserController import user_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True)