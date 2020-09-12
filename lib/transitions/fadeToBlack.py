import ffmpeg

def fadeToBlack(input_streams):
    filterset = list()
    for i in input_streams[1:]:
        filterset.append(i.filter("fade", t = "in", st = 0, d = 1).filter("fade", t = "out", st = 4, d = 1))

