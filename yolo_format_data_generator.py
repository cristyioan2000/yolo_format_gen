import os
import cv2
import numpy as np
import time

def __main__():
    boxes =[]
    path = os.getcwd()
    add_dir = os.path.join(path,'capture\\Hand\\')
    cap = cv2.VideoCapture(0)
    frame_count = 0
    multiTracker = cv2.MultiTracker_create()
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    i = 0
    a = 100
    # while True:
    #     _,frame=cap.read()
    #     cv2.imshow('a',frame)
    #
    #     cv2.waitKey(1000)
    #     cv2.destroyAllWindows()
    #     break

    wr = open('dump.txt', 'w')
    while cap.isOpened():
        ret,frame = cap.read()
        #img = frame
        frame_count= frame_count + 1


        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

        a-=1

        if frame_count<100:
            #ret, frame = cap.read()
            next

        # one time
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
                cv2.imwrite(os.path.join(add_dir, 'open_palm_{}.jpg'.format(a)), frame)
                cv2.rectangle(frame, p1, p2,(0,255,0), thickness, 1)

                absolute_x = (p1[0]+p2[0])/2
                X = absolute_x/width

                absolute_y = (p1[1]+p2[1])/2
                Y = absolute_y / height

                absolute_w = (w/width)
                absolute_h = (h/height)

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
        string = str('open_palm_{}.jpg {} {} {} {}\n'.format(a,X,Y,absolute_w,absolute_h))

        wr.write(string)
        #print('open_palm_{}.jpg'.format(a),X,Y,absolute_w,absolute_h)


        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    __main__()