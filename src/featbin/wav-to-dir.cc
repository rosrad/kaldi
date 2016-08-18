// featbin/wav-copy.cc

// Copyright 2013-2014  Daniel Povey

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
#include "feat/feature-mfcc.h"
#include "feat/wave-reader.h"

int main(int argc, char *argv[]) {
  try {
    using namespace kaldi;
    const char *usage =
        "Copy archives of wave to dir \n"
        "\n"
        "Usage:  wav-to-dir [options...] <wav-rspecifier> <wav-dir>\n"
        "e.g. wav-to-dir scp:wav.scp ./\n"
        "See also: wav-copy\n";

    ParseOptions po(usage);
    std::string ext="wav";
    po.Register("ext", &ext, "extension of wav files [wav]");

    std::string scp="";
    po.Register("scp", &scp, "wav.scp file path [dir/wav.scp]");

    po.Read(argc, argv);

    if (po.NumArgs() != 2) {
      po.PrintUsage();
      exit(1);
    }

    std::string wav_rspecifier = po.GetArg(1),
        dir = po.GetArg(2);

    int32 num_done = 0;
    
    SequentialTableReader<WaveHolder> wav_reader(wav_rspecifier);
    // TableWriter<WaveHolder> wav_writer(wav_wspecifier);
    // bool binary=true;
    std::vector<std::pair<std::string, std::string> > script;
    for (; !wav_reader.Done(); wav_reader.Next()) {
      // wav_writer.Write(wav_reader.Key(), wav_reader.Value());
      std::string wav_file = dir +"/"+wav_reader.Key()+"."+ext;
      // WriteKaldiObject(wav_reader.Value(), wav_file, binary);
      {
          Output ko(wav_file, true, false);
          wav_reader.Value().Write(ko.Stream());
      }
      
      script.push_back( std::make_pair(wav_reader.Key(), wav_file));
      num_done++;
    }
    std::string wav_scp = scp;
    if (wav_scp.empty()) {
        wav_scp=dir+"/"+ext+".scp";
    }
    WriteScriptFile(wav_scp, script);
    KALDI_LOG << "Copied " << num_done << " wave files";
    return (num_done != 0 ? 0 : 1);
  } catch(const std::exception &e) {
    std::cerr << e.what();
    return -1;
  }
}

