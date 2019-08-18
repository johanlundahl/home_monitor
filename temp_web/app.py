from flask import Flask
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
basic_auth = BasicAuth(app)

@app.route("/", methods=['GET'])
@basic_auth.required
def root():
	return 'Halloj!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')