import subprocess
import sys
import ffmpeg
import pathlib
from nicelog import setup_logging
from nicelog.formatters import Colorful
import logging 

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(Colorful(
    show_date=True,
    show_function=True,
    show_filename=True,
    message_inline=True,
    ))
handler.setLevel(logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def get_file_duration(filename) :
  try : 
    probe = ffmpeg.probe(filename, format="duration")
    return probe['streams'][0]['duration'] 
  except  ffmpeg.Error as e:
    print('stdout:', e.stdout.decode('utf8'))
    print('stderr:', e.stderr.decode('utf8'))
    raise e


def generate_interval(file, outfile, start, end ):
  stream = ffmpeg.input(file, ss=start, t=end)
  
  stream = ffmpeg.output(stream, outfile)
  
  ffmpeg.run(stream)


def validate_args(file, inf, of) :
  if not file.exists :
    logger.error(f"input file:{file} not found")
    return False

  if inf not in ['.mp3', '.ogg'] :
    logger.error(f"unsupported input format")
    return False  

  if of not in ['.mp3', '.ogg'] :
    logger.error(f"unsupported output format")
    return False
  
  return True

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='simple utility to segment an audio file with ffmpeg')
  parser.add_argument('--interval',         "-v", help="segment interval in seconds [default: 15] ", default=15)
  parser.add_argument('--input-audio',      "-i", help="source file", required=True)
  parser.add_argument('--output-directory', "-d", help="output directory to store the segments [default: out]", default="out")
  parser.add_argument('--manifest-file',    "-m", help="name of manifest file [default: <file-name>.<format>]")
  parser.add_argument('--filename-format',  "-s", help="printf style format string for the output files [default: <file-name>-<%d>.<output-format>]")
  parser.add_argument('--output-format',    "-f", help="output media format for segment files [default: <input-format>]")
  args = parser.parse_args()
  infile = pathlib.Path(args.input_audio)
  if args.output_format is None :
    args.output_format = infile.suffix
  if not validate_args(infile, infile.suffix, args.output_format) :
    logger.error("argument validation error. exiting...")
    exit(-1)

  outdir = pathlib.Path(args.output_directory)
  if not outdir.exists() :
    outdir.mkdir()
  
  duration = get_file_duration(infile)
  intervals = float(duration)/int(args.interval)
  logger.info(f"{duration} producing {intervals} intervals to {args.output_directory}")  
  stem = infile.stem
  i = 0
  while i < intervals:
    path = pathlib.Path(outdir, f"{stem}-{i:03}{args.output_format}")
    logger.info(f"writing {path}")
    generate_interval(infile, str(path), int(args.interval) * i, int(args.interval))
    i += 1



