// feat/feature-gcc.h

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

#ifndef KALDI_FEAT_FEATURE_GCC_H_
#define KALDI_FEAT_FEATURE_GCC_H_

#include <map>
#include <string>
#include <memory>

#include "feat/mic.h"
#include "feat/feature-common.h"
#include "feat/feature-functions.h"
#include "feat/feature-window.h"


namespace kaldi {
    class PhatGCC {
  public:
        PhatGCC(Mic& mic);
        PhatGCC(const PhatGCC &other);
        /**
           Function that computes one frame of features from
           one frame of signal.
           @param [in] signal_frame  One frame of the signal,
           as extracted using the function ExtractWindow() using the options
           returned by this->GetFrameOptions().  The function will use the
           vector as a workspace, which is why it's a non-const pointer.
           @param [out] feature  Pointer to a vector of size this->Dim(), to which
           the computed feature will be written.
        */
        void Compute(const MatrixBase<BaseFloat>& wav, Matrix<BaseFloat>&  feature);
        int32 Dim() { return mic_.Pairs().size() * mic_.ntheta; }
        ~PhatGCC();

  private:
        SplitRadixRealFft<BaseFloat>* srfft_;
        Mic& mic_;
        int32 wlen_;
        /* typedef std::vector<std::pair<int32,int32> > PairVec; */
        /* PairVec pairs_; */
        Vector<BaseFloat> win_;

        PhatGCC &operator =(const PhatGCC &other);
    };

    /* typedef OfflineFeatureTpl<PhatGCC> Fbank; */

    /// @} End of "addtogroup feat"
}  // namespace kaldi


#endif  // KALDI_FEAT_FEATURE_GCC_H_
