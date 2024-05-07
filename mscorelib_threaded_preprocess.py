import os
from music21 import converter, metadata, stream
from concurrent.futures import ThreadPoolExecutor

total_num_of_bars = 0


def convert_and_save_instrument(mxl_path, output_folder, instrument_name):
    global total_num_of_bars
    output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(mxl_path))[0]}{instrument_name}.mxl")

    if os.path.exists(output_file):
        new_stream = converter.parse(output_file)
        total_num_of_bars += len(new_stream.parts[0])
        print(f"Instrument '{instrument_name}': Loaded from {output_file}")
        return

    try:
        # Parse the input musicXML file
        music_stream = converter.parse(mxl_path)

        # Filter parts based on the instrument name
        parts_to_combine = [part for part in music_stream.parts if part.partName == instrument_name]

        new_stream = stream.Score()
        new_stream.metadata = metadata.Metadata()
        new_stream.metadata.title = f"{instrument_name}_part"

        # Combine parts with the same instrument name
        for part in parts_to_combine:
            new_stream.append(part)

        total_num_of_bars += len(new_stream.parts[0])

        # Generate output paths
        mid_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(mxl_path))[0]}{instrument_name}.mid")

        new_stream.write('musicxml', fp=output_file)
        new_stream.write('midi', fp=mid_path)

        print(f"Instrument '{instrument_name}': Saved to {output_file}")
    except Exception as e:
        print(f'Error in {mxl_path}_{instrument_name}, exception: {e}')


def convert_mxl_to_mid():
    input_folder = 'cmidi'
    output_folder = 'mscorelib'
    global total_num_of_bars
    os.makedirs(output_folder, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        futures = []

        for root, dirs, files in os.walk(input_folder):
            l_f = len(files)
            n = 0
            for file in files:
                n += 1
                print(f'Progress: {n}/{l_f}')
                if file.endswith(".mxl"):
                    mxl_path = os.path.join(root, file)

                    # Parse the input musicXML file
                    music_stream = converter.parse(mxl_path)

                    # Get a list of unique instrument names
                    instrument_names = set(
                        part.partName or f'instrument_{i + 1}' for i, part in enumerate(music_stream.parts) if
                        not part.getInstrument().inGMPercMap)

                    # Submit tasks for each instrument
                    for instrument_name in instrument_names:
                        future = executor.submit(convert_and_save_instrument, mxl_path, output_folder, instrument_name)
                        futures.append(future)

        # Wait for all tasks to complete
        for future in futures:
            future.result()

    print(f'Total Number of Bars in mscorelib: {total_num_of_bars}')
