// feat/mic.h

// Copyright 2009-2012  Karel Vesely
//                2016  Johns Hopkins University (author: Daniel Povey)

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

#ifndef KALDI_FEAT_MIC_H_
#define KALDI_FEAT_MIC_H_

#include<map>
#include <string>
#include <vector>
#include <memory>

#include "feat/feature-common.h"
#include "feat/feature-functions.h"


namespace kaldi {

    struct Pos {
        BaseFloat x;
        BaseFloat y;
      Pos() :x(0),y(0){};
      Pos(BaseFloat xp, BaseFloat yp) :x(xp),y(yp){};
    };

    typedef std::vector<std::pair<int32,int32> > PairVec;
    /* typedef std::shared_ptr <Matrix<BaseFloat> > BaseFloatMatrixPtr; */
    /* typedef std::shared_ptr<Vector<BaseFloat> > BaseFloatVectorPtr; */

    struct Mic
    {

        Mic(std::vector<Pos> mic, int32 wlen, int32 fs);
        ~Mic() {};
        PairVec& Pairs();
        const Matrix<BaseFloat>& Exp(int32 pair_id);
        int32 ntheta;
        int32 wlen;
        int32 fs;
      private:
        void Init();
        std::vector<Pos> pos_;
        PairVec pair_;
        int32 res_;
        BaseFloat c_;  /* speech of sound in air */
        std::vector<BaseFloat> distance_;
        std::vector<Matrix<BaseFloat> > exp_;
    };
    
}  // namespace kaldi


#endif  // KALDI_FEAT_MIC_H_
