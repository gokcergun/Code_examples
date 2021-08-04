import cv2


# capture computer camera
cap = cv2.VideoCapture('videomotor_short.mp4') ## cv2.VideoCapture(0)  0 means read from local camera.

#create a tracker
#tracker = cv2.legacy.TrackerMOSSE_create() ## much more faster but less accurate
tracker = cv2.TrackerCSRT_create() #CSRTuses a more slower but more accurate tracker

# take a frame
success, img = cap.read()
# create the bounding box - these are tuples
bbox = cv2.selectROI("Tracking", img, False)
#initiate the tracker
tracker.init(img, bbox)

#create a function for drawing bounding boxes
def drawBox(img, bbox):
    # x and y are initial x- and y-coordinates. w is width and h is height
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img,(x, y),(x+w, y+h),(0,255,0), 3, 1)
    cv2.putText(img, 'Tracking', (75,75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

while True:
    timer = cv2.getTickCount()
    success, img = cap.read()  # img will give us our frame
    success, bbox = tracker.update(img)

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, 'Lost', (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # calculate frame per second
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Tracking", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break