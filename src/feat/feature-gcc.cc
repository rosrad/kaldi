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
    int32 wlen = mic_.wlen;
    win_.Resize(wlen);
	for(int i=0; i<wlen; i++)
		win_(i) = sin((0.5+i)/wlen*M_PI);
    
    srfft_ = new SplitRadixRealFft<BaseFloat>(wlen);
}

PhatGCC::PhatGCC(const PhatGCC &other):
        srfft_(NULL), mic_(other.mic_) {
    if (other.srfft_)
        srfft_ = new SplitRadixRealFft<BaseFloat>(*(other.srfft_));
    else
        srfft_ = new SplitRadixRealFft<BaseFloat>(other.mic_.wlen);
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
void XX_real(const VectorBase<BaseFloat>& e, const VectorBase<BaseFloat>& x,
             VectorBase<BaseFloat>& d)
{
    // e.dim * 2  == x.dim
    KALDI_ASSERT(e.Dim() == x.Dim() && e.Dim() == 2* d.Dim());
    int32 j;
	for(int32 i=0; i<d.Dim(); i++)
	{  // real*real - imag*imag
        j = 2*i;
        d(i) = e(j)*x(j) - e(j+1)*x(j+1);
	}
}
void SubBand(const VectorBase<BaseFloat>& x,
             VectorBase<BaseFloat>& y) {
    int32 width = x.Dim()/y.Dim();
    for( int32 i=0; i < y.Dim(); i++) {
        y(i) = x.Range(i*width, width).Sum();
    }
}

void PhatGCC::Compute(const MatrixBase<BaseFloat>&  wav,
                      Matrix<BaseFloat>& feature) {
    // extract window
    int32 wlen= mic_.wlen;
    int32 nbin = wlen/2;
    int32 nsub = sqrt(nbin);
    int32 nsample = wav.NumCols();
    int32 nchan = wav.NumRows();
    int32 nshift = wlen/2;
    int32 nfrm = (nsample-wlen)/nshift + 1;
    int32 ntheta = mic_.ntheta;
    PairVec& pairs = mic_.Pairs();
    int32 npair = pairs.size();
    
    Matrix<BaseFloat> x;

    Vector<BaseFloat> P(nbin*2);
    // Vector<BaseFloat> F(ntheta);
    Vector<BaseFloat> real_CC(nsub*ntheta);
    feature.Resize(nfrm,ntheta*nsub);
    
    for (int32 i = 0; i < nfrm; i++) {
        x = wav.ColRange(i*nshift,wlen);
        x.MulColsVec(win_);  // x = x.*w
        for (int32 j = 0; j < nchan; j++) {
            srfft_->Compute(x.RowData(j), true);
        }
        

        for (int32 k = 0; k < npair; k++ ) {
            int32 id0 = pairs[k].first;
            int32 id1 = pairs[k].second;
            
            Matrix<BaseFloat> exp(mic_.Exp(k));
            spec_XXt(x.Row(id0), x.Row(id1), P);
            norm_X(P);
            for (int32 r=0; r < exp.NumRows(); r++) {
                Vector<BaseFloat> row(nbin);
                XX_real(exp.Row(r), P, row);
                SubVector<BaseFloat> sub_row(real_CC, r*nsub, nsub);
                SubBand(row,sub_row);
            }
            feature.Row(i).AddVec(1,real_CC);
        }
        
    }
}


}  // namespace kaldi
