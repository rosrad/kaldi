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

PhatGCC::PhatGCC(Mic& mic):
        srfft_(NULL) , mic_(mic){
    // compute window 
    int32 wlen_ = mic_.wlen;
    win_.Resize(wlen_);
	for(int i=0; i<wlen_; i++)
		win_(i) = sin((0.5+i)/wlen_*M_PI);
    
    srfft_ = new SplitRadixRealFft<BaseFloat>(wlen_);
}

PhatGCC::PhatGCC(const PhatGCC &other):
        srfft_(NULL), mic_(other.mic_) {
    if (other.srfft_)
        srfft_ = new SplitRadixRealFft<BaseFloat>(*(other.srfft_));
    else
        srfft_ = new SplitRadixRealFft<BaseFloat>(other.wlen_);
    win_ = other.win_;
    // for(int i = 0; i < opts_.NumPair(); i++) {
    //     pairs_[i] = other.pairs_[i];
    // }
}

PhatGCC::~PhatGCC() {
    if (srfft_) 
        delete srfft_;
}



void spec_XXt(const SubVector<BaseFloat> &x1, const SubVector<BaseFloat>& x2, VectorBase<BaseFloat>& d)
{
	for(int32 j=0; j<x1.Dim(); j+=2)
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

// special purpose for  real( mag .* x);
void Exp_XX_sum(VectorBase<BaseFloat>& e, const VectorBase<BaseFloat>& x)
{
    // e.dim * 2  == x.dim
	for(int32 i=0; i<e.Dim(); i++)
	{  // real*real - imag*imag
        e(i) = cos(e(i))*x(2*i) - sin(e(i))*x(2*i+1);
	}
}


void PhatGCC::Compute(const MatrixBase<BaseFloat>&  wav,
                      Matrix<BaseFloat>& feature) {
    // extract window
    int32 nsample = wav.NumCols();
    int32 nchan = wav.NumRows();
    int32 nshift = wlen_/2;
    int32 nfrm = (nsample-wlen_)/nshift + 1;
    int32 ntheta = mic_.ntheta;
    PairVec& pairs = mic_.Pairs();
    int32 npair = pairs.size();
    
    Matrix<BaseFloat> x;

    int32 minbin=25;
    int32 nbin = 200-25;
    Vector<BaseFloat> P(nbin*2);
    Vector<BaseFloat> F(nbin);
    feature.Resize(nfrm,ntheta*npair);
    
    for (int32 i = 0; i < nfrm; i++) {
        x = wav.ColRange(i*nshift,wlen_);
        x.MulColsVec(win_);  // x = x.*w
        for (int32 j = 0; j < nchan; j++) {
            srfft_->Compute(x.RowData(j), true);
        }
        

        for (int32 k = 0; k < npair; k++ ) {
            int32 id0 = pairs[k].first;
            int32 id1 = pairs[k].second;
            
            Matrix<BaseFloat> exp(mic_.Exp(k).ColRange(minbin,nbin));

            spec_XXt(x.Row(id0).Range(minbin*2, nbin*2),
                     x.Row(id1).Range(minbin*2, nbin*2), P);
            norm_X(P);
            for (int32 r=0; r < exp.NumRows(); r++) {
                SubVector<BaseFloat> row(exp, r);
                Exp_XX_sum(row, P);
            }
            F.AddColSumMat(1, exp);
            feature.Row(i).Range(k*ntheta, ntheta).CopyFromVec(F);            
        }
    }
}


}  // namespace kaldi
