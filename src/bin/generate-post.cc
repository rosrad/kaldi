// featbin/paste-feats.cc

// Copyright 2012 Korbinian Riedhammer
//           2013 Brno University of Technology (Author: Karel Vesely)
//           2013 Johns Hopkins University (Author: Daniel Povey)

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
#include "hmm/posterior.h"


int main(int argc, char *argv[]) {
    try {
        using namespace kaldi;
        using namespace std;

        const char *usage =
                "generate posteriors arks from feature and labels\n"
                "Usage: generate-post <feat-rspecifier> <label-rspecifier> [<post-wspecifier>\n"
                " e.g. generate-post ark:feats.ark ark:label.ark ark:post.ark \n";

        ParseOptions po(usage);

        bool binary = true;
        po.Register("binary", &binary, "If true, output files in binary "
                    "(only relevant for single-file operation, i.e. no tables)");

        po.Read(argc, argv);

        if (po.NumArgs() != 3) {
            po.PrintUsage();
            exit(1);
        }
        
        KALDI_ASSERT((ClassifyRspecifier(po.GetArg(1), NULL, NULL) == kNoRspecifier)
                     && "feature file should be tables, e.g. archives");

        string feat_rspecifier = po.GetArg(1);
        string label_rspecifier = po.GetArg(2);
        string post_wspecifier = po.GetArg(3);

        PosteriorWriter post_writer(post_wspecifier);

        SequentialBaseFloatMatrixReader feats_reader(feat_rspecifier);
        RandomAccessInt32Reader label_reader(label_rspecifier);

        int32 num_done = 0, num_err = 0;
        for (; !feats_reader.Done(); feats_reader.Next()) {
            string utt = feats_reader.Key();
            
            if (!label_reader.HasKey(utt)) {
                KALDI_WARN << "Missing utt " << utt << " from label "
                           << label_rspecifier;
                num_err++;
                break;
            }

            label_reader.Value(utt);
            const Matrix<BaseFloat> &mat = feats_reader.Value();
            int32 num_frames = mat.NumRows();

            // Posterior is vector<vector<pair<int32, BaseFloat> > >
            Posterior post(num_frames);
            // Fill posterior with matrix values,
            for (int32 f = 0; f < num_frames; f++) {
                post[f].push_back(std::make_pair(label_reader.Value(utt), 1));
            }
            // Store
            post_writer.Write(utt, post);
            num_done++;
        }
        KALDI_LOG << "Generated  " << num_done << " posteriors.";
        return (num_done != 0 ? 0 : 1);

    } catch(const std::exception &e) {
        std::cerr << e.what();
        return -1;
    }
}

