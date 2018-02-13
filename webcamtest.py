import numpy as np
import cv2
from compare2set import compare2set

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('c'):
        compare2set(frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()