import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import numpy as np
from util import *
import sudoku_solver as sudokuSolver

pathImage = input("Image:")
heightImg = 450
widthImg = 450
model = initializePredictionModel()

img = cv2.imread(pathImage)
img = cv2.resize(img, (widthImg, heightImg))
imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
imgThreshold = preProcess(img)

imgContours = img.copy()
imgBigContour = img.copy()
contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

biggest, maxArea = biggestContour(contours)
if biggest.size != 0:
    biggest = reorder(biggest)
    cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 10)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    imgDetectedDigits = imgBlank.copy()
    imgWarpColored = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)

imgSolvedDigits = imgBlank.copy()
boxes = splitBoxes(imgWarpColored)
numbers = getPrediction(boxes, model)
grid = [numbers[i:i+9] for i in range(0, 81, 9)]
imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
numbers = np.asarray(numbers)
posArray = np.where(numbers > 0, 0, 1)

board = np.array_split(numbers, 9)
try:
    sudokuSolver.solve(board)
except:
    pass

flatlist = []
for sublist in board:
    for item in sublist:
        flatlist.append(item)
solvedNumbers = flatlist * posArray
imgSolvedDigits = displayNumbers(imgSolvedDigits, solvedNumbers)
imgSolved = cv2.addWeighted(imgSolvedDigits, 1, imgDetectedDigits, 0.5, 1)

pts2 = np.float32(biggest)
pts1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
imgInvWarpColored = img.copy()
imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (widthImg, heightImg))
inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
imgDetectedDigits = drawGrid(imgDetectedDigits)
imgSolvedDigits = drawGrid(imgSolvedDigits)
imgSolved = drawGrid(imgSolved)

imageArray = ([img, imgThreshold, imgContours], [imgBigContour, imgWarpColored,imgDetectedDigits], [imgSolved, imgInvWarpColored, inv_perspective])
stackedImage = stackImages(imageArray, 0.5)
cv2.imshow('Stacked Images', stackedImage)
cv2.waitKey(0)