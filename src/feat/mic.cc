// feat/mic.cc


#include "feat/mic.h"

namespace kaldi {

Mic::Mic(std::vector<Pos> pos, int32 wlen, int32 fs)
        :wlen(wlen), fs(fs) {
    res_=5;
    c_ = 340;
    pos_ = pos;
    ntheta = 360/res_;
}

PairVec& Mic::Pairs() {
    return pair_;
}

const Matrix<BaseFloat>& Mic::Exp(int32 pair_id) {
    return exp_[pair_id];
}
BaseFloat Distance(const Pos& a) {
    return sqrt(a.x*a.x+a.y*a.y);
}


Pos VecPos(const Pos& a, const Pos& b) {
    return Pos(a.x-b.x,a.y-b.y);
}


void Mic::Init(){
    // init theta grid
    Vector<BaseFloat> theta_grid(ntheta);
    for( int32 i=0; i < ntheta; i++)
        theta_grid(i)=i*res_;

    // init frequency grid
    int32 nbin = wlen/2;
    Vector<BaseFloat> f_grid(nbin);
    for( int32 i=1; i <= nbin; i++)
        f_grid(i-1)=fs/wlen*i;

    // init microphone pairs
    int32 nmic = pos_.size();
    for( int32 i=0; i < nmic; i++ )
        for( int32 j=i+1; j< nmic; j++)
            pair_.push_back(std::make_pair(i,j));


    int32 npair = pair_.size();
    BaseFloat dmic;
    BaseFloat tau;
    BaseFloat mic_theta;



    Matrix<BaseFloat> exp_i(ntheta, nbin);

    Vector<BaseFloat> alpha_i(ntheta);
    for( int32 i=0; i < npair; i++) {
        int32 id0 = pair_[i].first;
        int32 id1 = pair_[i].second;
        // init micphone pair vector pos relative to origin
        Pos p = VecPos(pos_[id0], pos_[id1]);
        // init microphone distances
        dmic = Distance(p);
        distance_.push_back(dmic);
        mic_theta=atan2(p.y, p.x)/M_PI*180;

        exp_i.SetZero();
        for (int32 j=0; j< ntheta; j++) {
            tau = dmic * cos( (theta_grid(j)-mic_theta)*M_PI/180 ) / c_;
            exp_i.Row(j).CopyFromVec(f_grid);
            exp_i.Row(j).Scale(tau*2*M_PI);
        }
        exp_.push_back(exp_i);
    }
    
}


}  // namespace kaldi












