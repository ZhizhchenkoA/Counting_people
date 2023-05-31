from flask import Flask, request, redirect, flash, url_for, render_template, send_from_directory, session, g
from werkzeug.utils import secure_filename
import os
from camera import Camera
from settings import SECRET_KEY
import photo as ph

cameras = []
app = Flask(__name__, )
app.secret_key = SECRET_KEY
UPLOAD_FOLDER = 'static/Photos/'
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


@app.route('/<id>camera', methods=['GET', 'POST'])
def upload_photo(id):
    if request.method == 'POST':
        # Получаем загруженный файл из запроса
        photo = request.files['photo']

        # Проверяем, что файл был загружен и имеет допустимое расширение (например, jpg или png)
        if photo and allowed_file(photo.filename):
            # Сохраняем файл на сервере
            photo.save('static/Photos/' + photo.filename)
            n = ph.main('static/Photos/' + photo.filename, camera_id=int(id))

            try:
                # Возвращаем шаблон страницы с отображением загруженного фото
                return render_template('video_load.html', photo_url=id + '.jpeg', id=id, number_of_people=n)
            except:
                return render_template('video_load.html', id=id)

    # Если метод запроса GET или файл не был загружен или имеет недопустимое расширение, отображаем страницу загрузки
    return render_template('video_load.html', id=id)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower()


if __name__ == '__main__':
    app.run(debug=False)
