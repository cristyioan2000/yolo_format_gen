import os
import cv2
import argparse
import numpy as np
import time
from PyQt5 import QtWidgets,QtGui

parser = argparse.ArgumentParser(description='Open-source yolo format tool samepling')
parser.add_argument('-c', '--class_name', type=str, help='name of the class')
parser.add_argument('-o', '--output_dir', type=str, help='Path to output directory')
parser.add_argument('-n', '--sampel_number', type=int, help='How many sampels of the selected class')
parser.add_argument('-m', '--mode',default='0', type=int, help='normal\\negative')
parser.add_argument('-f', '--index_from',default='0', type=int, help='start indexing from')
args = parser.parse_args()
import time



def __main__(output_dir,class_name,sampel_number,mode,index):

    current_time = int(time.time())
    if mode == 1:

        start_file_index = 0


    boxes =[]
    path = os.getcwd()
    #add_dir = os.path.join(path,'capture\\Hand\\')
    cap = cv2.VideoCapture(0)
    frame_count = 0
    multiTracker = cv2.MultiTracker_create()
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    i = 0

    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)
    #     os.makedirs(os.path.join(output_dir,'img\\'))
    #     os.makedirs(os.path.join(output_dir,'text\\'))
    # img_dir  = os.path.join(output_dir,'img\\')
    # text_dir = os.path.join(output_dir,'text\\')
    img_dir = output_dir
    text_dir = output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sampel_number+=index
    width = 416
    height = 416
    while cap.isOpened():
        if sampel_number == index:
            break
        ret,frame = cap.read()
        frame = cv2.resize(frame, (width, height))

        # img = frame.copy()
        img = frame
        frame_count= frame_count + 1


        #width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        #height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

        sampel_number-=1



        if frame_count > 100 & frame_count < 120 and len(boxes) == 0:
            box = cv2.selectROI('MultiTracker', frame)
            boxes.append(box)
            # Initialize MultiTracker
            for box in boxes:
                multiTracker.add(cv2.TrackerMIL_create(), frame, box)
        # -----------------------------------------------------------------

        if len(boxes) > 0:
            success, boxes = multiTracker.update(frame)
            # draw tracked objects
            for i, newbox in enumerate(boxes):
                coord = map(int,newbox)
                x,y,w,h = coord

                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                cv2.rectangle(frame, p1, p2,(0,255,0), thickness, 1)

                absolute_x = (p1[0]+p2[0])/float(2*width)
                X = absolute_x#/width


                absolute_y = (p1[1]+p2[1])/float(2*height)
                Y = absolute_y #/ height

                absolute_w = float(abs(p2[0] - p1[0]))/width
                absolute_h = float(abs(p2[1] - p1[1])) / height

        cv2.putText(frame, str(sampel_number), (80, 120), cv2.FONT_HERSHEY_SIMPLEX, 4.0, (0, 255, 0), lineType=cv2.LINE_AA)
        cv2.imshow('window', frame)
        '''
        < class_number > (< absolute_x > / < image_width >)( < absolute_y > / < image_height >) (
                    < absolute_width > / < image_width >)( < absolute_height > / < image_height >)
                    
                    My Image Size: 360 * 480 it have one object ie:dog
        image_width = 360
        image_height = 480
        absolute_x = 30 (dog x position from image)
        absolute_y = 40 (dog y position from image)
        absolute_height = 200 (original height of dog from image)
        absolute_width = 200 (original width of dog from image)
        '''

        string = str(' {} {} {} {} {}\n'.format(class_name, X, Y, absolute_w, absolute_h))
        if mode == 1:
           string=''
        wr = open(os.path.join(text_dir,'{}{}.txt'.format(current_time,sampel_number)), 'w')
        #wr = open(os.path.join(text_dir, '{}.txt'.format(sampel_number)), 'w')
        string = string.replace('\r',' ')
        wr.write(string)


        cv2.imwrite(os.path.join(img_dir, '{}{}.jpg'.format(current_time,sampel_number)), img)
        #cv2.imwrite(os.path.join(img_dir, '{}.jpg'.format(sampel_number)), img)

        if sampel_number == 0:
            exit()

        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()

def get_last_index_from_dir(directory):
    if len(os.listdir(directory)):
        print('files here')
    else:
        print('no files here')
     #    file_list = os.listdir(directory)
     # = file_list
if __name__ == '__main__':

    OUTPUT_DIR = args.output_dir
    CLASS_NAME = args.class_name
    SAMPEL_NUMBER = args.sampel_number
    MODE = args.mode
    INDEX = args.index_from

    __main__(OUTPUT_DIR,CLASS_NAME,SAMPEL_NUMBER,MODE,INDEX)
