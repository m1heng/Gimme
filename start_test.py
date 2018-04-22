import cv2
from align_custom import AlignCustom
from ffr import face_feture_reg as FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
import argparse
import sys
import json
import numpy as np
import time
import threading
import os
import shutil
import serial
from Naked.toolshed.shell import execute_js, muterun_js


def camera_recog():
    print("[INFO] camera sensor warming up...")
    vs = cv2.VideoCapture(1); #get input from webcam
    while True:
        _,frame = vs.read();
        #u can certainly add a roi here but for the sake of a demo i'll just leave it as simple as this
        rects, landmarks = face_detect.detect_face(frame,80);#min face size is set to 80x80
        aligns = []
        positions = []
        for (i, rect) in enumerate(rects):
            aligned_face, face_pos = aligner.align(160,frame,landmarks[i])
            if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                aligns.append(aligned_face)
                positions.append(face_pos)
            else: 
                print("Align face failed") #log        
        if(len(aligns) > 0):
            features_arr = extract_feature.get_features(aligns)
            recog_data = findPeople(features_arr,positions);
            for (i,rect) in enumerate(rects):
                cv2.rectangle(frame,(rect[0],rect[1]),(rect[0] + rect[2],rect[1]+rect[3]),(255,0,0)) #draw bounding box for the face
                cv2.putText(frame,recog_data[i][0]+" - "+str(recog_data[i][1])+"%",(rect[0],rect[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
        frame = cv2.resize(frame, (1280,720))
        cv2.imshow("Frame",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            #ft._stop_event.set()
            break

def findPeople(features_arr, positions, thres = 0.6, percent_thres = 70):
    lock.acquire()
    lock.release()
    returnRes = [];
    bestposi = 0
    bestpers = None
    for (i,features_128D) in enumerate(features_arr):
        result = "Unknown";
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person][positions[i]];
            for data in person_data:
                distance = np.sqrt(np.sum(np.square(data-features_128D)))
                if(distance < smallest):
                    smallest = distance;
                    result = person;
        percentage =  min(100, 100 * thres / smallest)
        if percentage <= percent_thres :
            result = "Unknown"
        if percentage >= bestposi:
        	bestposi = percentage
        	bestpers = result
        returnRes.append((result,percentage))
    print('Best: ' + str(bestpers) + ' With Posibility: ' + str(bestposi))
    return returnRes

def create_manual_data_test(root, file_name):
    
    new_dir = os.path.join(root, file_name)
    person_name = file_name
    pic_list = []
    for pic in os.listdir(new_dir):
    	if pic != '.DS_Store':
    		pic_list.append(os.path.join(new_dir, pic))
    if len(pic_list) == 0:
    	return 
    person_imgs = {"Left" : [], "Right": [], "Center": []};
    person_features = {"Left" : [], "Right": [], "Center": []};
    for pic in pic_list:
        frame = cv2.imread(pic);
        rects, landmarks = face_detect.detect_face(frame, 80);  # min face size is set to 80x80
        for (i, rect) in enumerate(rects):
            aligned_frame, pos = aligner.align(160,frame,landmarks[i]);
            if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                person_imgs[pos].append(aligned_frame)
    for pos in person_imgs: #there r some exceptions here, but I'll just leave it as this to keep it simple
        if len(person_imgs[pos]) != 0:
            person_features[pos] = [np.mean(extract_feature.get_features(person_imgs[pos]),axis=0).tolist()]
    lock.acquire()
    data_set[person_name] = person_features
    lock.release()
    print("new user added" + person_name)


def filecheck():
	image_root = './image'
	while True:
		execute_js('./down.js')
		time.sleep(15)
		dir_list = os.listdir(image_root)
		if len(dir_list) != 0:
			for nd in dir_list:
				if nd.startswith('user'):
					create_manual_data_test(image_root, nd)
					shutil.rmtree(os.path.join(image_root, nd))
if __name__ == '__main__':
    FRGraph = FaceRecGraph()
    aligner = AlignCustom()
    extract_feature = FaceFeature(FRGraph)
    face_detect = MTCNNDetect(FRGraph, scale_factor=2)
    f = open('./facerec_128D.txt','r')
    data_set = json.loads(f.read())
    f.close()
    lock = threading.Lock()
    ft = threading.Thread(target=filecheck)
    ft.start()
    camera_recog()











