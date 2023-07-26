{
  TChain *TT = new TChain("g11kp");

	TT->Add("/work/halld/home/viducic/forMoskov/g11_pipi_kplus.root");

  gStyle->SetPalette(1);


  TCanvas *c1 = new TCanvas("c1","",500,500);

 
  gStyle->SetOptStat(111111111);
  gStyle->SetLineWidth(2.);
  gStyle->SetTextSize(1.1);
  gStyle->SetLabelSize(0.06,"xy");
  gStyle->SetTitleSize(0.06,"xy");
  gStyle->SetTitleOffset(1.2,"x");
  gStyle->SetTitleOffset(1.0,"y");
  gStyle->SetPadTopMargin(0.1);
  gStyle->SetPadRightMargin(0.1);
  gStyle->SetPadBottomMargin(0.16);
  gStyle->SetPadLeftMargin(0.12);

  c1->Clear();

 

  

  //         TT->Draw("mk0>>h99(100, 0.47, 0.52)","coll>0.97&&dist>3&& doca<0.75&& gamma< 4.0 ", "e");

  //        TT->Draw("mk0>>h99(100, 0.47, 0.52)","coll>0.97&&dist>3&& doca<0.75&& gamma< 4.0 ", "e");
 

  //      TT->Draw("mxk0kp>>h99(100, 0.5, 1.5)","coll>0.97&&dist>3&& doca<0.75 && mk0>0.485 && mk0<0.505&&gamma< 4.0 ", "e");


     c1->Divide(1,2);
  c1->cd(1);


     TT->Draw("mxkp>>h99(1000, 1.4, 2.4)","mxk0kp>0.9 && mxk0kp<0.96 && coll>0.97&&dist>3&& doca<0.75 && mk0>0.48 && mk0<0.51 ", "e");
     c1->Update();

    c1->cd(2);

        TT->Draw("mxk0>>h98 (50, 1.4, 2.4)","mxk0kp>0.9 && mxk0kp<0.96 && coll>0.97&&dist>1&& doca<0.75 && mk0>0.48 && mk0<0.51&&mxkp<1.5 ", "e");
      c1->Update();
c1->SaveAs("mgg.png");
	 
	       return;

	
}