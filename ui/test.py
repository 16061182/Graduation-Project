import cv2
img0 = cv2.cvtColor(cv2.imread('./icon/status_0.png'), cv2.COLOR_BGR2RGB)
cv2.imshow('kk', img0)
cv2.waitKey(0)