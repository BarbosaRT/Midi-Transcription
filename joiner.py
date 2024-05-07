import os
import json

MAX_LEN = 4096


def combine_jsons(input_dir, output_file):
    combined_data = {}
    data = {}
    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".json") and filename != 'final_dataset.json':

            file_path = os.path.join(input_dir, filename)

            # Read the JSON data from each file
            with open(file_path, 'r') as file:
                data = json.load(file)
            data_filtered = data.copy()
            for _, k in enumerate(data):
                v = data[k]
                # Eliminates Midis that are null
                if len(v['midi']) > MAX_LEN or len(v['midi']) == 0:
                    data_filtered.pop(k)
                    continue
                if len(v['musicxml']) > MAX_LEN or v['musicxml'] == 'R bar time_4/4 clef_treble L bar time_4/4 clef_treble':
                    data_filtered.pop(k)
            # Merge the data into the combined_data dictionary
            combined_data.update(data_filtered)

    # Write the combined data to the output file
    with open(output_file, 'w') as output:
        json.dump(combined_data, output, indent=4)


def run():
    input_directory = './datasets'
    output_file = './datasets/final_dataset.json'

    combine_jsons(input_directory, output_file)


if __name__ == "__main__":
    run()
