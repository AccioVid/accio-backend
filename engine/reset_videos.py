import sys
sys.path.append('./')
from api import VideosModel

videos = VideosModel.query.filter_by(processed=True)
for v in videos:
    v.processed = False
    v.results = None
    v.save()

