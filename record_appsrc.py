import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def generate_frame(width, height):
    # Generate a dummy frame with UYVY format
    frame_size = width * height * 2  # UYVY has 2 bytes per pixel
    frame = bytearray(frame_size)
    for i in range(0, frame_size, 2):
        frame[i] = (i // 2) % 256  # U
        frame[i + 1] = ((i // 2) + 128) % 256  # Y
    return bytes(frame)

def on_need_data(src, length, stream):
    frame = generate_frame(stream.width, stream.height)
    buffer = Gst.Buffer.new_wrapped(frame)
    src.emit("push-buffer", buffer)

def main(stream):
    Gst.init(None)

    pipeline = Gst.parse_launch(
        f"appsrc is-live=true block=true format=GST_FORMAT_TIME num-buffers=200 ! video/x-raw,format=UYVY,width={stream.width},height={stream.height},framerate={stream.fps}/1 ! filesink location=output.raw"
    )

    appsrc = pipeline.get_by_name("appsrc0")  # Get the appsrc element
    if not appsrc:
        print("Error: appsrc element not found in the pipeline.")
        return

    appsrc.connect("need-data", on_need_data, stream)

    pipeline.set_state(Gst.State.PLAYING)
    bus = pipeline.get_bus()

    while True:
        msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS | Gst.MessageType.ERROR)
        if msg:
            if msg.type == Gst.MessageType.ERROR:
                err, debug = msg.parse_error()
                print(f"Error: {err}, {debug}")
            break

    pipeline.set_state(Gst.State.NULL)

class StreamConfig:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps

if __name__ == "__main__":
    stream = StreamConfig(640, 480, 30)
    main(stream)
