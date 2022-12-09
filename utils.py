import os
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import datetime
import json


# Hàm kiểm tra xem file có thuộc loại hợp lệ hay không
def allowed_file(filename: str) -> bool:
    if filename.split(".")[-1] in ("jpg", "jpeg", "png", "webp", "mp4", "mov", "avi"):
        return True
    return False


# Hàm xác định và vẽ ô quanh vật thể
def detect_and_draw_box(img_filepath: str, model="yolo.h5", confidence=0.2):
    if img_filepath.split(".")[-1] in ("mp4", "mov", "avi"):

        print("\nFile is a video")
        return detect_video(img_filepath, confidence, model)
    else:
        print("\nFile is an image")

        # Đọc file ảnh vào một numpy array
        img = cv2.imread(img_filepath)

        # Thực hiện xác định đối tượng
        bbox, label, conf = cv.detect_common_objects(img, confidence=confidence,
                                                     model=model)

        # In đối tượng ra màn hình
        for lb, c in zip(label, conf):
            print(f"Detected object: {lb} with confidence level of {c}\n")

        # Tạo ra ảnh mới bao gồm khung xác định đối tượng và nhãn
        output_image = draw_bbox(img, bbox, label, conf)

        # Đặt tên file và làm đường dẫn cho file
        filename = img_filepath.split("/")[-1].split(".")[0]
        output_image_path = os.path.join(OUTPUT_FOLDER, 'output_image_{name}.jpg'.format(name=filename))
        print(f"========================\nImage processed: {output_image_path}\n")

        # Lưu file
        cv2.imwrite(output_image_path, output_image)

        # Lưu response vào JSON locally
        response = write_response(bbox, label, conf, width=img.shape[1], height=img.shape[0])
        write_json(OUTPUT_FOLDER, "out_response_{name}.json".format(name=filename),
                   data=response)

        filetype = 'image'
        return output_image_path, response, filetype


# Xác định lại output folder
OUTPUT_FOLDER = os.path.join('static', 'output')


# Hàm xác định video
def detect_video(video_filepath, confidence: float, model: str):
    """Thực hiện xác định đối tượng trên một video đã được tải lên
    cũng như dán nhãn cho video khi nó đang được stream

    Kết quả trả về
        response (dict): Một dic chứa dữ liệu hồi đáp từ model's result
        filetype (str): Một chuỗi thể hiện loại file video
    """

    print("\nThực hiện xác định vật thể trong video...")

    # Lầy file name
    filename = video_filepath.split("/")[-1].split(".")[0]
    # Set output folder path
    out_path = os.path.join(OUTPUT_FOLDER, "video_result_{name}".format(name=filename))
    # Tạo video capture, dùng để stream hoặc play video
    cap = cv2.VideoCapture(video_filepath)
    # Lưu output video vào một folder
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    response = dict()
    while cap.isOpened():
        # Trả về một tuple bool và frame, nếu ret là true thì có một khung để nhìn
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Lật hình nếu bị ngược
        frame = cv2.flip(frame, 1)

        # Lấy thuộc tính của object
        bbox, label, conf = cv.detect_common_objects(frame, confidence=confidence, model=model)

        # Viết frame vào output files
        output_frame = draw_bbox(frame, bbox, label, conf)
        out = cv2.VideoWriter(out_path, fourcc, 10.0, (640, 480))
        out.write(output_frame)

        print("Streaming...")
        cv2.imshow('frame', output_frame)
        height, width, _ = frame.shape
        response['response'] = (write_response(bbox, label, conf, width, height))

        # Đợi 20 giây để chờ dừng video vào nhập user input
        k = cv2.waitKey(20)
        if k == 113:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    write_json(OUTPUT_FOLDER, "out_response_{name}.json".format(name=filename), data=response)
    filetype = 'video'

    return video_filepath, response['response'], filetype


def write_response(bbox, label, conf, width, height):
    """ Adds model results to a dictionary to create a response object
    Parameters:
        bbox (list):
        label (list of str):
        conf (list of float):
        width (float):
        height  (float):
    Returns:
        response (dict): A dictionary containing response data from the model's results.
    """
    response = dict()
    response['Bounding Box Coordinates'] = bbox
    response['Object Class'] = label
    response['Confidence'] = conf
    now = datetime.datetime.now()
    timestamp = str(now.strftime("%Y-%m-%d_%H:%M:%S"))
    response['Timestamp'] = timestamp
    response['Image Metadata'] = {'width': width, 'height': height}

    return response


def write_json(target_path, target_file, data):
    with open(os.path.join(target_path, target_file), 'w') as f:
        json.dump(data, f)
