from tokens_to_score import tokens_to_score
from music21 import stream, metadata, bar, layout


def join_measures(score_list):
    # Create a new Stream to store the joined measures
    # combined_score = stream.Score()
    r = stream.PartStaff()
    l = stream.PartStaff()
    # Iterate through each score in the list
    m = 0
    for score in score_list:
        m += 1
        # score.show('text')
        right_measure = stream.Measure(number=m)
        right = score.parts[0][0]
        right_measure.mergeElements(right)

        left_measure = stream.Measure(number=m)
        left = score.parts[1][0]
        left_measure.mergeElements(left)

        r.append(right_measure)
        l.append(left_measure)

    s = stream.Score()
    # g = layout.StaffGroup([r, l], symbol='brace', barTogether=True)
    s.append([r, l])
    # return s
    return s


with open('./pred.txt', 'r', encoding='utf-8') as file:
    out = str(file.read()).strip().split('\n')

measures = []
n = 0
for m in out:
    n += 1
    try:
        measure = tokens_to_score(m)
        # measure.write('musicxml', f'songs/score_{n}')
        measures.append(measure)
    except Exception as e:
        print(f'Exception {e}')
        measure = tokens_to_score('R bar time_4/4 clef_treble L bar time_4/4 clef_treble')
        # measure.write('musicxml', f'songs/score_{n}')
        measures.append(measure)

music_stream = join_measures(measures)
music_stream.write('musicxml', 'output')
