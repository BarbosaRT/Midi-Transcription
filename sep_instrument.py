import os
from music21 import *
import shutil


def copy_file(source_path, destination_path):
    try:
        shutil.copy(source_path, destination_path)
        print(f"File copied successfully from {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error copying file: {e}")


def infer_clef_from_pitches(part):
    # Check the pitch range to infer clef

    pitch_ranges = [p.midi for p in part.pitches]

    if pitch_ranges:
        # Create a temporary stream with the same pitches to find the best clef
        temp_stream = stream.Stream()
        for pitch in pitch_ranges:
            n = note.Note()
            n.pitch.midi = pitch
            temp_stream.insert(n)

        # Use bestClef to get the best-matching clef for the pitch range
        best_clef = clef.bestClef(temp_stream)

        if best_clef.sign == 'G':
            return 'treble'
        elif best_clef.sign == 'F':
            return 'bass'

    return None


def sep_instuments():
    input_folder = 'mscorelib'
    output_folder = 'mscorelib_piano'
    os.makedirs(output_folder, exist_ok=True)

    for root, dirs, files in os.walk(input_folder):
        l_f = len(files)
        n = 0
        for file in files:
            if file.endswith(".mxl"):
                n += 2
                print(f'{n} / {l_f}: {file}')
                mxl_path = os.path.join(root, file)
                mxl_new_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.mxl")

                if os.path.exists(mxl_new_path):
                    continue

                music_stream = converter.parse(mxl_path)
                treble_clef_found = False
                bass_clef_found = False

                for part in music_stream.parts:
                    inference = infer_clef_from_pitches(part)
                    if inference == 'treble':
                        treble_clef_found = True
                    elif inference == 'bass':
                        bass_clef_found = True
                    if bass_clef_found and treble_clef_found:
                        break

                if bass_clef_found and treble_clef_found:
                    mid_path = os.path.join(root, f"{os.path.splitext(file)[0]}.mid")
                    mid_new_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.mid")

                    copy_file(mid_path, mid_new_path)
                    copy_file(mxl_path, mxl_new_path)

