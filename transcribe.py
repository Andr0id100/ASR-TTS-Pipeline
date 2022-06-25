import speech_recognition as sr
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--input_folder", type=str, required=True)
parser.add_argument("--language", type=str, required=True)
parser.add_argument("--output_file", type=str, required=True)

args = parser.parse_args()

r = sr.Recognizer()

f = open(args.output_file, 'w')

# Fix this when generalizing in the future, count files using some os util
for i in range(1, 894):
	print(i)
	filename = f"{args.input_folder}{str(i).zfill(3)}.wav"
	with sr.AudioFile(filename) as source:
		audio = r.record(source)
	try:
		transcribed = r.recognize_google(audio, language=args.language)
	except sr.UnknownValueError:
		print("Error at entry", i)
		transcribed = ""
	print(transcribed, end="\n\n")
	f.write(transcribed)
	f.write('\n')
f.close()
