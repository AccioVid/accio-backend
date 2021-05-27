__all__ = ['FaceDetectionPlugin']

from glob import glob
import pickle
from ..base import AbstractPlugin
import cv2
import imutils
import face_recognition

class FaceDetectionPlugin(AbstractPlugin):

  '''
    plugin_config:
      - encodings_path: 'plugins/facedetection/the_office.pkl'
  '''

  def __init__(self, plugin_config) -> None:
      super().__init__(plugin_config)
      self.encodings = pickle.loads(open(self.plugin_config.get('encodings_path'), "rb").read())
      

  def run(self, input_path):
    # input_frame = glob(input_path)
    cvframe = cv2.imread(input_path)
    rgb = cv2.cvtColor(cvframe, cv2.COLOR_BGR2RGB)
    rgb = imutils.resize(rgb, width=750)
    boxes = face_recognition.face_locations(rgb, model='hog')
    frame_encodings = face_recognition.face_encodings(rgb, boxes)

    n_faces = len(boxes)
    detections = []
    for i in range(n_faces):
      encoding = frame_encodings[i]
      scores = {}
      for label, ref_encodings in self.encodings.items():
        matches = face_recognition.compare_faces(ref_encodings, encoding)
        hits = sum(1 for m in matches if m == True)
        if hits > 0:
          scores[label] = hits / len(matches)
        #end if
      #end for
      if scores:
        most_likely = max(scores, key=scores.get)
        if most_likely:
          confidence = round(scores[most_likely], 3)
          detections.append({'content-type': 'face', 'content': most_likely, 'bb': boxes[i], 'confidence': confidence})
        #end if
      #end if
      return detections
  #end def
#end class 