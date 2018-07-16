# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 14:41:27 2018

@author: ggoncalves
"""

#!/usr/bin/env python
 
import cv2
import numpy as np
 

class HeadPose():
    
    def __init__(self, cv):
        self.cv = cv;
        self.dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
        
        # 3D model points.
        self.model_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -330.0, -65.0),        # Chin
                            (-225.0, 170.0, -135.0),     # Left eye left corner
                            (225.0, 170.0, -135.0),      # Right eye right corne
                            (-150.0, -150.0, -125.0),    # Left Mouth corner
                            (150.0, -150.0, -125.0)      # Right mouth corner
                         
                        ])
        
    def setVideo(self, stream):
        im = stream;
        size = im.shape
        # Camera internals
         
        focal_length = size[1]
        center = (size[1]/2, size[0]/2)
        self.camera_matrix = np.array(
                                 [[focal_length, 0, center[0]],
                                 [0, focal_length, center[1]],
                                 [0, 0, 1]], dtype = "double"
                                 )
 
#        print ("Camera Matrix :\n {0}".format(self.camera_matrix))
        
    def getLinePoints(self, face_points):
        
        image_points = face_points;
        
        (success, rotation_vector, translation_vector) = self.cv.solvePnP(self.model_points, image_points, self.camera_matrix, self.dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
        
        if( not success ):
            return None;
        
        print ("Rotation Vector:\n {0}".format(rotation_vector))
        print ("Translation Vector:\n {0}".format(translation_vector))
        
        # Project a 3D point (0, 0, 1000.0) onto the image plane.
        # We use this to draw a line sticking out of the nose
        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, self.camera_matrix, self.dist_coeffs)
     
     
        p1 = ( int(image_points[0][0]), int(image_points[0][1]))
        p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
        
        line_points = (p1,p2)
        
        return line_points;