# import th*e necessary packages-/
from imutils import face_utils
import dlib
import numpy as np


class LandMark():
    __face = [];

    def __init__(self):
        print("[INFO] loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("./face_predictor/shape_predictor_68_face_landmarks.dat")

    def set_frame(self, frame):
        self.frame = frame;

    def get_land_mark(self):
        rects = self.detector(self.frame, 1);
        self.__face.clear();
        self.aux = []

        # loop over the face detections
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            self.__shape = self.predictor(self.frame, rect)
            self.__shape = face_utils.shape_to_np(self.__shape)

            self.aux.append(self.__shape)

            QUEIXO = self.__shape[8];
            NARIZ = self.__shape[30];
            BOCA_ESQUERDO = self.__shape[54];
            BOCA_DIREITO = self.__shape[48];
            OLHO_ESQUERDO = self.__shape[45];
            OLHO_DIREITO = self.__shape[36];

            self.__face.append(np.array([
                NARIZ,  # Nose tip
                QUEIXO,  # Chin
                OLHO_ESQUERDO,  # Left eye left corner
                OLHO_DIREITO,  # Right eye right corne
                BOCA_ESQUERDO,  # Left Mouth corner
                BOCA_DIREITO  # Right mouth corner
            ], dtype="double"))

        return self.__face;

    @property
    def shape(self):
        return self.aux

if (__name__ == '__main__'):
    lm = LandMark
