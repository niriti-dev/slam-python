import cv2
import numpy as np


class Extractor(object):
	def __init__(self):
		self.orb = cv2.orb = cv2.ORB_create(nfeatures=1, scoreType=cv2.ORB_FAST_SCORE)
		self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)
		self.last = None

	def extract_keypoints(self, img):
		# detection

		# goodFeaturesToTrack basically detects corners/ "strong points"
		
		if len(img.shape) > 2: # if color image 
			pts = cv2.goodFeaturesToTrack(image=np.mean(img, axis=2).astype(np.uint8), maxCorners=4500,
				qualityLevel=0.02, minDistance=3)

		else: # if not color image 
			pts = cv2.goodFeaturesToTrack(image=np.array(img).astype(np.uint8), maxCorners=4500,
				qualityLevel=0.02, minDistance=3)
		

		
		# extraction --> convert the above images to KeyPoint objects 
		kpts = [cv2.KeyPoint(p[0][0],p[0][1], size=30) for p in pts]

		kpts, des = self.orb.compute(img, kpts)

		# matching
		ret = [] # for any given two frames, contains the potential matches between the two images 
		if self.last is not None:
			matches = self.bf.knnMatch(des, self.last["des"], k=2)
			# print("MATTTCHHHESSSS", matches)
			# ((< cv2.DMatch 0x14d48b730>, < cv2.DMatch 0x14d48b710>), 
			# it returns tuples of objects like this 
			
			for m, n in matches:
				# print("m in matches: ", m)
				# print("n in matches: ", n)
				# print()
				if m.distance < 0.55* n.distance:
					if m.distance < 64:
						kpt1_match = kpts[m.queryIdx]
						# print("kpts1_match: ", kpt1_match )
						kpt2_match = self.last["kpts"][m.trainIdx]
						# print("kpts2_match: ", kpt2_match )
						ret.append((kpt1_match, kpt2_match))

			coords1_match_pts = np.asarray([kpts[m.queryIdx].pt for m,n in matches])  # (3,8)
			coords2_match_pts = np.asarray([self.last["kpts"][m.trainIdx].pt for m,n in matches]) # (3, 15)
			
			# find transformation between two matched points
			retval, mask = cv2.findHomography(coords1_match_pts, coords2_match_pts, cv2.RANSAC, 100.0)
			mask = mask.ravel()

			pts1 = coords1_match_pts[mask==1]
			pts2 = coords2_match_pts[mask==1]

			
			# so you don't save the image, you save the key points of this image 
			# and the descriptors of this image 
			self.last = {"kpts":kpts, "des":des}
			return pts1.T, pts2.T, kpts, ret
		
		else:
			self.last = {"kpts":kpts, "des":des}
			return np.array([0]),np.array([0]), 0, 0
		
