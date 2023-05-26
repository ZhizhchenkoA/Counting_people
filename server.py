from flask import Flask, request, redirect, flash, url_for, render_template
from werkzeug.utils import secure_filename
import os
from settings import SECRET_KEY

app = Flask(__name__, )
app.secret_key = SECRET_KEY
UPLOAD_FOLDER = 'Photos/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template('base.html')



if __name__ == '__main__':
    app.run(debug=True)
