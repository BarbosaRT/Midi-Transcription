from midi_to_tokens import midi_to_tokens
from score_to_tokens import MusicXML_to_tokens
import os
import concurrent.futures
import music21
import json
import requests
import zipfile
from sep_instrument import sep_instuments
from mscorelib_threaded_preprocess import convert_mxl_to_mid

in_dir = 'mscorelib_piano'
out_file = 'datasets/mscorelib_piano_dataset.json'


def process_measure(midi_path, midi_score, musicxml_score, measure, output):
    measure_midi = midi_score.measure(measure)
    measure_musicxml = musicxml_score.measure(measure)

    # Create a new MIDI file for the measure
    path_midi = f'./tmp/temp_midi_{measure}.mid'
    path_xml = f'./tmp/temp_musicxml_{measure}.xml'

    try:
        measure_midi.write('midi', fp=path_midi)
        midi_tokens = ' '.join(midi_to_tokens(path_midi, steps_per_beat=24).tokens)
        measure_musicxml.write('musicxml', fp=path_xml)
        musicxml_tokens = ' '.join(MusicXML_to_tokens(path_xml))
        if musicxml_tokens == '':
            raise Exception
        output[f'{midi_path}_{measure}'] = {'midi': midi_tokens, 'musicxml': musicxml_tokens}
    except Exception as e:
        print(f'An error occurred while processing: {midi_path}_{measure}, Exception {e}')
        pass
    finally:
        if os.path.exists(path_midi):
            os.remove(path_midi)
        if os.path.exists(path_xml):
            os.remove(path_xml)


def process_files(midi_path, midi_score, musicxml_score):
    output = {}
    measures = [i for i in range(len(midi_score.parts[0]))]
    with concurrent.futures.ThreadPoolExecutor() as measure_executor:
        measure_executor.map(lambda measure: process_measure(midi_path, midi_score, musicxml_score, measure, output),
                             measures)
    return output


def tokenize_pair(midi_list, musicxml_list):
    output = {}
    if os.path.exists(out_file):
        with open(out_file, 'r', encoding='utf-8') as f:
            output = json.load(f)
    processed = 0
    for midi_path, musicxml_path in zip(midi_list, musicxml_list):
        processed += 1
        midi_score = music21.converter.parse(midi_path)
        print(f'{processed} - MIDI: {midi_path}, MusicXML: {musicxml_path}')
        if f'{midi_path}' in str(output.keys()):
            continue

        musicxml_score = music21.converter.parse(musicxml_path)
        result = process_files(midi_path, midi_score, musicxml_score)
        if result is not None:
            output.update(result)
        if processed % 10 == 0:
            print('saving')
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
    return output


def tokenize(midi_list, musicxml_list):
    with concurrent.futures.ProcessPoolExecutor() as _:
        results = tokenize_pair(midi_list, musicxml_list)

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


def run():
    """response = requests.get('http://mscorelib.com/zip/accu/all.zip')
    zip_file = 'all.zip'
    open(zip_file, "wb").write(response.content)
    print('zip file downloaded, extracting...')
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('./')
    except zipfile.BadZipfile:
        print('invalid link')"""
    print('extracting process done')
    print('Starting conversion')
    # convert_mxl_to_mid()  # Converts each piece to a midi and musicxml file

    print('Starting Separation of Instruments')
    sep_instuments()  # Gets only the pieces with a piano part

    print('Starting Writing to a Dataset')
    if not os.path.exists('./datasets'):
        os.mkdir('./datasets')
    # Get a list of performances such as there are not 2 performances of the same piece
    unique_midi_list = []
    unique_xml_list = []
    for root, dirs, files in os.walk(in_dir):
        for file in files:
            if file.endswith(".mxl"):
                mxl_path = os.path.join(root, file)
                mid_path = os.path.join(root, f"{os.path.splitext(file)[0]}.mid")
                unique_midi_list.append(mid_path)
                unique_xml_list.append(mxl_path)
    tokenize(unique_midi_list, unique_xml_list)


if __name__ == "__main__":
    run()
