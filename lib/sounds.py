from pydub.playback import play
from math import ceil

def createSoundEffect(sound_file, video_length):
	sound = pydub.AudioSegment.from_wav(sound_file)
	length_sound_file = length(sound)
	if length_sound_file >= video_length:
		return
	loops_required = ceil(video_length/length_sound_file)
	new_sound = sound*loops_required
	return new_sound 

def playSound(sound_object):
	play(sound_object)