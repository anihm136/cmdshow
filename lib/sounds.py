from math import ceil
import pydub


def createSoundEffect(sound_file, video_length):
    """
    Adjust sound_file to given length, and write a new file from it

    :param sound_file Path: Path to sound file
    :param video_length int: Length of the video to adjust to
    """
    allowed_sound_formats = ["mp3", "wav", "au", "ogg"]

    try:
        extension = sound_file[-3:]
        if extension not in allowed_sound_formats:
            print("Music file format invalid.")
            exit(2)
    except:
        print("Music file invalid.")
        exit(2)
    sound = pydub.AudioSegment.from_file(sound_file)
    length_sound_file = len(sound) / 1000
    if length_sound_file >= video_length:
        return
    loops_required = ceil(video_length / length_sound_file)
    new_sound = sound * loops_required
    new_sound.export("new_audio.{ext}".format(ext=extension), format=extension)


# FOR TESTING:
"""
sound = pydub.AudioSegment.from_wav("audio.wav")
length_sound_file = len(sound)
print("LENGTH: ",length_sound_file)
print("Playing once: ")
play(sound)
new_sound = sound*2
print("LENGTH: ", len(new_sound))
print("Playing twice: ")
play(new_sound)
new_sound.export("new_audio.wav", format="wav")
"""
# createSoundEffect("audio.wav")
