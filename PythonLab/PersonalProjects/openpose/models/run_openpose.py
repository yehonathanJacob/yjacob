from datetime import datetime
import cv2
protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "pose/mpi/pose_iter_160000.caffemodel"



# Read the network into Memory
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FPS,1)
#rotated
inWidth = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
inHeight = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

NUMBER_OF_FRAME = 0
start = datetime.now()
while cap.isOpened():
    success, frame = cap.read()
    if success:
        end = datetime.now()
        print(f"numer of frame: {NUMBER_OF_FRAME}, time: {end-start}")
        start=end
        NUMBER_OF_FRAME+=1
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Prepare the frame to be fed to the network
        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
        # Set the prepared object as the input blob of the network
        net.setInput(inpBlob)

        output = net.forward()

        H = output.shape[2]
        W = output.shape[3]
        # Empty list to store the detected keypoints
        points = []
        for i in range(14):
            # confidence map of corresponding body's part.
            probMap = output[0, i, :, :]
            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
            # Scale the point to fit on the original image
            x = (inWidth * point[0]) / W
            y = (inHeight * point[1]) / H
            if prob > 0:
                cv2.circle(frame, (int(x), int(y)), 15, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3,
                            lineType=cv2.LINE_AA)
                # Add the point to the list if the probability is greater than the threshold
                points.append((int(x), int(y)))
            else:
                points.append(None)

        cv2.imshow("Result", frame)
        k = cv2.waitKey(33)
        if k in [27, ord('q')]:
            exit(1)




