from flask import Flask, request, redirect, flash, url_for, render_template, send_from_directory, session, g
from werkzeug.utils import secure_filename
import os
from camera import Camera
from settings import SECRET_KEY

cameras = []
app = Flask(__name__, )
app.secret_key = SECRET_KEY
UPLOAD_FOLDER = 'Photos/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница', cameras_links=cameras)


@app.route('/add_camera', methods=['POST', 'GET'])
def add_camera():
    if request.method == 'POST':
        n = request.form
        cameras.append(Camera(n['id'], n['space']))
        return redirect('/')


@app.route('/<id>camera')
def camera_video(id):
    print(id)


if __name__ == '__main__':
    app.run(debug=True)
