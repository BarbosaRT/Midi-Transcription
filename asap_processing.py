import pandas as pd
from pathlib import Path
from midi_to_tokens import midi_to_tokens
from score_to_tokens import MusicXML_to_tokens
import os
import concurrent.futures
import music21
import json
import requests
import zipfile

BASE_PATH = "./asap-dataset-master"


def process_measure(midi_path, midi_score, musicxml_score, measure, output):
    measure_midi = midi_score.measure(measure)
    measure_musicxml = musicxml_score.measure(measure)

    # Create a new MIDI file for the measure
    path_midi = f'./tmp/temp_midi_{measure}.mid'
    path_xml = f'./tmp/temp_musicxml_{measure}.xml'

    measure_midi.write('midi', fp=path_midi)
    try:
        # measure_midi.write('midi', fp=path_midi)
        measure_musicxml.write('musicxml', fp=path_xml)
        midi_tokens = ' '.join(midi_to_tokens(path_midi, steps_per_beat=24).tokens)
        musicxml_tokens = ' '.join(MusicXML_to_tokens(path_xml))
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
    try:
        measures = [i for i in range(len(midi_score.parts[0]))]

        with concurrent.futures.ThreadPoolExecutor() as measure_executor:
            measure_executor.map(lambda measure: process_measure(midi_path, midi_score, musicxml_score, measure, output),
                                 measures)
    except Exception as e:
        print(f'An error occurred in process_files while processing: {midi_path}, Exception {e}')
    return output


def tokenize_pair(midi_list, musicxml_list):
    output = {}
    if os.path.exists('datasets/asap_dataset.json'):
        with open(f'datasets/asap_dataset.json', 'r', encoding='utf-8') as f:
            output = json.load(f)
    processed = 0
    for midi_file, musicxml_file in zip(midi_list, musicxml_list):
        processed += 1
        midi_path = os.path.join(BASE_PATH, midi_file)
        musicxml_path = os.path.join(BASE_PATH, musicxml_file)
        print(f'{processed} - MIDI: {midi_path}, MusicXML: {musicxml_path}')
        if f'{midi_path}_1' in output.keys():
            continue

        midi_score = music21.converter.parse(midi_path)
        musicxml_score = music21.converter.parse(musicxml_path)

        result = process_files(midi_path, midi_score, musicxml_score)
        if result is not None:
            output.update(result)
        if processed % 10 == 0:
            print('saving')
            with open(f'datasets/asap_dataset.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
    return output


def tokenize(midi_list, musicxml_list):
    with concurrent.futures.ProcessPoolExecutor() as _:
        results = tokenize_pair(midi_list, musicxml_list)

    with open(f'datasets/asap_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


def run():
    response = requests.get('https://github.com/fosfrancesco/asap-dataset/archive/refs/heads/master.zip')
    zip_file = 'asap.zip'
    open(zip_file, "wb").write(response.content)
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('./')
    except zipfile.BadZipfile:
        print('invalid link')

    if not os.path.exists('./tmp'):
        os.mkdir('./tmp')

    if not os.path.exists('./datasets'):
        os.mkdir('./datasets')
    # Get a list of performances such as there are not 2 performances of the same piece
    df = pd.read_csv(Path(BASE_PATH, "metadata.csv"))
    unique_df = df.drop_duplicates(subset=["title", "composer"])
    unique_midi_list = unique_df["midi_score"].tolist()
    unique_xml_list = unique_df["xml_score"].tolist()
    tokenize(unique_midi_list, unique_xml_list)


if __name__ == "__main__":
    run()

