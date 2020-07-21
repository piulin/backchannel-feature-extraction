
import librosa
import numpy as np
import os
import subprocess
from reader.dataset import backchannel
from tqdm import tqdm

import librosa.display


def librosa_extract ( x, sr ):


    mfcc = librosa.feature.mfcc(x, sr=sr, n_mfcc=13, hop_length=int(0.010*sr), n_fft=int(0.025*sr))
    mfcc_delta = librosa.feature.delta( mfcc )
    mfcc_delta_delta = librosa.feature.delta(mfcc,order=2)

    return [mfcc,mfcc_delta,mfcc_delta_delta]

def extract (file_path,mfcc_arr,mfcc_delta_arr,mfcc_delta_delta_arr,offset,duration):

    x, sr = librosa.load(file_path, offset=offset, duration=duration, mono=True)

    mfcc, mfcc_delta, mfcc_delta_delta = librosa_extract(x, sr)

    mfcc_arr.append(mfcc)
    mfcc_delta_arr.append(mfcc_delta)
    mfcc_delta_delta_arr.append(mfcc_delta_delta)

def write_librosa_mfcc_from_dataset(out_folder, dataset, annotation, spks, offset):

    mfcc_arr = []
    mfcc_delta_arr = []
    mfcc_delta_delta_arr = []

    speakers = []
    listeners = []

    extracted = 0
    broken = 0
    exist = 0
    for file_path in tqdm(dataset):
        filename = os.path.basename(file_path).split('.')[0]
        tqdm.write('Processing file: ' + filename,end='' )
        if filename in annotation:
            annotation[filename].insert(0,backchannel('foo','0','0','foo'))
            for i,bc in enumerate(annotation[ filename ][1:],0):


                try:

                    speaker_name = f"{filename}-{bc.speaker}"
                    listener_letter = "A" if bc.speaker == "B" else "B"
                    listener_name = f"{filename}-{listener_letter}"
                    fake_idx_spk = spks.fake_idxs [ speaker_name ]
                    fake_idx_ls = spks.fake_idxs [ listener_name ]


                    extract(file_path, mfcc_arr, mfcc_delta_arr, mfcc_delta_delta_arr, bc.start, offset)
                    speakers.append(fake_idx_spk)
                    listeners.append(fake_idx_ls)

                    extracted += 1
                    tqdm.write('+', end='')

                except Exception as e:
                    tqdm.write('*', end='')
                    broken += 1
                    break
            del annotation[filename][0]
            tqdm.write('')
        else:
            tqdm.write('?')
            exist += 1
    print(f"extracted {extracted}")
    print(f"broken: {broken}")
    print(f"do not exist: {exist}")

    mfcc = np.array(mfcc_arr)
    dmfcc = np.array(mfcc_delta_arr)
    ddmfcc = np.array(mfcc_delta_delta_arr)


    e = np.expand_dims(mfcc, axis=1)
    e1 = np.expand_dims(dmfcc, axis=1)
    e2 = np.expand_dims(ddmfcc, axis=1)

    all_mfcc = np.concatenate((np.concatenate((e,e1),axis=1),e2),axis=1)

    np.save(out_folder + "data.mfcc",mfcc)
    np.save(out_folder + 'data.3dmfcc',all_mfcc)

    npspeakers = np.array(speakers)
    nplisteners = np.array(listeners)

    np.save(out_folder + "speakers", npspeakers)
    np.save(out_folder + 'listeners', nplisteners)


#this function was never tested.
def write_opensmile_mfcc_from_dataset(out_folder, dataset, annotation, offset, opensmile_config):
    for file_path in dataset:
        filename = os.path.basename(file_path).split('.')[0]
        print('Processing file: ' + filename,end='',flush=True )
        for bc in annotation[ filename ]:

            output = out_folder + filename + '-' + bc.speaker + '-' + str(offset) +'_' + "{:.2f}".format(bc.start)
            command = f"SMILExtract -C {opensmile_config} -start {bc.start-offset} -end {bc.start} -I {file_path} -O {output}"
            stdout = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

            print('.',end='',flush=True)
        print('')