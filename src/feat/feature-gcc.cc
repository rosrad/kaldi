// feat/feature-fbank.cc

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


#include "feat/feature-gcc.h"

namespace kaldi {

PhatGCC::PhatGCC(const PhatGCCOptions& opts):
        srfft_(NULL) , opts_(opts){
    // compute window 
	for(int i=0; i<opts_.wlen; i++)
		win_(i) = sin((0.5+i)/opts_.wlen*M_PI);

    // compute microphones pair;
    for(int i = 0; i<opts_.nmic; i++ )
        for (int j =i+1; i < opts_.nmic; j++)
            pairs_.push_back(std::make_pair(i,j));
    
}

PhatGCC::PhatGCC(const PhatGCC &other):
        srfft_(NULL), opts_(other.opts_) {
    if (other.srfft_)
        srfft_ = new SplitRadixRealFft<BaseFloat>(*(other.srfft_));

    win_ = other.win_;
    for(int i = 0; i < opts_.NumPair(); i++) {
        pairs_[i] = other.pairs_[i];
    }
}

PhatGCC::~PhatGCC() {
    if (srfft_) 
        delete srfft_;
}



void spec_XXt(const SubVector<BaseFloat> &x1, const SubVector<BaseFloat>& x2, Vector<BaseFloat> &d)
{
	int32 i, j;
    int32 ndim = x1.Dim();
	for(i=0,j=0; i<ndim; i++,j+=2)
	{
		d(j)   = x1(j)*x2(j)   + x1(j+1)*x2(j+1);
		d(j+1) = x1(j+1)*x2(j) - x1(j)  *x2(j+1);
	}
}

void norm_X(Vector<BaseFloat>& x)
{
	BaseFloat a;
	for(int32 j=0; j<x.Dim(); j+=2)
	{
		a = sqrt(x(j)*x(j) + x(j+1)*x(j+1));
		a = 1 / (a+DBL_EPSILON);
		x(j)   = x(j)   * a;
		x(j+1) = x(j+1) * a;
	}
}


void PhatGCC::Compute(const MatrixBase<BaseFloat>&  wav,
                      Matrix<BaseFloat>& feature) {
    // extract window
    int32 wlen = opts_.wlen;
    int32 nshift = wlen/2;
    int32 nchan = wav.NumCols();
    int32 nsample = wav.NumRows();
    int32 nfrm = (nsample-wlen)/nshift +1;

    Matrix<BaseFloat> x;
    Vector<BaseFloat> P;
    for (int32 i = 0; i < nfrm; i++) {
        x = wav.RowRange(i*wlen,wlen);
        x.MulColsVec(win_);  // x = x.*w
        for (int32 j = 0; j < nchan; j++) {
            // if (srfft_ != NULL)  // Compute FFT using split-radix algorithm.
            //     srfft_->Compute(x.RowData(j), true);
            // else  // An alternative algorithm that works for non-powers-of-two.
            //     RealFft(x.RowData(j), true);
        }

        for (int32 k = 0; k < pairs_.size(); k++ ) {
            int32 id0 = pairs_[k].first;
            int32 id1 = pairs_[k].second;
            spec_XXt(x.Row(id0),x.Row(id1),P);
            norm_X(P);
            feature.Row(i).Range(k, wlen/2).CopyFromVec(P);
        }
    }
}


}  // namespace kaldi
