import os
from flask import Flask, request, redirect, url_for
from flask import flash
from werkzeug.utils import secure_filename
from keras.models import Sequential, load_model
import keras, sys
import numpy as np
from PIL import Image

classes = ["bns-v","btk","dsp","hcr","hdr25"]
num_classes = len(classes)
image_size = 320


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません。')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません。')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            model  = load_model('D:/keras-yolo3/logs/000/trained_weights_final.h5')

            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()
            # percentage = int(result[predicted] * 100)
            percentage = int(result[predicted])

            return classes[predicted] + " " + str(percentage) + " %"

            #return redirect(url_for('uploaded_file', filename=filename))

    return '''
    <!doctype html>
    <html>
    <head>
    <meta chrset="UTF-8">
    <title>YOLO3-THK_Product_AI</title></head>
    <body bgcolor="#f5f5f5">
    <h1>THK製品の画像ファイルをアップして下さい。</h1>
    <P>jpg, png, gif　形式のみ受付</P>
    <form method = post enctype = multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#   if __name__ == '__main__':
#        app.run(debug=False, host='0.0.0.0', port=80)

#このプログラムの実行方法
# conda install Flask
# pip install keras
# conda install tensorflow
#(tf140) D:\product_ai>set FLASK_APP=predict_file.py
#(tf140) D:\product_ai>flask run
