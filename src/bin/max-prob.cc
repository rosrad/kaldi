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
                "select max-prob locations from prob files generated from DNN\n"
                "Usage: max-prob <prob-rspecifier> <loc-wspecifier>\n"
                " e.g. max-prob ark:prob.ark ark:utt2loc \n";
        ParseOptions po(usage);

        bool binary = false;
        bool log = false;
        po.Register("apply-log", &log, "apply log() before selection");

        po.Register("binary", &binary, "If true, output files in binary "
                    "(only relevant for single-file operation, i.e. no tables)");

        po.Read(argc, argv);

        if (po.NumArgs() != 2) {
            po.PrintUsage();
            exit(1);
        }
        
        string prob_rspecifier = po.GetArg(1);
        string loc_wspecifier = po.GetArg(2);
        SequentialBaseFloatMatrixReader prob_reader(prob_rspecifier);
        Int32VectorWriter loc_writer(loc_wspecifier);
        int32 num_done = 0;
        for (; !prob_reader.Done(); prob_reader.Next()) {
            string utt = prob_reader.Key();

            Matrix<BaseFloat> prob = prob_reader.Value();
            if (log) { prob.ApplyLog(); }

            std::vector<int32> loc;
            int32 max_ind = -1;
            Vector<BaseFloat> acc(prob.NumCols());
            acc.AddRowSumMat(1.0,prob);
            acc.Max(&max_ind);
            loc.push_back(max_ind);
            // Store
            loc_writer.Write(utt, loc);
            num_done++;
        }
        KALDI_LOG << "Have selected max prob for " << num_done << " utterances.";
        return (num_done != 0 ? 0 : 1);
    } catch(const std::exception &e) {
        std::cerr << e.what();
        return -1;
    }
}

