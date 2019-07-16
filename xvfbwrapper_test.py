from xvfbwrapper import Xvfb

with Xvfb() as xvfb:
    # launch stuff inside virtual display here.
    # It starts/stops in this code block.
    xvfb.start()