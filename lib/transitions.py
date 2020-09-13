import random

import ffmpeg


def applyTransitions(
    image_paths, image_dimensions, transition_name, frame_duration, transition_duration
):
    """
    Apply transition effect to given images and return a concatenated input stream with effects applied

    :param image_paths list(Path): List of paths to images to be used
    :param image_dimensions tuple(int,int): Width and heaght of each image to adjust to
    :param transition_name str: Name if transition effect to apply
    :param frame_duration int: Duration for each frame to be displayed
    :param transition_duration int: Duration for the transition effect to last
    """
    im_streams = []
    valid_transitions = [
        "fade",
        "fadeblack",
        "fadewhite",
        "distance",
        "wipeleft",
        "wiperight",
        "wipeup",
        "wipedown",
        "slideleft",
        "slideright",
        "slideup",
        "slidedown",
        "smoothleft",
        "smoothright",
        "smoothup",
        "smoothdown",
        "rectcrop",
        "circlecrop",
        "circleclose",
        "circleopen",
        "horzclose",
        "horzopen",
        "vertclose",
        "vertopen",
        "diagbl",
        "diagbr",
        "diagtl",
        "diagtr",
        "hlslice",
        "hrslice",
        "vuslice",
        "vdslice",
        "dissolve",
        "pixelize",
        "radial",
        "hblur",
        "wipetl",
        "wipetr",
        "wipebl",
        "wipebr",
        "fadegrays",
    ]
    assert (
        transition_name in valid_transitions or transition_name == "random"
    ), "Invalid transition name"
    assert (transition_duration < frame_duration), "Transition duration is too long for given frame duration"

    for file in image_paths:
        im_streams.append(ffmpeg.input(file, t=frame_duration, loop=1))
    filterset = []
    offset_time = frame_duration - transition_duration
    for i in range(len(im_streams)):
        im_streams[i] = (
            im_streams[i]
            .filter(
                "scale",
                width=image_dimensions[0],
                height=image_dimensions[1],
                force_original_aspect_ratio="decrease",
            )
            .filter(
                "pad",
                width=image_dimensions[0],
                height=image_dimensions[1],
                x="(ow-iw)/2",
                y="(oh-ih)/2",
            )
            .filter("setsar", 1)
            .split()
        )
    for i in range(len(im_streams) - 1):
        transition_to_apply = transition_name
        if transition_name == "random":
            transition_to_apply = random.choice(valid_transitions)
        filterset.append(
            ffmpeg.filter(
                [im_streams[i][1], im_streams[i + 1][0]],
                "xfade",
                transition=transition_to_apply,
                duration=transition_duration,
                offset=offset_time,
            )
        )
    concat_images = ffmpeg.concat(*filterset, v=1, a=0)
    return concat_images
