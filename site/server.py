from flask import Flask, request, redirect, flash, url_for, render_template, send_from_directory, session, g
from werkzeug.utils import secure_filename
import os
from Models.camera import Camera
from config import SECRET_KEY
import CV_model.photo as ph

cameras = []
app = Flask(__name__, )
app.secret_key = SECRET_KEY

app.config['UPLOAD_FOLDER'] = ''

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

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

            try:
                photo.save('static/photos/' + id + '.' + photo.filename.split('.')[-1])
                n = ph.main('static/photos/' + id + '.' + photo.filename.split('.')[-1], camera_id=int(id))

                # Возвращаем шаблон страницы с отображением загруженного фото
                return render_template('video_load.html', photo_url=f'/photos/{id}.{photo.filename.split(".")[-1]}', id=id, number_of_people=n)
            except:
                return render_template('video_load.html', photo_url=f'/photos/{id}.{photo.filename.split(".")[-1]}',  id=id, number_of_people=0)

    # Если метод запроса GET или файл не был загружен или имеет недопустимое расширение, отображаем страницу загрузки
    return render_template('video_load.html', id=id)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html')


if __name__ == '__main__':
    app.run(debug=True)
