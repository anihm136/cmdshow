import ffmpeg


def applyTransitions(image_paths, image_dimensions, transition_name, frame_duration, transition_duration):
    im_streams = []
    for file in image_paths:
        im_streams.append(ffmpeg.input(file, t=frame_duration, loop=1))
    filterset = []
    offset_time = frame_duration - transition_duration / 2
    for i in range(len(im_streams)):
        im_streams[i] = (
            im_streams[i]
            .filter(
                "scale",
                width=image_dimensions[0],
                height=image_dimensions[1],
                force_original_aspect_ratio="decrease",
            )
            .filter("pad", width=image_dimensions[0], height=image_dimensions[1], x="(ow-iw)/2", y="(oh-ih)/2")
            .filter("setsar", 1)
            .split()
        )
    for i in range(len(im_streams) - 1):
        filterset.append(
            ffmpeg.filter(
                [im_streams[i][1], im_streams[i + 1][0]],
                "xfade",
                transition=transition_name,
                duration=transition_duration,
                offset=offset_time,
            )
        )
    # im_streams = transition_function(im_streams)
    concat_images = ffmpeg.concat(*filterset, v=1, a=0)
    return concat_images
