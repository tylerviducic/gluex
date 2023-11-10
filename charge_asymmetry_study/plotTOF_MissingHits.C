void plotTOF_MissingHits(int period = 0, TString path = "/cache/halld/gluex_simulations/REQUESTED_MC/phi2pi_17_20230221025001pm/root/monitoring_hists/") {
	gStyle->SetOptStat(0);
	
	int minRunPeriod[3] = {30274, 40857, 50685};
	int maxRunPeriod[3] = {31057, 42559, 51768};
	TString periodName[3] = {"2017_01","2018_01","2018_08"};

	int minRun = minRunPeriod[period]; 
	int maxRun = maxRunPeriod[period];
	TH1F *hTOFPointsVsRun = new TH1F("hTOFPointsVsRun","hTOFPointsVsRun", maxRun-minRun+1, minRun-0.5, maxRun+0.5);
	TH1F *hTOFHitsVsRun = new TH1F("hTOFHitsVsRun","hTOFHitsVsRun", maxRun-minRun+1, minRun-0.5, maxRun+0.5);

	for(int irun=minRun; irun<=maxRun; irun++) {

		//TODO FIGURE OUT WHY HIST IS MISSING

		// replace with the filename specific to your generator
		TString fileName = Form("%s/hd_root_gen_amp_0%d.root", path.Data(), irun);
		TFile *f = TFile::Open(fileName);
		if(f == NULL) continue;

		TH1F *hTOFPoints = (TH1F*)f->Get("/Independent/Hist_NumReconstructedObjects/NumTOFPoints");
		TH1F *hTOFHits = (TH1F*)f->Get("/Independent/Hist_NumReconstructedObjects/NumTOFHits");
		double nTOFPoints = hTOFPoints->GetMean();
		double nTOFHits = hTOFHits->GetMean();

		hTOFPointsVsRun->SetBinContent(hTOFHitsVsRun->GetXaxis()->FindBin(irun), nTOFPoints);
		hTOFHitsVsRun->SetBinContent(hTOFHitsVsRun->GetXaxis()->FindBin(irun), nTOFHits);
	}

	TCanvas *aa = new TCanvas("aa","aa",600,400);
	hTOFPointsVsRun->SetMarkerStyle(20);
	hTOFPointsVsRun->Draw("p");

	TCanvas *bb = new TCanvas("bb","bb",600,400);
	hTOFHitsVsRun->SetMarkerStyle(20);
	hTOFHitsVsRun->Draw("p");

	aa->Print(Form("toffPointsVsRun_%s.png",periodName[period].Data()));
	bb->Print(Form("toffHitsVsRun_%s.png",periodName[period].Data()));
}

