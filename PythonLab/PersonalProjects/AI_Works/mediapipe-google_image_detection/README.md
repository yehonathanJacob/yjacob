# MediaPipe Python Examples

This repository contains examples of using Google's MediaPipe library with Python for various computer vision tasks.

## References
- [MediaPipe Solutions](https://google.github.io/mediapipe/solutions/solutions.html)
- [Original MediaPipe Project](https://google.github.io/mediapipe/)
- [Python Samples](https://github.com/ai-coodinator/mediapipe-python)

## Installation

### Using pip (recommended)
Install the required Python packages using the provided requirements.txt file:

```shell
pip install -r requirements.txt
```

### Manual Installation
Alternatively, you can install the dependencies individually:

```shell
pip install opencv-python>=4.5.0
pip install mediapipe>=0.8.0
pip install numpy>=1.19.0
```

### System Dependencies
On Linux systems, you may need to install additional system dependencies for OpenCV:

```shell
apt-get update
apt-get install ffmpeg libsm6 libxext6 -y
```

## Docker
A Dockerfile is provided for containerized execution. Build and run the Docker container with:

```shell
docker build -t mediapipe-examples .
docker run -it --device=/dev/video0 mediapipe-examples
```

Note: The `--device=/dev/video0` flag is required to give the container access to your webcam.

## Available Examples
The `run_files` directory contains examples for various MediaPipe solutions:

- `facedetection.py` - Face detection
- `facemesh.py` - Face mesh (facial landmarks)
- `hands.py` - Hand tracking
- `holistic.py` - Combined face, pose, and hand tracking
- `objectron.py` - 3D object detection
- `pose.py` - Body pose estimation
- `self_segmentation.py` - Background removal/segmentation

## Usage
Run any example from the command line:

```shell
python run_files/hands.py
```

Press ESC to exit the application.
