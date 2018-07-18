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
    
    def setVideo(self, gray):
        self.gray = gray;
    
    def getLandMark(self):
        
        rects = self.detector(self.gray, 1);
        self.__face.clear();
        
        # loop over the face detections
        for (i, rect) in enumerate(rects):            
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = self.predictor(self.gray, rect)
            shape = face_utils.shape_to_np(shape)
            
            QUEIXO = shape[8];
            NARIZ = shape[30];
            BOCA_ESQUERDO = shape[54];
            BOCA_DIREITO = shape[48];
            OLHO_ESQUERDO = shape[45];
            OLHO_DIREITO = shape[36];
            
            self.__face.append( np.array([
                            NARIZ,              # Nose tip
                            QUEIXO,             # Chin
                            OLHO_ESQUERDO,      # Left eye left corner
                            OLHO_DIREITO,       # Right eye right corne
                            BOCA_ESQUERDO,      # Left Mouth corner
                            BOCA_DIREITO        # Right mouth corner
                        ], dtype="double"))
            print(i)
            return self.__face;