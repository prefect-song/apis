import base64
import cv2

capture_flag = False
capture_img = None
isStartRecordVideo = False


def get_current_img():
    global isStartRecordVideo, capture_flag, capture_img
    if isStartRecordVideo:
        capture_flag = True
        while not capture_img:
            pass
        result = capture_img
        capture_img = None
        return result
    else:
        return False


def gen_display(camera):
    global isStartRecordVideo
    isStartRecordVideo = True
    """
    视频流生成器功能。
    """
    while True:
        # 读取图片
        ret, origin_frame = camera.read()
        if ret:
            # frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # 将图片进行解码
            ret, frame = cv2.imencode('.jpeg', origin_frame)
            if ret:
                global capture_flag, capture_img
                if capture_flag:
                    encoded_origin_frame = cv2.imencode('.jpg', origin_frame)[1]
                    img_base64 = base64.b64encode(encoded_origin_frame)
                    capture_img = img_base64
                    capture_flag = False
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

