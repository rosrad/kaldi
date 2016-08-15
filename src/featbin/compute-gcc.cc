// featbin/compute-fbank-feats.cc

// Copyright 2009-2012  Microsoft Corporation
//                      Johns Hopkins University (author: Daniel Povey)

// See ../../COPYING for clarification regarding multiple authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//  http://www.apache.org/licenses/LICENSE-2.0
//
// THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
// WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
// MERCHANTABLITY OR NON-INFRINGEMENT.
// See the Apache 2 License for the specific language governing permissions and
// limitations under the License.

#include "base/kaldi-common.h"
#include "util/common-utils.h"
#include "feat/mic.h"
#include "feat/feature-gcc.h"
#include "feat/wave-reader.h"



int main(int argc, char *argv[]) {
    try {
        using namespace kaldi;
        const char *usage =
                "Compute PHAT-GCC feature from multiple channels.\n"
                "Usage:  compute-gcc [options...] <wav-rspecifier> <feats-wspecifier>\n";


        ParseOptions po(usage);
        int32 wlen = 32;
        int32 fs = 16000;
        po.Register("wlen", &wlen, "window length");
        po.Register("fs", &fs, "sampling frequency");

        po.Read(argc, argv);

        if (po.NumArgs() != 2) {
            po.PrintUsage();
            exit(1);
        }

        std::string wav_rspecifier = po.GetArg(1);
        std::string output_wspecifier = po.GetArg(2);

        SequentialTableReader<WaveHolder> reader(wav_rspecifier);
        BaseFloatMatrixWriter kaldi_writer;  // typedef to TableWriter<something>.
        if (!kaldi_writer.Open(output_wspecifier)) {
            KALDI_ERR << "Could not initialize output with wspecifier "
                      << output_wspecifier;
        }  

        // array = [1,0;0,1;-1,0;0,-1]*d.';
        std::vector<Pos> mic_pos;
        BaseFloat r=0.035;
        mic_pos.push_back(Pos(r,0));
        mic_pos.push_back(Pos(0,r));
        mic_pos.push_back(Pos(-r,0));
        mic_pos.push_back(Pos(0,-r));
        Mic mic(mic_pos, wlen, fs);
        PhatGCC gcc(mic);
        int32 num_utts = 0, num_success = 0;
        for (; !reader.Done(); reader.Next()) {
            num_utts++;
            std::string utt = reader.Key();
            const WaveData &wave_data = reader.Value();
            Matrix<BaseFloat> feature;
            try {
                gcc.Compute(wave_data.Data(), feature);
            } catch (...) {
                KALDI_WARN << "Failed to compute features for utterance "
                           << utt;
                continue;
            }
            kaldi_writer.Write(utt, feature);
            if (num_utts % 10 == 0)
                KALDI_LOG << "Processed " << num_utts << " utterances";
            KALDI_VLOG(2) << "Processed features for key " << utt;
            num_success++;
        }
        KALDI_LOG << " Done " << num_success << " out of " << num_utts
                  << " utterances.";
        return (num_success != 0 ? 0 : 1);
    } catch(const std::exception &e) {
        std::cerr << e.what();
        return -1;
    }
    return 0;
}

