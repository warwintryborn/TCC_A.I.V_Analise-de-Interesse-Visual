# import the necessary packages
from imutils.video import VideoStream
import imutils
import time
import cv2
import threading as th
from land_mark import LandMark
from head_pose import HeadPose
from heat_mapping import HeatMaping


def main():
    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-p", "--shape-predictor", required=True,
    #	help="path to facial landmark predictor")
    # ap.add_argument("-r", "--picamera", type=int, default=-1,
    #	help="whether or not the Raspberry Pi camera should be used")
    # args = vars(ap.parse_args())

    # initialize the video stream and allow the cammera sensor to warmup
    print("[INFO] camera sensor warming up...")
    vs = VideoStream(0).start()
    time.sleep(2.0)
    
    lm = LandMark();
    hp = HeadPose(cv2);
    global hm;
    
    hm = HeatMaping();
    
    heat_thread = th.Thread(target=heat_map_thread)
    heat_thread.start();

    global boIsHeatMapRunning;
    boIsHeatMapRunning = False

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream, resize it to
        # have a maximum width of 400 pixels, and convert it to
        # grayscale
        frame = vs.read()

        if (None is not frame):
            frame = imutils.resize(frame, width=400, height=500)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        lm.set_video(gray);
        hp.set_video(gray);

        mapa = lm.get_land_mark();

        if (None is not mapa):
            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw them on the image
            for face in mapa:

                for mark in face:
                    x = mark[0]
                    y = mark[1]
                    cv2.circle(frame, (int(x), int(y)), 2, (0, 0, 255), -1)

                points = hp.get_line_points(face);
                cv2.arrowedLine(frame, points[0], points[1], (255, 0, 0), 2)

        # show the frame
        cv2.imshow("Frame", frame)
        hm.show_map();
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    boIsHeatMapRunning = False;
    # do a bit of cleanup
    vs.stop()
    cv2.destroyAllWindows();


def heat_map_thread():
    while boIsHeatMapRunning:
        hm.show_map();
        '''
             Heat map thread!
    
             Atualizar vetor Z;
             Mostrar Heat Map;
        '''


if __name__ == "__main__":
    main()
