
from mfcc import mfcc
from reader import dataset
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='This program extracts MFCC/Delta MFCC features from wav files as well as '
                                                 'speakers and listeners ids.')

    parser.add_argument('wav_list', help='Contains the location for each of the audio files. The name of each file is used as an unique identifier of such file. '
                                         'File format: <wav_path>\\n ')
    parser.add_argument('bc_annotation',
                        help='Contains the timestamps to extract backchannel samples . '
                             'File format: <wav_id>-<speaker>\\t<start>\\t<end>\\t<transcription>\\n')

    parser.add_argument('no_bc_annotation',
                        help='Contains the timestamps to extract NON-backchannel samples. '
                             'File format: <wav_id>-<speaker>\\t<start>\\t<end>\\t<empty>\\n')

    parser.add_argument('speaker_annotation',
                        help='Relates each of the samples with the real speakers. '
                             'File format: <wav_id>-<speaker>\\t<speaker_id>\\n')

    parser.add_argument('backchannel_folder_output',
                        help='Save the extracted backchannel samples into the provided folder: the mfcc (data.mfcc.npy); delta, delta-delta mfcc (data.3dmfcc.npy); '
                             'as well as the speaker (speakers.npy) and listener (listeners.npy) ids.')
    parser.add_argument('non_backchannel_folder_output',
                        help='Save the extracted NON-backchannel samples into the provided folder: the mfcc (data.mfcc.npy); delta, delta-delta mfcc (data.3dmfcc.npy); '
                             'as well as the speaker (speakers.npy) and listener (listeners.npy) ids.')

    return parser.parse_args()

if __name__ == '__main__':


    args = parse_args()

    # create output folders if they don't exist.
    if not os.path.exists(args.backchannel_folder_output):
        os.makedirs(args.backchannel_folder_output)

    if not os.path.exists(args.non_backchannel_folder_output):
        os.makedirs(args.non_backchannel_folder_output)

    # get the paths to the audio files
    split = dataset.read_split( args.wav_list )

    # get the backchannel annotations.
    bc_annotation = dataset.read_time_annotation( args.bc_annotation )

    # get the non backchannel annotations
    no_bc_annotation = dataset.read_time_annotation( args.no_bc_annotation )

    # get the speaker ids.
    speaker = dataset.speakers( args.speaker_annotation )

    # extract mfcc features and speakers/listeners ids.
    mfcc.write_librosa_mfcc_from_dataset(args.backchannel_folder_output,split,bc_annotation, speaker, 2)
    mfcc.write_librosa_mfcc_from_dataset(args.non_backchannel_folder_output,split,no_bc_annotation, speaker, 2)
