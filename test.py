from plugins.facedetection import FaceDetectionPlugin
from plugins.yolo_object_detection.yolo import yoloPlugin


sys_config = "asd"
yp = yoloPlugin(sys_config)

_configuration = {
		"confidence" : 0.5,
		"threshold" : 0.3
}

imagePathVar = "baggage_claim.jpg"
yp.run("./plugins/yolo_object_detection/images/" + imagePathVar, _configuration)

# fp = FaceDetectionPlugin(sys_config)
# det = fp.run("./plugins/yolo_object_detection/images/" + imagePathVar, "./plugins/facedetection/the_office.pkl")
# print(det)
