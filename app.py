from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify
from src.routes import routes_blueprint


app = Flask(__name__)

cors = CORS(app, resources={
r"/*"
: {
"origins"
:
"*"
}}, expose_headers=
'AuthToken'
)

app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(routes_blueprint)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"msg": "Server up!"})


if __name__ == '__main__':
    app.run()
