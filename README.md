# Raw video recording and playback

## Prerequisites

### Fetch Docker

```bash
docker pull shalex88/opencv-4.11
```

## Usage

### Save raw video

```bash
docker run --rm -v "$(pwd)":/app -w /app shalex88/opencv-4.11 \
gst-launch-1.0 videotestsrc num-buffers=500 ! video/x-raw, format=UYVY, width=640, height=480,framerate=25/1 ! filesink location=output.raw
```

### Play raw video

```bash
docker run --rm -e DISPLAY=:0 -v /tmp/.X11-unix:/tmp/.X11-unix -v "$(pwd)":/app -w /app shalex88/opencv-4.11 \
gst-launch-1.0 filesrc location=output.raw ! rawvideoparse format=5 width=640 height=480 framerate=25/1  ! autovideosink
```