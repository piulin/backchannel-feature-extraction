


class speakers:

    def __init__( self, speakers_file ):

        self.fake_idxs = {}
        id_tracker = {}
        with open(speakers_file) as f:
            f.readline() # discard first line
            fake_id = 0
            for line in f:

                speaker_name, speaker_id = line.split('\t')  # keep only speakerID, since [0] is conv_chan
                speaker_id = speaker_id.strip('\n')

                if speaker_id not in id_tracker:
                    id_tracker [ speaker_id ] = fake_id
                    self.fake_idxs [ speaker_name] = fake_id
                    fake_id += 1
                else:
                    self.fake_idxs[speaker_name] = id_tracker [ speaker_id]

        self.no_speakers = len(self.fake_idxs)

class backchannel:

    def __init__(self,speaker,start,end,transcription):
        self.speaker = speaker
        self.start = float(start)
        self.end = float(end)
        self.transcription = transcription

    def __str__(self):
        return 'speaker: ' + self.speaker + ' start: ' + str(self.start) + ' end: ' + str(self.end) + ' backchannel: ' + self.bc


def read_split ( path ):
    with open(path) as f:
        alist = [line.rstrip() for line in f]
    return alist

def read_time_annotation ( path ):
    e = {}
    with open(path) as f:
        f.readline()
        for line in f:
            wav_rep, start, end, bc = line.split("\t")
            wav, speaker = wav_rep.split( "-" )
            if wav not in e:
                e[wav] = []
            b = backchannel(speaker,start,end,bc.rstrip())
            e [wav].append(b)
    return e
