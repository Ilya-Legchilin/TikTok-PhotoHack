import sys
from threading import Thread
from shutil import copyfile
import numpy as np
import moviepy.editor as mv
from aubio import tempo, source
from set_effect import set_template

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size


filename = "song.mp3"

samplerate = 0

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = tempo("default", win_s, hop_s, samplerate)

# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 8. * hop_s

# list of beats, in samples
beats = []

# total number of frames read
total_frames = 0
i = 0
while True:
    samples, read = s()
    is_beat = o(samples)
    
    if is_beat:
      if i%2 == 0:
        this_beat = int(total_frames - delay + is_beat[0] * hop_s)
        print("%f" % (this_beat / float(samplerate)-1.6))
        beats.append(this_beat)
      i += 1
    total_frames += read
    if read < hop_s: break
i = 0
while i < s.duration/s.samplerate*25:
  name = "frames/" + str(i) + ".jpg"
  copyfile("selfie.png", name)
  i += 1
def parallel_effects(time, id):
  i = round_down(time*25)
  threads = []
  while i < s.duration/s.samplerate*25:
    threads.append(threading.Thread(target=set_template, args=(i, id)))
    
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()

i = 0
while i < s.duration/s.samplerate*25:
  names = []
  names.append("frames/" + str(i) + ".jpg")
  final.write_videofile("output.mp4")
  clip = ImageSequenceClip(names, fps=25)
  audio = mp.AudioFileClip("song.mp3")
  clip = clip.set_audio(audio.set_duration(clip))    
