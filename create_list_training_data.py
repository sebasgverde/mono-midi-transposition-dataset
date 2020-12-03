
from midi_manager import midi2sequenceVectorWithTimeTuple
import os
import argparse

parser = argparse.ArgumentParser(
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--data_dir', type=str, default='~/datasets/validation/midi',
                    help='data directory containing songs')
parser.add_argument('--output_file', type=str, default='~/data/validation_song_list.p',
                    help='data directory containing songs')
args = parser.parse_args()

data_dir = args.data_dir
output_file = args.output_file

def midi_folder_2_list_of_sequences(data_dir):
    tensor = []
    for midifile in os.listdir(data_dir):
        # print midifile
        tensor.append(midi2sequenceVectorWithTimeTuple(data_dir+ '/' +midifile))

    return tensor

tensor = midi_folder_2_list_of_sequences(data_dir)

import pickle
pickle.dump(tensor,open(output_file, "wb"))