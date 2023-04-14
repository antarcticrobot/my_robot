import os

m4a_path = "/home/yr/catkin_ws/src/my_robot/scripts/voice/input/"
m4a_file = os.listdir(m4a_path)
print(m4a_file)

for i, m4a in enumerate(m4a_file):
    if m4a.endswith('.m4a'):
        wav_name = m4a_path+m4a.split(".m4a")[0]+".wav"
        os.system("ffmpeg -i " + m4a_path + m4a + " " + wav_name)
