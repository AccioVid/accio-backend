from engine.keyframes import KeyFrameExtractor
from plugins.facedetection import FaceDetectionPlugin
from plugins.yolo_object_detection.yolo import yoloPlugin
from os import listdir
from os.path import isfile, join

# sys_config = "asd"
# yp = yoloPlugin(sys_config)

# _configuration = {
# 		"confidence" : 0.5,
# 		"threshold" : 0.3
# }

# imagePathVar = "baggage_claim.jpg"
# yp.run("./plugins/yolo_object_detection/images/" + imagePathVar, _configuration)

def runKeyFrames():
	path = "./plugins/yolo_object_detection/videos/"
	destPath = "./output/"
	files = listdir(path)

	for file in files:
		kf = KeyFrameExtractor()
		folderName = file.split(".")[0]
		kf.light_significant_change_detect(path+file , destPath+folderName,0.55, verbose=False)
		results = runYolo(destPath+folderName)
		storeInDatabase(results)

def runYolo(path):
	sys_config = "asd"
	yp = yoloPlugin(sys_config)

	_configuration = {
			"confidence" : 0.5,
			"threshold" : 0.3
	}
	newPath = path + "/" + "keyframes/"
	frames =  listdir(newPath)

	objectsInFrames = []
	for frame in frames:
		objectsDetected = yp.run(newPath + frame, _configuration)
		if(len(objectsDetected) != 0):
			objectsInFrames.append(objectsDetected)
	
	return objectsInFrames

def storeInDatabase(results):
	print("##########RESULTS###############")
	print(results)

runKeyFrames()

# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# fp = FaceDetectionPlugin(sys_config)
# det = fp.run("./plugins/yolo_object_detection/images/" + imagePathVar, "./plugins/facedetection/the_office.pkl")
# print(det)
