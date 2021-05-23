from glob import glob
import pickle
from plugins.base import AbstractPlugin
import cv2
import imutils
import face_recognition

class FaceDetectionPlugin(AbstractPlugin):

  '''
    system_config:
      - encodings_path: './the-office.pkl'
  '''

  def __init__(self, system_config) -> None:
      super().__init__(system_config)
      self.encodings = pickle.loads(open(self.system_config.get('encodings_path'), "rb").read())
      

  def run(self, input_path, run_config):
    input_frame = glob(input_path)
    cvframe = cv2.imread(input_frame)
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
          scores[label] = hits
        #end if
      #end for
      if scores:
        most_likely = max(scores, key=scores.get)
        total = sum(score for score in scores.values())
        if most_likely:
          confidence = 0 if total == 0 else round(most_likely/total, 3)
          detections.append({'content-type': 'face', 'content': {most_likely}, 'bb': boxes[i], 'confidence': confidence})
        #end if
      #end if
      return detections
  #end def
#end class 