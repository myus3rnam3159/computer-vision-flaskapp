import os
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import datetime
import json
from bson import json_util
from db import collection


def add_data(response):
    rs = json.loads(json_util.dumps(response))
    collection.insert_one(rs)


def allowed_file(filename: str) -> bool:
    if filename.split(".")[-1] in ("jpg", "jpeg", "png", "webp", "mp4", "mov", "avi"):
        return True
    return False


def detect_and_draw_box(img_filepath: str, model="yolo.h5", confidence=0.3):
    if img_filepath.split(".")[-1] in ("mp4", "mov", "avi"):
        return detect_video(img_filepath, confidence, model)
    else:
        img = cv2.imread(img_filepath)

        bbox, label, conf = cv.detect_common_objects(img, confidence=confidence, model=model)
        output_image = draw_bbox(img, bbox, label, conf)

        filename = img_filepath.split("/")[-1].split(".")[0]
        output_image_path = os.path.join(OUTPUT_FOLDER, 'output_image_{name}.jpg'.format(name=filename))

        cv2.imwrite(output_image_path, output_image)

        response = write_response(bbox, label, conf, width=img.shape[1], height=img.shape[0])
        write_json(OUTPUT_FOLDER, "out_response_{name}.json".format(name=filename), data=response)
        add_data(response)

        filetype = 'image'
        return output_image_path, response, filetype


OUTPUT_FOLDER = os.path.join('static', 'output')


# Hàm xác định video
def detect_video(video_filepath, confidence: float, model: str):
    filename = video_filepath.split("/")[-1].split(".")[0]
    out_path = os.path.join(OUTPUT_FOLDER, "video_result_{name}".format(name=filename))

    cap = cv2.VideoCapture(video_filepath)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    response = dict()
    out = None

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        bbox, label, conf = cv.detect_common_objects(frame, confidence=confidence, model=model)

        frame = cv2.flip(frame, 1)
        output_frame = draw_bbox(frame, bbox, label, conf)

        out = cv2.VideoWriter(out_path, fourcc, 10.0, (640, 480))
        out.write(output_frame)

        print("Streaming...")
        cv2.imshow('frame', output_frame)
        height, width, _ = frame.shape
        response['response'] = (write_response(bbox, label, conf, width, height))

        k = cv2.waitKey(20)
        if k == 113:
            break

    add_data(response)

    cap.release()
    out.release()

    cv2.destroyAllWindows()
    write_json(OUTPUT_FOLDER, "out_response_{name}.json".format(name=filename), data=response)

    filetype = 'video'
    return video_filepath, response['response'], filetype


def write_response(bbox, label, conf, width, height):
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
