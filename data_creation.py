# from midi_manager import MidiLoader
import pickle

from midi_manager import sequence_melody_vector_2_DB12_melody_vector_with_time, sequence_melody_vector_2_interval_melody_vector_with_time
import argparse

parser = argparse.ArgumentParser(
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--data_dir', type=str, default='~/datasets/validation/midi',
                    help='data directory containing pickle')
parser.add_argument('--base_name', type=str, default='validation',
                    help='subset of the dataset')
args = parser.parse_args()


files_count_dict = {'train': 9552, 'evaluation': 3980, 'validation': 2400}

# base_name = 'train'
# files_count = 9552

# base_name = 'evaluation'
# files_count = 3980

# base_name = 'validation'
# files_count = 2400

files_count= files_count_dict[args.base_name]
base_name = args.base_name
source_dir = args.data_dir
output_dir = args.data_dir

MIN_SONG_SIZE = 12


# -------------------------------------------
# 				Song lists
# -------------------------------------------
tensor = pickle.load(open(source_dir + base_name + '_song_list.p', "rb"))

print 'length of array, should be the number of midis in folder, in my case ' + str(files_count) + ':'
assert len(tensor) == files_count

print 'cleaning original pickle'
# keep only songs with at least 12 notes, since these are the one considered in evaluation
clean_tensor = filter(lambda a: len(a) >= MIN_SONG_SIZE, tensor)

# clean durations greater than 16, I discover that max duration was 35791394
# import pdb; pdb.set_trace()
new_array = []
count_longer_songs = 0
for song in clean_tensor:
    flag = True
    for elem in song:
        if elem[1] > 16 or elem[1] == 0:
            flag = False
    if flag:
        new_array.append(song)
    else:
        count_longer_songs += 1

clean_tensor = new_array
# [song for song in clean_tensor if elem[1] < 16 for element in song]
#assert min len of a song is 12 and max duration of note is 16
assert min([len(elem) for elem in clean_tensor]) == 12
assert not False in [elem[1] <= 16 for song in clean_tensor for elem in song]

assert min([elem[1] for song in clean_tensor for elem in song]) == 1
assert max([elem[1] for song in clean_tensor for elem in song]) == 16

# test the size of clean tensor
count_false_songs=0
for seq in tensor:
    if len(seq) < MIN_SONG_SIZE:
        count_false_songs+=1

print 'this sould be the same'
assert len(tensor) - count_false_songs - count_longer_songs == len(clean_tensor)
# save cleaned pickle
pickle.dump(clean_tensor, open(output_dir + base_name + '_song_list_cleaned.p','wb'))

"""
(Pdb) min([elem[1] for song in clean_tensor for elem in song])
1
(Pdb) max([elem[1] for song in clean_tensor for elem in song])
16
(Pdb) min([elem[0] for song in clean_tensor for elem in song])
14
(Pdb) max([elem[0] for song in clean_tensor for elem in song])
127
(Pdb) len(clean_tensor)
4874
"""


# DB12 version

clean_tensor = pickle.load(open(output_dir + base_name + '_song_list_cleaned.p', "rb"))

print ''
print 'creating DB12 version'

tensor_DB12 = []

for seq in clean_tensor:
        tensor_DB12 += (sequence_melody_vector_2_DB12_melody_vector_with_time(seq))

print 'size of DB12'
print len(tensor_DB12)
print 'len(tensor_DB12)/ len(clean_tensor) should be 12'
assert float(len(tensor_DB12))/ len(clean_tensor) == 12.0
print float(len(tensor_DB12))/ len(clean_tensor)

# assert the range of the notes in each chuck of 12 sequences is the right one
i = 0
while i < len(tensor_DB12):
    test_chunk = [elem[0][0] for elem in tensor_DB12[i:i+12]]
    assert max(test_chunk) - min(test_chunk) == 11
    i+=12

pickle.dump(tensor_DB12, open(output_dir + base_name + '_song_list_db12_cleaned.p','wb'))
#
#
# Interval version

clean_tensor = pickle.load(open(output_dir + base_name + '_song_list_cleaned.p', "rb"))


print ''
print 'creating interval version'
tensor_intervals = []
for seq in clean_tensor:
    tensor_intervals.append(sequence_melody_vector_2_interval_melody_vector_with_time(seq))

# there is always one interval less than notes

count = 0
for i in range(len(tensor_intervals)):
	count += len(clean_tensor[i]) - len(tensor_intervals[i])

print 'there shouldnt be sequences with only one element'
assert len(filter(lambda a: len(a) == 1, tensor_intervals)) == 0

print 'this should be the same'
assert count == len(tensor_intervals)
assert count == len(clean_tensor)
assert len(clean_tensor) == len(tensor_intervals)

pickle.dump(tensor_intervals, open(output_dir + base_name + '_song_list_intervals_cleaned.p','wb'))


#-------------------------------------------
# 				Final Data
#-------------------------------------------

# print 'creating final sequence database'
# clean_tensor = pickle.load(open(output_dir + base_name + '_song_list_cleaned.p', "rb"))
# definitive_data = loader.create_dict_x_y_from_list(clean_tensor)
#
#
# print 'This should be the same'
# # the -1 is cause the slide in every song for every x and y
# print sum([len(a)-1 for a in clean_tensor])
# print len(definitive_data['x'])
# print len(definitive_data['y'])
#
# pickle.dump(definitive_data, open(output_dir + base_name + '_final_cleaned.p','wb'))
#
#
# print 'creating final interval database'
# clean_tensor = pickle.load(open(output_dir + base_name + '_song_list_intervals_cleaned.p', "rb"))
# definitive_data = loader.create_dict_x_y_from_list(clean_tensor)
#
#
# print 'This should be the same'
# # the -1 is cause the slide in every song for every x and y
# print sum([len(a)-1 for a in clean_tensor])
# print len(definitive_data['x'])
# print len(definitive_data['y'])
#
# pickle.dump(definitive_data, open(output_dir + base_name + '_intervals_final_cleaned.p','wb'))
#
# print 'creating final DB12 database'
# clean_tensor = pickle.load(open(output_dir + base_name + '_song_list_DB12_cleaned.p', "rb"))
# definitive_data = loader.create_dict_x_y_from_list(clean_tensor)
#
#
# print 'This should be the same'
# # the -1 is cause the slide in every song for every x and y
# print sum([len(a)-1 for a in clean_tensor])
# print len(definitive_data['x'])
# print len(definitive_data['y'])
#
# pickle.dump(definitive_data, open(output_dir + base_name + '_DB12_final_cleaned.p','wb'))
