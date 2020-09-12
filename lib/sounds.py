from pydub.playback import play
from math import ceil
import pydub

def createSoundEffect(sound_file, video_length = 20):
	sound = pydub.AudioSegment.from_file(sound_file)
	length_sound_file = len(sound)/1000
	if length_sound_file >= video_length:
		return
	loops_required = ceil(video_length/length_sound_file)
	new_sound = sound*loops_required
	new_sound.export("new_audio.wav", format="wav") 

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
sound1.export("new_audio.wav", format="wav")
'''
# createSoundEffect("audio.wav")
