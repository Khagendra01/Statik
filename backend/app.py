from flask import Flask, request, jsonify
from flask_cors import CORS
from lang_res import askIT

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Route to handle the POST request
@app.route('/askai', methods=['POST'])
def ask_AI():

    data = request.get_json()
    question = data.get('question')
    print(question)
    res = askIT(question)

    # Return a success response
    return jsonify({
        'data': res,
        'status': 'success',
        'message': 'Memorial created successfully'
    }), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)