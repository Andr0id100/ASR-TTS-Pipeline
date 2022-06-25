import argparse
import os


def read_format_0(filename):
    with open(filename) as f:
        raw_data = f.readlines()

    slot_tokens, slot_labels, intent_labels = [], [], []
    for entry in raw_data:
        slot_data, intent_label = entry.split("<=>")

        slot_data = slot_data.strip()
        intent_label = intent_label.strip()

        slot_data = slot_data.split()
        tokens, labels = [], []
        for slot in slot_data:
            token, label = slot.split(':')
            tokens.append(token)
            labels.append(label)

        slot_tokens.append(tokens)
        slot_labels.append(labels)
        intent_labels.append(intent_label)

    return (slot_tokens, slot_labels, intent_labels)

def read_format_2(filename):
    with open(filename) as f:
        raw_data = f.read().split("\n\n")

    slot_tokens, slot_labels, intent_labels = [], [], []

    for entry in raw_data:
        slot_data = entry.split('\n')
        intent_label = slot_data[-1].strip()
        slot_data = slot_data[:-1]
        
        tokens, labels = [], []
        for slot in slot_data:
            token, label = slot.split()
            tokens.append(token.strip())
            labels.append(label.strip())

        slot_tokens.append(tokens)
        slot_labels.append(labels)
        intent_labels.append(intent_label)

    return (slot_tokens, slot_labels, intent_labels)


def write_format_0(filename, slot_tokens, slot_labels, intent_labels):
    assert len(slot_tokens) == len(slot_labels) == len(intent_labels)

    f = open(filename, 'w')

    for i in range(len(intent_labels)):
        tokens = slot_tokens[i]
        labels = slot_labels[i]
        intent_label = intent_labels[i]

        if intent_label == "":
            break

        for j in range(len(tokens)):
            # Remove Slot Labels
            tokens[j] = tokens[j].replace(":", "")
            if j != 0:
                f.write(" ")
            f.write(f"{tokens[j]}:{labels[j]}")
        f.write(" <=> ")
        f.write(f"{intent_label}\n")

    f.close()


def write_format_1(foldername, slot_tokens, slot_labels, intent_labels):
    assert len(slot_tokens) == len(slot_labels) == len(intent_labels)

    os.makedirs(foldername, exist_ok=True)
    f_seq_in = open(f"{foldername}/seq.in", 'w')
    f_seq_out = open(f"{foldername}/seq.out", 'w')
    f_label = open(f"{foldername}/label", 'w')

    for i in range(len(intent_labels)):
        tokens = slot_tokens[i]
        labels = slot_labels[i]
        intent_label = intent_labels[i]

        f_seq_in.write(f"{' '.join(tokens)}\n")
        f_seq_out.write(f"{' '.join(labels)}\n")
        f_label.write(f"{intent_label}\n")

    f_seq_in.close()
    f_seq_out.close()
    f_label.close()


def write_format_2(filename, slot_tokens, slot_labels, intent_labels):
    assert len(slot_tokens) == len(slot_labels) == len(intent_labels)

    f = open(filename, 'w')

    for i in range(len(intent_labels)):
        tokens = slot_tokens[i]
        labels = slot_labels[i]
        intent_label = intent_labels[i]

        for j in range(len(tokens)):
            # Remove Slot Labels
            tokens[j] = tokens[j].replace(":", "")
            f.write(f"{tokens[j]} {labels[j]}\n")
        f.write(f"{intent_label}\n\n")

    f.close()


def read_asr_transcript(filename):
    with open(filename) as f:
        raw_data = f.readlines()

    slot_tokens = []
    for entry in raw_data:
        entry = entry.strip().lower()

        slot_tokens.append(entry.split())

    return slot_tokens


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--source_format", type=int, required=True)
    parser.add_argument("--destination_format", type=int, required=True)
    parser.add_argument("--source_location", type=str, required=True)
    parser.add_argument("--destination_location", type=str, required=True)

    args = parser.parse_args()

    source_format = args.source_format
    destination_format = args.destination_format
    if source_format == 0:
        (slot_tokens, slot_labels, intent_labels) = read_format_0(
            args.source_location)
    elif source_format == 2:
        (slot_tokens, slot_labels, intent_labels) = read_format_2(
            args.source_location)

    if destination_format == 0:
        write_format_0(args.destination_location, slot_tokens,
                       slot_labels, intent_labels)
    elif destination_format == 1:
        write_format_1(args.destination_location, slot_tokens,
                       slot_labels, intent_labels)
    elif destination_format == 2:
        write_format_2(args.destination_location, slot_tokens,
                       slot_labels, intent_labels)