import argparse
from os import path
from lib import createSlideshow, getImagesFromPath, orderImages

allowed_transition_types = [
    "fade",
    "random",
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
allowed_FPS = [i for i in range(1, 26)]

# allowed_quality_choices = ["fast", "best", "good"]

allowed_sound_formats = ["mp3", "wav", "au", "ogg"]
music_file_path = "lib/audio.wav"
parser = argparse.ArgumentParser()

# Arguments
parser.add_argument(
    dest="path_to_images", type=str, help="Path to dirctory containing the images."
)
parser.add_argument(
    "-m",
    "--music",
    dest="path_to_music",
    type=str,
    help="Path to the music file.",
    default=music_file_path,
)
parser.add_argument(
    "-fd",
    "--fduration",
    dest="frame_duration",
    type=int,
    help="Duration of each frame.",
    default=5,
)
parser.add_argument(
    "-td",
    "--tduration",
    dest="transition_duration",
    type=int,
    help="Duration of transition.",
    default=2,
)
parser.add_argument(
    "-t",
    "--transition",
    dest="transition_type",
    type=str,
    help="Type of transition.\nFor more clarity visit: https://trac.ffmpeg.org/wiki/Xfade",
    default="fade",
)

# parser.add_argument('-q',
# 	'--quality',
# 	dest='quality',
# 	type=str,
# 	choices=allowed_quality_choices,
# 	help="Desired Quality",
# 	default="good")

parser.add_argument(
    "-r",
    "--resolution",
    dest="resolution",
    type=str,
    help="Desired resolution",
    default="1920x1080",
)
parser.add_argument(
    "-fps",
    "--frames",
    dest="frames_per_second",
    type=int,
    help="Number of Frames per second.",
    default=15,
)
parser.add_argument(
    "-o",
    "--output",
    dest="output_path",
    type=str,
    help="Output path for the resultant sildeshow.",
    default="output.mp4",
)

args = parser.parse_args()
flag = 1

if not path.exists(args.path_to_images):
    flag = "Invalid path: " + args.path_to_images
if not path.isfile(music_file_path):
    flag = "Invalid path: " + args.path_to_music
if args.transition_type not in allowed_transition_types:
    print("Invalid transition type.")
    print(
        "Following are the list of allowed transition types:",
        *allowed_transition_types,
        sep="\n\t\t"
    )
    print("\n\nFor more clarity visit: https://trac.ffmpeg.org/wiki/Xfade\n\n")
    exit(2)
try:
    if args.path_to_music[-3:] not in allowed_sound_formats:
        print("Music file format invalid.")
        exit(2)
except:
    print("Music file invalid.")
    exit(2)

if flag == 1:
    try:
        height, width = args.resolution.split("x")
        height = int(height)
        width = int(width)
    except:
        parser.error(
            "Invalid resolution value: {user_value} ".format(user_value=args.resolution)
        )

    image_frames = [str(i) for i in getImagesFromPath(args.path_to_images)]
    sorted_images = [str(i) for i in orderImages(image_frames)]
    createSlideshow(
        sorted_images,
        args.path_to_music,
        args.frame_duration,
        args.frames_per_second,
        args.resolution.split("x"),
        args.transition_duration,
        args.transition_type,
        args.output_path,
    )

else:
    print(flag)
    exit(2)
