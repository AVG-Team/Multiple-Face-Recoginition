import cv2
from main import recognition_face

listStudentInfo = recognition_face('Test/multiple.png')
print("Student Info: ", listStudentInfo)