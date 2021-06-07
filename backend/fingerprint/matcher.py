import cv2
import numpy as np
import matplotlib.pyplot as plt

def isMatch(fImage, DbImage):
    sift = cv2.xfeatures2d.SIFT_create()
    fimage8bit = cv2.normalize(fImage, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
    keypoints_1, descriptors_1 = sift.detectAndCompute(fimage8bit, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(DbImage, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors_1,descriptors_2, k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
    goodMatches = len(good)
    #print(goodMatches)
    
    if goodMatches > 50:
        return True
    return False
