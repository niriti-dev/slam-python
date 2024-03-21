from display import Display
from extractor import Extractor
from convertor import cart2hom
from normalize import compute_essential_normalized, compute_P_from_essential, reconstruct_one_point, triangulation


import cv2
import numpy as np
import open3d as o3d


display = Display()
extractor = Extractor()


def process(img):
	pts1, pts2, kpts, matches = extractor.extract_keypoints(img=img)

	# converto to 3 dimensional
	points1 = cart2hom(pts1)
	points2 = cart2hom(pts2)

	img_h, img_w, img_ch = img.shape

	intrinsic = np.array([[3000,0,img_w/2],
				[0,3000,img_h/2],
				[0,0,1]])
	
	tripoints3d = []
	
    #normalize the points 
	if points1.ndim != 1 or points2.ndim != 1:
        points1_norm = np.dot(np.linalg.inv(intrinsic), points1)
        points2_norm = np.dot(np.linalg.inv(intrinsic), points2)

        E = compute_essential_normalized(points1_norm, points2_norm)


		P1 = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0]])
        