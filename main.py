# @author Siddharth
# @website www.siddharthsah.com

import streamlit as st
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2


CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
#print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt',
                               'MobileNetSSD_deploy.caffemodel')

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
#print("[INFO] starting video stream...")

camera = VideoStream(src=0).start()

time.sleep(2.0)
fps = FPS().start()

favicon = './favicon.png'
st.set_page_config(page_title='Object Detector WebApp', page_icon = favicon, initial_sidebar_state = 'auto')
# favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)

hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    """
st.markdown(hide_footer_style, unsafe_allow_html=True)

st.text("[No video is stored/saved/further used]")
#st.text("Currently, this app works best for face classification. This dataset consists of all 70k REAL faces from the Flickr dataset collected by Nvidia, as well as 70k fake faces sampled from the 1 Million FAKE faces (generated by StyleGAN) that was provided by Bojan.")
#st.text("If you do not have a photo to test, the URL is autofilled, go ahead click the Real or Fake button.")

#showing header image
st.image('./header.jpg', use_column_width=True)


st.title("Simple Object Detector using Webcam")
FRAME_WINDOW = st.image([])
#camera = cv2.VideoCapture(0)

run = True

if st.button('Stop'):
    run = False

while (run):
    frame = camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=400)

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.2:
            # extract the index of the class label from the
            # `detections`,
            idx = int(detections[0, 0, i, 1])
            # then compute the (x, y)-coordinates of  the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx],
                                         confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # show the output frame
    #cv2.imshow("Frame", imutils.resize(frame, width=500))
    FRAME_WINDOW.image(frame, use_column_width=True)
    #key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    # if key == ord("q"):
    #     break

    # update the FPS counter
    fps.update()

# camera.release()
# cv2.destroyAllWindows()

else:
    fps.stop()
    #print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    camera.stop()
    cv2.destroyAllWindows()

st.write('\n')
st.write('\n')
st.write('\n')

st.write("""
#### Made with :heart: by Siddharth """)
# st.markdown(
#     """<a href="https://www.siddharthsah.com/">siddharthsah.com</a>""", unsafe_allow_html=True,
# )
link = '[siddharthsah.com](http://www.siddharthsah.com/)'
st.markdown(link, unsafe_allow_html=True)