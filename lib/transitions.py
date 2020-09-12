import ffmpeg


def applyTransitions(
    image_paths, transition_function, frame_duration, transition_duration
):
    im_streams = []
    for file in image_paths:
        im_streams.append(ffmpeg.input(file, t=frame_duration, loop=1))
    filterset = []
    # for i in range(len(im_streams)):
    #     im_streams[i] = (
    #         im_streams[i]
    #         .filter(
    #             "scale",
    #             width=1280,
    #             height=720,
    #             force_original_aspect_ratio="decrease",
    #         )
    #         .filter("pad", width=1280, height=720, x="(ow-iw)/2", y="(oh-ih)/2")
    #         .filter("setsar", 1)
    #     )
    for i in range(len(im_streams)-1):
        filterset.append(ffmpeg.filter([im_streams[i], im_streams[i+1]], 'xfade', transition='fade', duration=1, offset=4.5))
    # im_streams = transition_function(im_streams)
    concat_images = ffmpeg.concat(*filterset, v=1, a=0)
    return concat_images
