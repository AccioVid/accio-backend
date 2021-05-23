from plugins.yolo_object_detection.yolo import yoloPlugin


yp = yoloPlugin()

_configuration = {
		"confidence" : 0.5,
		"threshold" : 0.3
}

yp.run("images/baggage_claim.jpg", _configuration)