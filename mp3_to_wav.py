from pydub import AudioSegment
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("--input_folder", type=str, required=True)
parser.add_argument("--output_folder", type=str, required=True)

args = parser.parse_args()

os.makedirs(args.output_folder)

for i in range(1, 894):
	print(i)
	input_file = f"{args.input_folder}{str(i).zfill(3)}.mp3"
	output_file = f"{args.output_folder}/{str(i).zfill(3)}.wav"

	sound = AudioSegment.from_mp3(input_file)
	sound = sound.set_frame_rate(22050)
	sound.export(output_file, format="wav")
