import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def main():
    Gst.init(None)

    pipeline = Gst.parse_launch(
        "videotestsrc num-buffers=200 ! video/x-raw,format=UYVY,width=640,height=480,framerate=25/1 ! filesink location=output.raw"
    )

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

if __name__ == "__main__":
    main()
