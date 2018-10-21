# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 14:41:27 2018

@author: ggoncalves
"""

# !/usr/bin/env python

import cv2
import numpy as np


class HeadPose():

    RANGE_CABECA_FRENTE = 15
    FATOR_INCREMENTO_CENTRO = 0.015

    @property
    def vitrine_points(self):
        return self.__vitrine_points

    def __init__(self, cv):
        self.cv = cv;
        self.dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion

        # 3D model points.
        self.model_points = np.array([
            (0.0, 0.0, 0.0),  # Nose tip
            (0.0, -330.0, -65.0),  # Chin
            (-225.0, 170.0, -135.0),  # Left eye left corner
            (225.0, 170.0, -135.0),  # Right eye right corne
            (-150.0, -150.0, -125.0),  # Left Mouth corner
            (150.0, -150.0, -125.0)  # Right mouth corner

        ])
        self.__vitrine_points = (0, 0);

    def set_frame(self, frame):
        im = frame;
        size = im.shape

        # Camera internals

        focal_length = size[1]
        center = (size[1] / 2, size[0] / 2)
        self.camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )

    def get_line_points(self, face_points):
        image_points = face_points;

        (success, rotation_vector, translation_vector) = self.cv.solvePnP(self.model_points, image_points,
                                                                          self.camera_matrix, self.dist_coeffs,
                                                                          flags=cv2.SOLVEPNP_ITERATIVE)

        # (success, rotation_vector, translation_vector, inliers) = self.cv.solvePnPRansac(self.model_points, image_points,
        #                                                                   self.camera_matrix, self.dist_coeffs,
        #                                                                     iterationsCount=10, reprojectionError=8,
        #                                                                     confidence=0.9, flags=cv2.SOLVEPNP_ITERATIVE)

        if (not success):
            return None;

        distance = abs(-0.5 * translation_vector[2]);

        soma = self._cento(image_points);

        if( self.RANGE_CABECA_FRENTE >= soma >= ( -self.RANGE_CABECA_FRENTE )  ):
            rotation_vector[1] = soma * -self.FATOR_INCREMENTO_CENTRO;

        # We use this to draw a line sticking out of the nose
        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, distance)]),
                                                         rotation_vector,
                                                         translation_vector, self.camera_matrix, self.dist_coeffs)

        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

        self.__vitrine_points = ( p1[0] - p2[0], p1[1] - p2[1] );

        line_points = (p1, p2);

        return line_points;

    def _cento(self, image_points):
        nariz_x = image_points[0][0];
        olho_dir_x = image_points[3][0];
        olho_esq_x = image_points[2][0];

        return (nariz_x - olho_esq_x) + (nariz_x - olho_dir_x);


if (__name__ == '__main__'):
    hp = HeadPose
