from gtts import gTTS
from convert import read_format_0
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("--dataset_file", type=str, required=True)
parser.add_argument("--tld", type=str, required=True)
parser.add_argument("--output_folder", type=str, required=True)

args = parser.parse_args()

os.makedirs(args.output_folder, exist_ok=True)

(slot_tokens, slot_labels, intent_labels) = read_format_0(args.dataset_file)

for i in range(len(intent_labels)):
    print(f"{i}/{len(intent_labels)}")
    sentence = " ".join(slot_tokens[i]) 
    tts = gTTS(sentence, tld=args.tld)
    tts.save(f"{args.output_folder}/{str(i+1).zfill(3)}.mp3")
