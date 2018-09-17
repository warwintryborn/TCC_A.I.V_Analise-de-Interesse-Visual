# import the necessary packages

import time
import cv2
import threading as th
from land_mark import LandMark
from head_pose import HeadPose
from heatmap import HeatMap


def set_resolution_1080(cap):
    cap.set(3, 1920)  # Pixel horizontal
    cap.set(4, 1080)  # Pixel vertical


def set_resolution_900(cap):
    cap.set(3, 1600)  # Pixel horizontal
    cap.set(4, 900)  # Pixel vertical


def set_resolution_720(cap):
    cap.set(3, 1280)  # Pixel horizontal
    cap.set(4, 720)  # Pixel vertical


def set_resolution_480(cap):
    cap.set(3, 640)  # Pixel horizontal
    cap.set(4, 480)  # Pixel vertical


def video_stream():
    global is_HeatMap_Running;
    global heatmap

    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-p", "--shape-predictor", required=True,
    #	help="path to facial landmark predictor")
    # ap.add_argument("-r", "--picamera", type=int, default=-1,
    #	help="whether or not the Raspberry Pi camera should be used")
    # args = vars(ap.parse_args())

    # initialize the video stream and allow the cammera sensor to warmup
    print("[INFO] Preparando a câmera...")
    cap = cv2.VideoCapture(0)

    set_resolution_480(cap)

    time.sleep(1.0)

    land_mark = LandMark();
    head_pose = HeadPose(cv2);

    i = 0
    k = 0

    # Loop de frames do video
    while True:
        # Captura o frame
        ret, frame = cap.read()

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break;

        if (None is frame):
            print("[ERROR] FALHA NA CAPTURA DO VIDEO!!")
            print("[ERROR] TENTANDO NOVAMENTE")
            continue

        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        land_mark.set_video(gray);
        head_pose.set_video(gray);

        mapa = land_mark.get_land_mark();

        if (None is not mapa):  # Encontrou alguns rostos

            for face in mapa:  # Loop pelos rostos encontrados
                for (x, y) in face:
                    cv2.circle(frame, (int(x), int(y)), 2, (0, 0, 255), -1)

                points = head_pose.get_line_points(face);
                cv2.arrowedLine(frame, points[0], points[1], (255, 0, 0), 2)

        # show the frame
        cv2.imshow("Frame", frame)

    is_HeatMap_Running = False;
    cv2.destroyAllWindows();
    cap.release()

    return


def heat_map_thread():
    global heatmap
    global is_HeatMap_Running;

    heatmap = HeatMap();

    is_HeatMap_Running = True;

    while is_HeatMap_Running:

        # if (heatmap.IS_CHANGED):
        heatmap.show_map();

    return;


if __name__ == "__main__":
    heat_thread = th.Thread(target=heat_map_thread)
    heat_thread.start();

    video_stream()

    exit()
