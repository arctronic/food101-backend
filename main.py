from flask import Flask, request, jsonify
from utils import prediction_random_images
import requests

app = Flask(__name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        print(request.files)
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})
        if not allowed_file(filename=file.filename):
            return jsonify({'error': 'format not supported.'})
    # load image
    try:
        img_byte = file.read()
        prediction = prediction_random_images([img_byte])
        print(prediction)
        url = "https://www.themealdb.com/api/json/v1/1/search.php?s="+prediction.replace("_","")
        res = requests.get(url)
        res_data = res.json()
        return jsonify({'data': prediction, 'other': res_data})
    except:
        return jsonify({'error': 'Error during prediction'})
