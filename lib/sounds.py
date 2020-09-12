from pydub.playback import play
from math import ceil
import pydub

def createSoundEffect(sound_file, video_length):
	sound = pydub.AudioSegment.from_wav(sound_file)
	length_sound_file = len(sound)
	if length_sound_file >= video_length:
		return
	loops_required = ceil(video_length/length_sound_file)
	new_sound = sound*loops_required
	return new_sound 

def playSound(sound_object):
	play(sound_object)

# FOR TESTING: 
'''
sound = pydub.AudioSegment.from_wav("audio.wav")
length_sound_file = len(sound)
print("LENGTH: ",length_sound_file)
print("Playing once: ")
play(sound)
sound1 = sound*2
print("LENGTH: ", len(sound1))
print("Playing twice: ")
play(sound1)
'''