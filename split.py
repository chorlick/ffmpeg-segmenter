import subprocess
import sys


def main():
    """split a music track into specified sub-tracks by calling ffmpeg from the shell"""

    # check command line for original file and track list file
    if len(sys.argv) != 3:
        print("usage: split <original_track> <segment_length>")
        exit(1)

    # record command line args
    original_track = sys.argv[1]
    track_list = sys.argv[2]

    # create a template of the ffmpeg call in advance
    cmd_string = f'ffmpeg -i {tr} -acodec copy -ss {st} -to {en} {nm}.opus'

    # read each line of the track list and split into start, end, name
    with open(track_list, 'r') as f:
        for line in f:
            # skip comment and empty lines
            if line.startswith('#') or len(line) <= 1:
                continue

            # create command string for a given track
            start, end, name = line.strip().split()
            command = cmd_string.format(
                tr=original_track, st=start, en=end, nm=name)

            # use subprocess to execute the command in the shell
            subprocess.call(command, shell=True)

    return None


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='simple utility to segment an audio file')
  parser.add_argument('integers', metavar='N', type=int, nargs='+',
                      help='an integer for the accumulator')
  parser.add_argument('--sum', dest='accumulate', action='store_const',
                      const=sum, default=max,
                      help='sum the integers (default: find the max)')

  args = parser.parse_args()
  print(args.accumulate(args.integers))
  main()
