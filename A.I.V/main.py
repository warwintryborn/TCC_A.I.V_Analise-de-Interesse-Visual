# import the necessary packages
from imutils.video import VideoStream
import imutils
import time
import cv2
import threading as th
from land_mark import LandMark
from head_pose import HeadPose
from heat_map import HeatMaping


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
    
    land_mark = LandMark();
    head_pose = HeadPose(cv2);

    global heat_map
    heat_map = HeatMaping();

    global is_Heat_Map_Running;
    is_Heat_Map_Running = True;

    heat_thread = th.Thread(target=heat_map_thread)
    heat_thread.start();

    # Loop de frames do video
    while True:
        # Captura o frame
        frame = vs.read()

        if (None is not frame):
            frame = imutils.resize(frame, width=400, height=400)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        land_mark.set_video(gray);
        head_pose.set_video(gray);

        mapa = land_mark.get_land_mark();

        if (None is not mapa): #Encontrou alguns rostos

            for face in mapa:   #Loop pelos rostos encontrados
                for (x, y) in land_mark.show_all:
                    cv2.circle(frame, (int(x), int(y)), 2, (0, 0, 255), -1)

                points = head_pose.get_line_points(face);
                cv2.arrowedLine(frame, points[0], points[1], (255, 0, 0), 2)

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    is_Heat_Map_Running = False;

    vs.stop()
    cv2.destroyAllWindows();


def heat_map_thread():
    while is_Heat_Map_Running:

        # Atualizar os valores do heatmap
        # Salvar a imagem em um arquivo
        # Plotar em uma janela separada o heatmap sempre atualizado
        '''
        Mostrar heatmap em paralelo com o video
        '''

if __name__ == "__main__":
    main()