from music21 import converter
from midi_to_tokens import midi_to_tokens
import os

# Replace with the path to your music file
song = 'moonlight_sonata_3rd.mid'


def split_and_save_measures(input_file):
    # Load the music file
    score = converter.parse(input_file)

    # Initialize measure count
    measure_count = len(score.parts[0])+1
    tokens = []
    for i in range(measure_count):
        measure = score.measure(i)
        # Create a new MIDI file for the measure
        midi_filename = f'./tmp/measure_{i + 1}.midi'
        measure.write('midi', fp=midi_filename)
        midi_tokens = ' '.join(midi_to_tokens(midi_filename, steps_per_beat=24).tokens)
        tokens.append(midi_tokens)
        print(f'measure_{i + 1}.midi')
        if os.path.exists(midi_filename):
            os.remove(midi_filename)

    with open('./tokens.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(tokens))


# Example usage
if not os.path.exists('./tmp'):
    os.mkdir('./tmp')
split_and_save_measures(song)

