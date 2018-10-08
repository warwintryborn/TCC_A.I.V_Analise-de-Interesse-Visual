# import the necessary packages

import time
import cv2
from multipledispatch.conflict import super_signature

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

    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-p", "--shape-predictor", required=True,
    #	help="path to facial landmark predictor")
    # ap.add_argument("-r", "--picamera", type=int, default=-1,
    #	help="whether or not the Raspberry Pi camera should be used")
    # args = vars(ap.parse_args())

    # initialize the video stream and allow the cammera sensor to warmup
    global sup_esq, sup_dir, inf_esq, inf_dir, vitrine_larg_altu, divisao_colum_row

    sup_esq = None;
    sup_dir = None;
    inf_esq = None;
    inf_dir = None;
    vitrine_larg_altu = None;

    print("[INFO] Preparando a câmera...")
    cap = cv2.VideoCapture(0)

    set_resolution_480(cap)

    time.sleep(1.0)

    land_mark = LandMark();
    head_pose = HeadPose(cv2);
    heatmap_global = HeatMap("Diário");
    heatmap_usuario = HeatMap("Usuário");

    # Loop de frames do video
    while True:
        # Captura o frame
        ret, frame = cap.read()

        key = cv2.waitKey(100) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break;
        if key == ord("s"):
            heatmap_global.salve_map();
            heatmap_usuario.salve_map();
            print("[INFO] HeatMap salvo!!");

        if key == ord("r"):
            heatmap_usuario.reset_map();
            heatmap_global.reset_map()
            print("[INFO] HeatMap resetado!!");

        if key == ord("b"):
            comecar_leitura_unica = True;
            print("[INFO] Leitura de usuário começado!!");
        if key == ord("e"):
            comecar_leitura_unica = False;
            print("[INFO] Leitura de usuário parado!!");

        if (head_pose.vitrine_points != None):
            if key == ord("7"):
                sup_esq = head_pose.vitrine_points;
                print("[INFO] Ponto superior esquerdo capturado!!");
            if key == ord("9"):
                sup_dir = head_pose.vitrine_points;
                print("[INFO] Ponto superior direito capturado!!");
            if key == ord("1"):
                inf_esq = head_pose.vitrine_points;
                print("[INFO] Ponto inferor esquerdo capturado!!");
            if key == ord("3"):
                inf_dir = head_pose.vitrine_points;
                print("[INFO] Ponto inferior direito capturado!!");

        if key == ord("5"):
            sup_esq = None;
            sup_dir = None;
            inf_esq = None;
            inf_dir = None;
            vitrine_larg_altu = None;
            print("[INFO] Calibração resetada!!");

        if key == ord("c"):
            if ( sup_esq != None and sup_dir != None and inf_esq != None and inf_dir != None):
                vitrine_larg_altu = calibrar_vitrine(sup_esq, sup_dir, inf_esq, inf_dir);
                divisao_colum_row = [0 , 0]
                divisao_colum_row[0] = int(vitrine_larg_altu[0] / heatmap_global.width);
                divisao_colum_row[1] = int(vitrine_larg_altu[1] / heatmap_global.higth);
                print("[INFO] Calibração feita!!");

        if (None is frame):
            print("[ERROR] FALHA NA CAPTURA DO VIDEO!!")
            print("[ERROR] TENTANDO NOVAMENTE")
            continue

        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        land_mark.set_frame(gray);
        head_pose.set_frame(gray);

        mapa = land_mark.get_land_mark();

        if (None is not mapa):  # Encontrou alguns rostos

            for face in mapa:  # Loop pelos rostos encontrados
                for (x, y) in face:
                    cv2.circle(frame, (int(x), int(y)), 2, (0, 0, 255), -1)

                points = head_pose.get_line_points(face);
                cv2.arrowedLine(frame, points[0], points[1], (255, 0, 0), 2)

                # Adicionar regra de tempo para saber a partir de quanto tempo começa a contar
                if ( head_pose.vitrine_points != None):


                    if ( sup_esq != None and vitrine_larg_altu != None):
                        coordenada_heat = global2heat(sup_esq, head_pose.vitrine_points);
                        heatmap_global.incrementa(coordenada_heat)


        # show the frame
        cv2.imshow("Frame", frame)

    heatmap_global.salve_map()
    heatmap_usuario.salve_map()

    cv2.destroyAllWindows();
    cap.release()

    return


def calibrar_vitrine(sup_esq, sup_dir, inf_esq, inf_dir):

    largura = abs(sup_esq[0]) + abs(sup_dir[0]);
    altura = abs(sup_esq[1]) + abs(inf_esq[1]);

    return (abs(largura), abs(altura))


def global2heat(ponto_zero, vitrine_points):
    global divisao_colum_row, sup_esq, sup_dir, inf_esq, inf_dir;
    pontos_heat = [-1, -1];

    if( vitrine_points[0] < ponto_zero[0] ):
        pontos_heat[0] = int(abs(ponto_zero[0] - vitrine_points[0]) / divisao_colum_row[0]);

    if( vitrine_points[1] < ponto_zero[1] ):
        pontos_heat[1] = int(abs(ponto_zero[1] - vitrine_points[1]) / divisao_colum_row[1]);

    return pontos_heat


if __name__ == "__main__":

    video_stream()

    exit()
