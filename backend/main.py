from flask import Flask, jsonify

from loginPage import login_handler_app
from registrationPage import registration_handler_app
from capsuleCreation import capsule_creation_app 


app = Flask(__name__)

# Register login handler app
app.register_blueprint(login_handler_app)

# Register registration handler app
app.register_blueprint(registration_handler_app)

# Register capsule creation handler app
app.register_blueprint(capsule_creation_app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000)