import os
import cv2
import numpy as np
import time
import glob
from PIL import Image
import peakutils

class KeyFramesType:
    '''
        # frame_dict
        "source_url: "path/to/source,
        "frames": 
        [
            {
                "index": 0,
                "at": xx,
                "path": "path/to/frame"
            }
        ]
        '''
    def __init__(self, source_url):
        self.source_url = source_url
        self.frames_list = []
    
    def add_frame(self, frame_dict):
        self.frames_list.append(frame_dict)
class KeyFrameExtractor:
    
    def light_significant_change_detect(self, source, dest, thres, verbose=False):
        keyframePath = dest+'/keyframes'
        self.__prepare_dirs(keyframePath)

        cap = cv2.VideoCapture(source)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
        if (cap.isOpened()== False):
            print("Error opening video file")

        fps = self.__get_frames_per_seconds(cap)
        interval_end = 0

        lastFrame = None
        cnt = 1

        key_frames_obj = KeyFramesType(source)

        for i in range(length):
            ret, frame = cap.read()
            grayframe, blur_gray = self.__convert_frame_to_grayscale(frame)
            if lastFrame is not None:
                diff = cv2.subtract(blur_gray, lastFrame)
                diffMag = cv2.countNonZero(diff)
                
                

                height, width = blur_gray.shape
                resolution = height * width
                if diffMag / resolution > thres:
                    interval_end = i/fps
                    path = os.path.join(keyframePath , 'keyframe'+ str(cnt) +'.jpg')
                    cv2.imwrite(path, frame)
                    frame_dict = {
                        'index': cnt,
                        'path': path,
                        'at': interval_end
                    }
                    
                    key_frames_obj.add_frame(frame_dict)
                    if(verbose):
                        print(frame_dict)
                    cnt += 1
            lastFrame = blur_gray

        cap.release()
        cv2.destroyAllWindows()
        return key_frames_obj

    def significant_change_detect(self, source, dest, Thres, verbose=False):
        keyframePath = dest+'/keyframes'
        self.__prepare_dirs(keyframePath)

        cap = cv2.VideoCapture(source)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if (cap.isOpened()== False):
            print("Error opening video file")

        fps = self.__get_frames_per_seconds(cap)
        interval_end = 0
        key_frames_obj = KeyFramesType(source)

        lstfrm = []
        lstdiffMag = []
        timeSpans = []
        images = []
        full_color = []
        lastFrame = None
        Start_time = time.process_time()
        
        # Read until video is completed
        for i in range(length):
            ret, frame = cap.read()
            grayframe, blur_gray = self.__convert_frame_to_grayscale(frame)

            frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
            lstfrm.append(i)
            images.append(grayframe)
            full_color.append(frame)
            if frame_number == 0:
                lastFrame = blur_gray

            diff = cv2.subtract(blur_gray, lastFrame)
            diffMag = cv2.countNonZero(diff)
            lstdiffMag.append(diffMag)
            stop_time = time.process_time()
            time_Span = stop_time-Start_time
            timeSpans.append(time_Span)
            lastFrame = blur_gray

        cap.release()
        y = np.array(lstdiffMag)
        base = peakutils.baseline(y, 2)
        indices = peakutils.indexes(y-base, Thres, min_dist=1)
        
        cnt = 1
        for x in indices:
            frame_path = os.path.join(keyframePath , 'keyframe'+ str(cnt) +'.jpg') 
            cv2.imwrite(frame_path, full_color[x])
            interval_end = lstfrm[x]/fps
            frame_dict = {
                'index': cnt,
                'path': frame_path,
                'at': interval_end
            }
            key_frames_obj.add_frame(frame_dict)
            cnt += 1
            if(verbose):
                print(frame_dict)

        cv2.destroyAllWindows()
        return key_frames_obj
    
    def __get_frames_per_seconds(self, cap):
        fps = round(cap.get(cv2.CAP_PROP_FPS))
        return fps

    def __scale(self, img, xScale, yScale):
        res = cv2.resize(img, None, fx=xScale, fy=yScale, interpolation=cv2.INTER_AREA)
        return res


    def __crop(self, infile, height, width):
        im = Image.open(infile)
        imgwidth, imgheight = im.size
        for i in range(imgheight // height):
            for j in range(imgwidth // width):
                box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
                yield im.crop(box)


    def __averagePixels(self, path):
        r, g, b = 0, 0, 0
        count = 0
        pic = Image.open(path)
        for x in range(pic.size[0]):
            for y in range(pic.size[1]):
                imgData = pic.load()
                tempr, tempg, tempb = imgData[x, y]
                r += tempr
                g += tempg
                b += tempb
                count += 1
        return (r / count), (g / count), (b / count), count


    def __convert_frame_to_grayscale(self, frame):
        grayframe = None
        gray = None
        if frame is not None:
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = self.__scale(gray, 1, 1)
            grayframe = self.__scale(gray, 1, 1)
            gray = cv2.GaussianBlur(gray, (9, 9), 0.0)
        return grayframe, gray


    def __prepare_dirs(self, keyframePath):
        if not os.path.exists(keyframePath):
            os.makedirs(keyframePath)
        files = glob.glob(keyframePath + "/*")
        for f in files:
            os.remove(f)