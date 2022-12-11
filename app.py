from werkzeug.exceptions import HTTPException
from utils import allowed_file, detect_and_draw_box
import os
from flask import Flask, render_template, request, session

# Tạo application class
app = Flask(__name__, template_folder='templates', static_folder='static')

# Tạo các biến ứng với các folder lưu trữ
UPLOAD_FOLDER = os.path.join('static', 'uploads')
OUTPUT_FOLDER = os.path.join('static', 'output')


@app.route('/')
def main():
    return render_template("index.html")


# Đăng ký config cho upload folder để có được kiểu giá trị tham số phù hợp
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'xyz'
os.path.dirname("../templates")


# Tải file lên
@app.route('/', methods=["POST"])
def upload_file():
    # Lấy dữ liệu file từ post request
    _img = request.files['file-uploaded']
    # Lấy tên file
    filename = _img.filename
    # Nếu file không hợp lệ
    if not allowed_file(filename):
        # Thông báo
        raise HTTPException(description="Unsupported file provided")
    # File hợp lệ sẽ được lưu
    _img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Lưu đường dẫn của file vào danh sách session
    session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    return render_template('index.html', success=True)


# Thể hiện file
@app.route('/show_file')
def display_image():
    img_file_path = session.get('uploaded_img_file_path', None)
    if img_file_path.split(".")[-1] in ("mp4", "mov"):
        return render_template('show_file.html', user_image=img_file_path, is_image=False, is_show_button=True)
    else:
        return render_template('show_file.html', user_image=img_file_path, is_image=True, is_show_button=True)


@app.route('/detect_object')
def detect_object():
    uploaded_image_path = session.get('uploaded_img_file_path', None)
    output_image_path, response, file_type = detect_and_draw_box(uploaded_image_path)

    if file_type == "image":
        return render_template('show_file.html', user_image=output_image_path, is_image=True, is_show_button=False)
    else:
        return render_template('show_file.html', user_image=output_image_path, is_image=False, is_show_button=False)


if __name__ == '__main__':
    app.run(debug=True)
