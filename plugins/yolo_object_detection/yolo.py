__all__ = ['YoloPlugin']


# USAGE
# python yolo.py --image images/baggage_claim.jpg --yolo yolo-coco

from ..base import AbstractPlugin
import numpy as np
import time
import cv2
import os

class YoloPlugin(AbstractPlugin):

	_yoloDir = "./plugins/yolo_object_detection/yolo_coco"
	_contentType = "yolo"

	def __init__(self, plugin_config) -> None:
		super().__init__(plugin_config)
				# derive the paths to the YOLO weights and model configuration
		weightsPath = os.path.sep.join([self._yoloDir, "yolov3.weights"])
		configPath = os.path.sep.join([self._yoloDir, "yolov3.cfg"])

		# load our YOLO object detector trained on COCO dataset (80 classes)
		print("[INFO] loading YOLO from disk...")
		self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

	'''
		plugin_config:
		- confidence : default (0.5),
		- threshold : default (0.3)
	'''
	def run(self, input_path):
		labelsPath = os.path.join(self._yoloDir, 'coco.names')
		print(labelsPath)
		LABELS = open(labelsPath).read().strip().split("\n")

		# initialize a list of colors to represent each possible class label
		np.random.seed(42)
		COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
			dtype="uint8")

		# load our input image and grab its spatial dimensions
		image = cv2.imread(input_path)
		(H, W) = image.shape[:2]

		# determine only the *output* layer names that we need from YOLO
		ln = self.net.getLayerNames()
		ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

		# construct a blob from the input image and then perform a forward
		# pass of the YOLO object detector, giving us our bounding boxes and
		# associated probabilities
		blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
			swapRB=True, crop=False)
		self.net.setInput(blob)
		start = time.time()
		layerOutputs = self.net.forward(ln)
		end = time.time()

		# show timing information on YOLO
		print("[INFO] YOLO took {:.6f} seconds".format(end - start))

		# initialize our lists of detected bounding boxes, confidences, and
		# class IDs, respectively
		boxes = []
		confidences = []
		classIDs = []

		# loop over each of the layer outputs
		for output in layerOutputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability) of
				# the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]

				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > self.plugin_config["confidence"]:
					# scale the bounding box coordinates back relative to the
					# size of the image, keeping in mind that YOLO actually
					# returns the center (x, y)-coordinates of the bounding
					# box followed by the boxes' width and height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					# use the center (x, y)-coordinates to derive the top and
					# and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))
					
					# update our list of bounding box coordinates, confidences,
					# and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

		# apply non-maxima suppression to suppress weak, overlapping bounding
		# boxes
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.plugin_config["confidence"],
			self.plugin_config["threshold"])

		objects = []
		positions = []
		# ensure at least one detection exists
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])

				# draw a bounding box rectangle and label on the image
				color = [int(c) for c in COLORS[classIDs[i]]]
				cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
				text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
				# objects.append(text)
				content = LABELS[classIDs[i]]
				bounding_boxes = boxes[i]
				output_confidence = round(confidences[i], 3)
				objects.append({'content-type': self._contentType, 'content': content, 'bb': bounding_boxes, 'confidence': output_confidence})
				print({'content-type': self._contentType, 'content': content, 'bb': bounding_boxes, 'confidence': output_confidence})
				positions.append([x,y])
				cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
					0.5, color, 2)

		return objects
		# print(objects)
		# print(positions)
		# print(boxes)
		# show the output image
		# cv2.imshow("Image", image)
		# # cv2.imwrite("demo_image.png",image)
		# cv2.waitKey(0)