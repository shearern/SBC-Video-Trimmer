import os
import sys
import subprocess
import gflags
import json

gflags.DEFINE_string(
    'ffprobe',
    help = "Path to ffprobe program",
    default = None)


def exec_ffprobe(*cmd):

    # Find ffprobe
    executable = None
    search_dirs = sys.path[:]
    search_dirs.append(os.curdir)
    for parent in search_dirs:
        if executable is None:
            for filename in ('ffprobe', 'ffprobe.exe'):
                path = os.path.join(parent, filename)
                if os.path.exists(path):
                    executable = path
                    break

    if executable is None:
        raise Exception("Can't find ffprobe")

    # Prep command
    cmd = [executable, ] + list(cmd)

    # Execute
    return subprocess.check_output(cmd, stdin=None)


class FFProbeData(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    @property
    def streams(self):
        if self.raw_data.has_key('streams'):
            return self.raw_data['streams'][:]


    @property
    def video_stream(self):
        vid_stream = None
        for stream in self.streams:
            if stream['codec_type'] == 'video':
                if vid_stream is not None:
                    raise Exception("Multiple video streams found")
                vid_stream = stream
        if vid_stream is None:
            raise Exception("No video streams found")
        return vid_stream


    @property
    def framerate(self):
        '''Number of frames per second'''
        try:
            rate_str = self.video_stream['r_frame_rate']
        except AttributeError:
            try:
                rate_str = self.video_stream['avg_frame_rate']
            except AttributeError:
                raise Exception("Couldn't find framerate in data")

        if '/' in rate_str:
            parts = rate_str.split("/")
            return float(parts[0]) / float(parts[1])


    @property
    def duration_sec(self):
        '''Duration of the video file in miliseconds'''
        try:
            str_value = self.video_stream['duration']
        except AttributeError:
            raise Exception("Couldn't find duration in data")

        return float(str_value)


def get_file_data(path):

    # Call ffprobe to get data
    data_str = exec_ffprobe(
        '-show_format',
        '-show_streams',
        '-of', 'json',
        '-i', path,
        )

    # Parse Data
    data = json.loads(data_str)
    return FFProbeData(data)