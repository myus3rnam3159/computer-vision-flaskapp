COMPUTER VISION APP

* Nguồn tham khảo (nhớ sử dụng vpn)
    * https://github.com/ZaheedaT/computer-vision-flaskapp
* Format code trong pycharm: ctrl shift alt l
* Lỗi với cv2: https://github.com/opencv/opencv/issues/20997#issuecomment-1328068006
* Lỗi vời file favicon: https://www.facebook.com/groups/cs50/posts/1752004878279883/
* Hiện tại app chỉ có thể tải và xuất hình ảnh và video

1. Cài đặt

    a. Python 3.8.10

    b. Môi trường lập trình: Ubuntu 20.04

    c. Cách sử dụng môi trường ảo python venv (standard) trên ubuntu linux

        Tạo folder chứa môi trường ảo, đặt tên, ví dụ: myenv
        Tái: sudo apt-get install python3.x-venv (x là phiên bản python 3)
        Kích hoạt môi trường(trên bash - chú ý nhớ thoát ra folder cha):
            a. python3 -m venv myenv
            b. source myenv/bin/activate

    d. Tải flask: pip install Flask

    e. Tải pymongo: https://pymongo.readthedocs.io/en/stable/installation.html

    f. Tạo cơ sở dữ liệu trên mongodb atlas: Từ tìm hiểu trên google search

    g. Tải Model cho nhận diện hình ảnh và xác định đối tượng: wget https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5

    h. Các dependencies khác: https://github.com/OlafenwaMoses/ImageAI#dependencies


2. Quy trình thực hiện


    a. Tạo các thư mục vào file như trong bài báo hướng dẫn


   
