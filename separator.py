import json
import random
from sklearn.model_selection import train_test_split


def separate():
    # Load the JSON dataset
    with open('./datasets/final_dataset.json', 'r', encoding='utf-8') as file:
        dataset = json.load(file)
    print('loaded')
    # Extract midi and musicxml transcriptions
    midi_transcriptions = []
    musicxml_transcriptions = []

    for entry in dataset.values():
        midi_transcriptions.append(entry['midi'])
        musicxml_transcriptions.append(entry['musicxml'])

    # Split data into train and validation sets
    print('sampling')
    # Split data into train and validation sets
    train_midi, val_midi, train_musicxml, val_musicxml = train_test_split(
        midi_transcriptions, musicxml_transcriptions, test_size=0.1, random_state=42
    )
    print('finished')

    # Write train data to files
    with open('./datasets/src-train.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(train_midi))

    with open('./datasets/tgt-train.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(train_musicxml))

    # Write validation data to files
    with open('./datasets/src-val.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(val_midi))

    with open('./datasets/tgt-val.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(val_musicxml))
