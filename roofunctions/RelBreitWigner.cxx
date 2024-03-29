/***************************************************************************** 
 * Project: RooFit                                                           * 
 *                                                                           * 
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/ 

// Your description goes here... 

#include "Riostream.h" 

#include "RelBreitWigner.h" 
#include "RooAbsReal.h" 
#include "RooAbsCategory.h" 
#include <math.h> 
#include "TMath.h" 

ClassImp(RelBreitWigner); 

 RelBreitWigner::RelBreitWigner(const char *name, const char *title, 
                        RooAbsReal& _x,
                        RooAbsReal& _mean,
                        RooAbsReal& _width) :
   RooAbsPdf(name,title), 
   x("x","x",this,_x),
   mean("mean","mean",this,_mean),
   width("width","width",this,_width)
 { 
 } 


 RelBreitWigner::RelBreitWigner(const RelBreitWigner& other, const char* name) :  
   RooAbsPdf(other,name), 
   x("x",this,other.x),
   mean("mean",this,other.mean),
   width("width",this,other.width)
 { 
 } 



 Double_t RelBreitWigner::evaluate() const 
 { 
   // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 
  double kaon = 0.49367;
  double proton = 0.93827;
  double pion = 0.13957;
  double k_short = 0.49761;

  double intermediateParticle = kaon + pion;

  Double_t q0 = breakupMomentum(mean*mean, intermediateParticle, k_short);
  Double_t q = breakupMomentum(x*x, intermediateParticle, k_short);

  int spin = 0;

  double gamma = width * mean / x * q/q0 * (barrierFactor(spin, q) / barrierFactor(spin, q0)) * (barrierFactor(spin, q) / barrierFactor(spin, q0));
  
  double arg1 = 14.0/22.0;
  double arg2 = mean * mean * gamma * gamma;
  double arg3 = (x*x - mean*mean) * (x*x - mean*mean);
  double arg4 = x*x*x*x*((gamma*gamma)/(mean*mean));
  return arg1 * arg2 / (arg3 + arg4); 
 } 

 Double_t RelBreitWigner::breakupMomentum(double s, double m1, double m2) const
{
  if(s < (m1+m2)*(m1+m2)){
    return 0.0;
  }
  else{
    double result = 0.5 * sqrt((s - (m1-m2)*(m1-m2)) * (s - (m1+m2)*(m1+m2)) / s);
    return result;
  }
}

Int_t RelBreitWigner::barrierFactor(int L, double p) const{
  double hbarc = hbarc = 0.1973269631; //GeV*fm
  double z = (p/hbarc)*(p/hbarc);
  double barrier;

  switch(L){
    case 0:
      barrier = 1;
      break;
    case 1:
      barrier = sqrt(2 * z / (z + 1)); 
      break;
    case 2:
      barrier = sqrt(13 * z * z/ ((z-3)*(z-3) + 9*z));
      break;
    default:
      barrier = 0;
  }

  return barrier;
}



