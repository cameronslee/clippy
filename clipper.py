import pandas as pd
from helpers import perror
from moviepy.editor import VideoFileClip

# mac booshit
# https://github.com/Zulko/moviepy/issues/1158
import platform
import os
if platform.system() == 'Darwin':
    os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

# the heart and soul of the clipping algorithm: a vectorized version of maximum subarray sum
def mss(df):
    res = []
    curr_max = float('-inf')
    global_max = 0
    #curr_start_time = df['start_time'][0]
    #curr_end_time = df['end_time'][0]
    curr_start_time = 0
    curr_end_time = 0

    for index, row in df.iterrows():
        global_max += row['weight']

        if global_max > curr_max:
            curr_max = global_max
            curr_end_time = row['end_time']
            res.append((curr_start_time, curr_end_time, (curr_end_time - curr_start_time), global_max))

        if global_max < 0:
            global_max = 0
            curr_start_time = row['start_time']

    return sorted(res, key=lambda element: (element[2], element[3]), reverse=True)

def make_clips(video_file, input_file, output_dir):
    try:
        df = pd.read_csv(input_file)
    except:
        perror("could not read " + input_file)
        exit(1)
    try:
        clips = mss(df)
        print(clips)
    except:
        perror("could not calculate clip weights") 
        exit(1)

    try:
        v = VideoFileClip(video_file)
        for i in range(len(clips)):
            curr = v.subclip(clips[i][0], clips[i][1])
            curr.write_videofile(output_dir+str(i)+"_"+str(clips[i][3])+".mp4", codec="libx264", audio_codec="aac")
    except:
        perror("could not generate clips")
        exit(1)
