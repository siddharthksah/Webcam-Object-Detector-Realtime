"""
Simple Object Detector using Webcam

This script demonstrates a simple object detection using a webcam. The script reads from a list of predefined classes 
and uses OpenCV and deep neural networks (DNN) to detect the objects in the webcam feed.

Author: Siddharth Sah
Website: www.siddharthsah.com
"""

# Import necessary libraries
import cv2
import time
import numpy as np
import imutils
import streamlit as st
from imutils.video import VideoStream, FPS
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# Predefined classes for object detection
CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
    "car", "cat", "chair", "cow", "diningtable", "dog", "horse", 
    "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

# Generate random colors for bounding boxes
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Load the serialized model from disk
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

# Set up Streamlit page configuration
favicon = './favicon.png'
st.set_page_config(page_title='Object Detector WebApp', page_icon = favicon, initial_sidebar_state = 'auto')

# Hide footer 
hide_footer_style = "<style>.reportview-container .main footer {visibility: hidden;}</style>"
st.markdown(hide_footer_style, unsafe_allow_html=True)

# App disclaimer
st.text("No video is stored/saved/further used")

# Display header image
st.image('./header.jpg', use_column_width=True)

# App title
st.title("Simple Object Detector using Webcam")

class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        """Apply object detection to the frame."""
        # Convert and resize the frame
        img = frame.to_ndarray(format="bgr24")
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=400)

        # Create a blob from the frame and perform object detection
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        # Process the detections
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        return frame

# Stream webcam feed with object detection
webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

# App credits
st.write("""
#### Made with :heart: by Siddharth""")
link = '[siddharthsah.com](http://www.siddharthsah.com/)'
st.markdown(link, unsafe_allow_html=True)
