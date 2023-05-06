#include "DSelector_f1_pimkpks.h"

void DSelector_f1_pimkpks::Init(TTree *locTree)
{
	// USERS: IN THIS FUNCTION, ONLY MODIFY SECTIONS WITH A "USER" OR "EXAMPLE" LABEL. LEAVE THE REST ALONE.

	// The Init() function is called when the selector needs to initialize a new tree or chain.
	// Typically here the branch addresses and branch pointers of the tree will be set.
	// Init() will be called many times when running on PROOF (once per file to be processed).

	//USERS: SET OUTPUT FILE NAME //can be overriden by user in PROOF
	dOutputFileName = "f1_pimkpks.root"; //"" for none
	dOutputTreeFileName = ""; //"" for none
	dFlatTreeFileName = "flat_f1_pimkpks.root"; //output flat tree (one combo per tree entry), "" for none
	dFlatTreeName = ""; //if blank, default name will be chosen
	//dSaveDefaultFlatBranches = true; // False: don't save default branches, reduce disk footprint.

	//Because this function gets called for each TTree in the TChain, we must be careful:
		//We need to re-initialize the tree interface & branch wrappers, but don't want to recreate histograms
	bool locInitializedPriorFlag = dInitializedFlag; //save whether have been initialized previously
	DSelector::Init(locTree); //This must be called to initialize wrappers for each new TTree
	//gDirectory now points to the output file with name dOutputFileName (if any)
	if(locInitializedPriorFlag)
		return; //have already created histograms, etc. below: exit

	Get_ComboWrappers();
	dPreviousRunNumber = 0;

	/*********************************** EXAMPLE USER INITIALIZATION: ANALYSIS ACTIONS **********************************/

	// EXAMPLE: Create deque for histogramming particle masses:
	// // For histogramming the phi mass in phi -> K+ K-
	// // Be sure to change this and dAnalyzeCutActions to match reaction
	std::deque<Particle_t> MyPhi;
	MyPhi.push_back(KPlus); MyPhi.push_back(KMinus);

	//ANALYSIS ACTIONS: //Executed in order if added to dAnalysisActions
	//false/true below: use measured/kinfit data

	//PID
	dAnalysisActions.push_back(new DHistogramAction_ParticleID(dComboWrapper, false));
	//below: value: +/- N ns, Unknown: All PIDs, SYS_NULL: all timing systems
	//dAnalysisActions.push_back(new DCutAction_PIDDeltaT(dComboWrapper, false, 0.5, KPlus, SYS_BCAL));

	//PIDFOM (for charged tracks)
	dAnalysisActions.push_back(new DHistogramAction_PIDFOM(dComboWrapper));
	//dAnalysisActions.push_back(new DCutAction_PIDFOM(dComboWrapper, KPlus, 0.1));
	//dAnalysisActions.push_back(new DCutAction_EachPIDFOM(dComboWrapper, 0.1));

	//MASSES
	//dAnalysisActions.push_back(new DHistogramAction_InvariantMass(dComboWrapper, false, Lambda, 1000, 1.0, 1.2, "Lambda"));
	//dAnalysisActions.push_back(new DHistogramAction_MissingMassSquared(dComboWrapper, false, 1000, -0.1, 0.1));

	//KINFIT RESULTS
	dAnalysisActions.push_back(new DHistogramAction_KinFitResults(dComboWrapper));

	//CUT MISSING MASS
	//dAnalysisActions.push_back(new DCutAction_MissingMassSquared(dComboWrapper, false, -0.03, 0.02));

	//CUT ON SHOWER QUALITY
	//dAnalysisActions.push_back(new DCutAction_ShowerQuality(dComboWrapper, SYS_FCAL, 0.5));

	//BEAM ENERGY
	dAnalysisActions.push_back(new DHistogramAction_BeamEnergy(dComboWrapper, false));
	//dAnalysisActions.push_back(new DCutAction_BeamEnergy(dComboWrapper, false, 8.2, 8.8));  // Coherent peak for runs in the range 30000-59999

	//KINEMATICS
	dAnalysisActions.push_back(new DHistogramAction_ParticleComboKinematics(dComboWrapper, false));

	// ANALYZE CUT ACTIONS
	// // Change MyPhi to match reaction
	dAnalyzeCutActions = new DHistogramAction_AnalyzeCutActions( dAnalysisActions, dComboWrapper, false, 0, MyPhi, 1000, 0.9, 2.4, "CutActionEffect" );

	//INITIALIZE ACTIONS
	//If you create any actions that you want to run manually (i.e. don't add to dAnalysisActions), be sure to initialize them here as well
	Initialize_Actions();
	dAnalyzeCutActions->Initialize(); // manual action, must call Initialize()

	/******************************** EXAMPLE USER INITIALIZATION: STAND-ALONE HISTOGRAMS *******************************/

	//EXAMPLE MANUAL HISTOGRAMS:
	dHist_MissingMassSquared = new TH1F("MissingMassSquared", ";Missing Mass Squared (GeV/c^{2})^{2}", 600, -0.06, 0.06);
	dHist_BeamEnergy = new TH1F("BeamEnergy", ";Beam Energy (GeV)", 600, 0.0, 12.0);
	dHist_IM_PipPim2 = new TH1F("IM_PipPim", ";IM(pi+ pi-) GeV", 300, 0.3, 0.8);
	dHist_IM_KsKpPim = new TH1F("IM_KsKpPim", ";IM(Ks K+ Pi-) GeV", 150, 1, 2.25);
	dHist_IM_KsKpPim_1285 = new TH1F("IM_KsKpPim_1285", ";IM(Ks K+ Pi-) GeV", 150, 1, 2.25);
	dHist_IM_KsKpPim_1420 = new TH1F("IM_KsKpPim_1420", ";IM(Ks K+ Pi-) GeV", 150, 1, 2.25);
	dHist_IM_Pim1P = new TH1F("IM_Pim1P", ";IM(pi- p) GeV", 150, 0.5, 3.0);
	dHist_IM_PKp = new TH1F("IM_PKp", ";IM(K+ p) GeV", 100, 1.0, 2.5);
	dHist_IM_KsPim = new TH1F("IM_KsPim", ";IM(Ks pi-) GeV", 100, 0, 1.5);
	dHist_IM_KpPim = new TH1F("IM_KpPim", ";IM(K+ pi-) GeV", 100, 0, 1.5);
	dHist_IM_PKs = new TH1F("IM_PKs", ";IM(p Ks) GeV", 200, 1.4, 1.8);
	dHist_IM_KsKp = new TH1F("IM_KsKp", ";IM(Ks K+) GeV", 100, 0.0, 2.0);
	dHist_MinusT = new TH1F("MinusT", ";-t GeV^2", 100, 0, 10);
	dHist_TMin = new TH1F("TMin", "tmin GeV^2", 100, 0, 10);
	dHist_W = new TH1F("W", ";W (Gev)", 100, 3, 5);



	dHist_Ks_vs_FlightSig = new TH2F("Ks_vs_FlightSig", ";M(Ks) vs Flight Signifigance", 100, 0.3, 0.8, 100, 0, 10);
	dHist_Pim1P_vs_KsKpPim = new TH2F("Pim1P_vs_KsKpPim", ";IM(Ks K+ Pi-) vs IM(pi- p) GeV", 100, 1, 3.5, 70, 1.0, 2.5);
	dHist_KpP_KsKpPim = new TH2F("KpP_KsKpPim", ";IM(K+ p) vs IM(Ks K+ Pi-) GeV", 200, 0, 3.5, 100, 1.0, 2.5);
	dHist_DOCA_vs_IM_PipPim = new TH2F("DOCA_vs_IM_PipPim", ";DOCA vs IM(pi+ pi-)", 300, 0.3, 0.8, 100, 0, 20);
	dHist_DOCA_vs_IM_KsKpPim = new TH2F("DOCA_vs_IM_KsKpPim", ";DOCA vs IM(Ks K+ pi-)", 200, 0.0, 3.5, 100, 0, 20);
	dHist_CosTheta_vs_IM_PipPim = new TH2F("CosTheta_vs_IM_PipPim", ";CosTheta vs IM(pi+ pi-)", 300, 0.3, 0.8, 100, 0.9, 1.0);
	dHist_CosTheta_vs_IM_KsKpPim = new TH2F("CosTheta_vs_IM_KsKpPim", ";CosTheta vs IM(Ks K+ pi-)", 200, 0.0, 3.5, 100, 0.9, 1.0);
	dHist_W_vs_IM_KsKpPim = new TH2F("W_vs_IM_KsKpPip", "W vs IM(Ks K+ pi-)", 150, 1.0, 2.2, 100, 3, 5);
	dHist_KsPim_KpPim_Dalitz_1100_1350 = new TH2F("dHist_KsPim_KpPim_Dalitz_1100_1350", "M2 (Ks Pi-) vs M2 (K+ Pi-)", 100, 0, 2, 100, 0, 2);
	dHist_KsPim_KpPim_Dalitz_1350_1500 = new TH2F("dHist_KsPim_KpPim_Dalitz_1350_1500", "M2 (Ks Pi-) vs M2 (K+ Pi-)", 100, 0, 2, 100, 0, 2);
	dHist_KsPim_KpPim_Dalitz_1500 = new TH2F("dHist_KsPip_KpPip_Dalitz_1500", "M2 (Ks Pi-) vs M2 (K+ Pi-)", 100, 0, 2, 100, 0, 2);
	dHist_KsPim_vs_PimKpKs = new TH2F("dHist_KsPip_vs_PipKpKs", "M(KsPi-) vs M(K-KsPi-)", 50, 1.0, 1.7, 100, 0, 2);
	dHist_KsKp_vs_PimKpKs = new TH2F("dHist_KsKm_vs_PimKmKs", "M(KsK-) vs M(K+KsPi-)", 50, 1.0, 1.7, 100, 0, 2);
	dHist_KpPim_vs_PimKpKs = new TH2F("dHist_KpPim_vs_PimKpKs", "M(K+Pi-) vs M(K+KsPi-)", 50, 1.0, 1.7, 100, 0, 2);

	dHist_IM_KsKpPim_vs_t_70_75 = new TH2F("IM_KsKpPim_vs_t_70_75", "-t vs IM(Ks K+ pi-) for 7.0 < E(beam) < 7.5 GeV", 200, 1, 4.0, 100, 0, 5);
	dHist_IM_KsKpPim_vs_t_75_80 = new TH2F("IM_KsKpPim_vs_t_75_80", "-t vs IM(Ks K+ pi-) for 7.5 < E(beam) < 8.0 GeV", 200, 1, 4.0, 100, 0, 5);
	dHist_IM_KsKpPim_vs_t_80_85 = new TH2F("IM_KsKpPim_vs_t_80_85", "-t vs IM(Ks K+ pi-) for 8.0 < E(beam) < 8.5 GeV", 200, 1, 4.0, 100, 0, 5);
	dHist_IM_KsKpPim_vs_t_85_90 = new TH2F("IM_KsKpPim_vs_t_85_90", "-t vs IM(Ks K+ pi-) for 8.5 < E(beam) < 9.0 GeV", 200, 1, 4.0, 100, 0, 5);
	dHist_IM_KsKpPim_vs_t_82_88 = new TH2F("IM_KsKpPim_vs_t_82_88", "-t vs IM(Ks K+ pi-) for 8.2 < E(beam) < 8.8 GeV", 200, 1, 4.0, 100, 0, 5);

	for(int i = 0; i < 5; i++){ 
		double minus_t_higher = 0.2 * (i + 1);
		double minus_t_lower = 0.2 * i;

		char hist_name1[30];
		char hist_name2[30];
		char hist_name3[30];
		char hist_title[100];
		sprintf(hist_title, ";IM(Ks K+ pi-) for %.3f < -t <= %.3f GeV", minus_t_lower, minus_t_higher);
		sprintf(hist_name1, "Binnedf1_1285_%.3f", minus_t_higher);
		sprintf(hist_name2, "Binnedf1_1420_%.3f", minus_t_higher);
		sprintf(hist_name3, "Binnedf1_%.3f", minus_t_higher);

		dHist_IM_KsKpPim_1285_binned[i] = new TH1F(hist_name1, hist_title, 150, 1, 2.25);
		dHist_IM_KsKpPim_1420_binned[i] = new TH1F(hist_name2, hist_title, 150, 1, 2.25);
		dHist_IM_KsKpPim_binned[i] = new TH1F(hist_name3, hist_title, 150, 1, 2.25);

		char phi1_1285[18];
		char phi2_1285[18];
		char phi3_1285[18];
		char phi4_1285[18];
		char phi_hist_title[30];

		char phi1bkg_1285[18];
		char phi2bkg_1285[18];
		char phi3bkg_1285[18];
		char phi4bkg_1285[18];
		char phibkg_hist_title[40];

		char f1_1285[30];
		char f2_1285[30];
		char f3_1285[30];
		char f4_1285[30];
		char f1_hist_title[40];

		sprintf(phi_hist_title, "'#phi(f1) for %.3f < -t <= %.3f GeV", minus_t_lower, minus_t_higher);
		sprintf(phi1_1285, "phi_0_1285_%.3f", minus_t_higher);
		sprintf(phi2_1285, "phi_90_1285_%.3f", minus_t_higher);
		sprintf(phi3_1285, "phi_45_1285_%.3f", minus_t_higher);
		sprintf(phi4_1285, "phi_135_1285_%.3f", minus_t_higher);

		sprintf(phibkg_hist_title, "'#phi(bkg) for %.3f < -t <= %.3f GeV", minus_t_lower, minus_t_higher);
		sprintf(phi1bkg_1285, "phi_0_bkg_%.3f", minus_t_higher);
		sprintf(phi2bkg_1285, "phi_90_bkg_%.3f", minus_t_higher);
		sprintf(phi3bkg_1285, "phi_45_bkg_%.3f", minus_t_higher);
		sprintf(phi4bkg_1285, "phi_135_bkg_%.3f", minus_t_higher);

		dHist_Phi0_1285[i] = new TH1F(phi1_1285, phi_hist_title, 30, -3.14159265358979323846, 3.14159265358979323846);
		dHist_Phi90_1285[i] = new TH1F(phi2_1285, phi_hist_title, 30, -3.14159265358979323846, 3.14159265358979323846);
		dHist_Phi45_1285[i] = new TH1F(phi3_1285, phi_hist_title, 30, -3.14159265358979323846, 3.14159265358979323846);
		dHist_Phi135_1285[i] = new TH1F(phi4_1285, phi_hist_title, 30, -3.14159265358979323846, 3.14159265358979323846);

		dHist_Phi0_background_1285[i] = new TH1F(phi1bkg_1285, phibkg_hist_title, 30, -3.14159265358979323846, 3.14159265358979323846);
		dHist_Phi90_background_1285[i] = new TH1F(phi2bkg_1285, phibkg_hist_title, 30, -3.14159265358979323846, 3.14159265358979323846);
		dHist_Phi45_background_1285[i] = new TH1F(phi3bkg_1285, phibkg_hist_title, 30, -3.14159265358979323846, 3.14159265358979323846);
		dHist_Phi135_background_1285[i] = new TH1F(phi4bkg_1285, phibkg_hist_title, 30, -3.14159265358979323846, 3.14159265358979323846);

		sprintf(f1_hist_title, "f1(1285) for %.3f < -t <= %.3f GeV", minus_t_lower, minus_t_higher);
		sprintf(f1_1285, "f1_0_1285_%.3f", minus_t_higher);
		sprintf(f2_1285, "f1_90_1285_%.3f", minus_t_higher);
		sprintf(f3_1285, "f1_45_1285_%.3f", minus_t_higher);
		sprintf(f4_1285, "f1_135_1285_%.3f", minus_t_higher);

		dHist_f1_0_1285[i] = new TH1F(f1_1285, f1_hist_title, 150, 1, 2.25);
		dHist_f1_90_1285[i] = new TH1F(f2_1285, f1_hist_title, 150, 1, 2.25);
		dHist_f1_45_1285[i] = new TH1F(f3_1285, f1_hist_title, 150, 1, 2.25);
		dHist_f1_135_1285[i] = new TH1F(f4_1285, f1_hist_title, 150, 1, 2.25);

	}

	for(int i = 0; i < 5; i++){
		double w_lower = i * 0.28 + 3.3;
		double w_upper = (i + 1) * 0.28 + 3.3;

		char hist_name[40];
		char hist_title[100];

		char f1_hist_name[20];
		char f1_hist_title[100];

		sprintf(hist_name, "f1_costheta_%.3f", w_lower);
		sprintf(hist_title, "cos(#theta)c.m. for %.3f < W < %.3f GeV", w_lower, w_upper);

		sprintf(f1_hist_name, "f1_%.3f", w_lower);
		sprintf(f1_hist_title, "IM(Ks K- pi+) for %.3f < W < %.3f GeV", w_lower, w_upper);

		dHist_CosThetaCM[i] = new TH1F(hist_name, hist_title, 100, -1, 1);
		dHist_W_binned_f1[i] = new TH1F(f1_hist_name, f1_hist_title, 150, 1, 2.25);
	}

	//lower T range
	for(int i = 0; i < 4; i++){
		double minus_t_higher = 0.1 * (i + 1);
		double minus_t_lower = 0.1 * i;


		char hist_name5[40];
		char hist_name4[40];
		char hist_name_b7[40];
		char hist_name_b8[40];
		char hist_name_b9[40];
		char hist_name_b10[40];
		char hist_name_b11[40];
		char hist_name_b12[40];
		char hist_title[100];

		sprintf(hist_title, ";IM(Ks K+ pi-) for %.3f < -t <= %.3f GeV", minus_t_lower, minus_t_higher);
		sprintf(hist_name4, "Binnedf1_%.3f_fullbeam", minus_t_higher);
		sprintf(hist_name5, "Binnedf1_1285_%.3f_fullbeam", minus_t_higher);
		sprintf(hist_name_b11, "Binnedf1_1285_%.3f_beam_5", minus_t_higher);
		sprintf(hist_name_b12, "Binnedf1_1285_%.3f_beam_6", minus_t_higher);
		sprintf(hist_name_b7, "Binnedf1_1285_%.3f_beam_7", minus_t_higher);
		sprintf(hist_name_b8, "Binnedf1_1285_%.3f_beam_8", minus_t_higher);
		sprintf(hist_name_b9, "Binnedf1_1285_%.3f_beam_9", minus_t_higher);
		sprintf(hist_name_b10, "Binnedf1_1285_%.3f_beam_10", minus_t_higher);


		dHist_IM_KsKpPim_binned_full_low[i] = new TH1F(hist_name4, hist_title, 50, 1, 1.7);
		dHist_f1_1285_binned_full_low[i] = new TH1F(hist_name5, hist_title, 50, 1, 1.7);

		dHist_f1_1285_beam_5_low[i] = new TH1F(hist_name_b11, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_6_low[i] = new TH1F(hist_name_b12, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_7_low[i] = new TH1F(hist_name_b7, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_8_low[i] = new TH1F(hist_name_b8, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_9_low[i] = new TH1F(hist_name_b9, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_10_low[i] = new TH1F(hist_name_b10, hist_title, 50, 1, 1.7);

	}

	//medium T range
	for(int i = 0; i < 2; i++){
		double minus_t_higher = 0.4 + (0.25 * (i + 1));
		double minus_t_lower = 0.4 + (0.25 * i);


		char hist_name5[40];
		char hist_name4[40];
		char hist_name_b7[40];
		char hist_name_b8[40];
		char hist_name_b9[40];
		char hist_name_b10[40];
		char hist_name_b11[40];
		char hist_name_b12[40];
		char hist_title[100];

		sprintf(hist_title, ";IM(Ks K+ pi-) for %.3f < -t <= %.3f GeV", minus_t_lower, minus_t_higher);
		sprintf(hist_name4, "Binnedf1_%.3f_fullbeam", minus_t_higher);
		sprintf(hist_name5, "Binnedf1_1285_%.3f_fullbeam", minus_t_higher);
		sprintf(hist_name_b11, "Binnedf1_1285_%.3f_beam_5", minus_t_higher);
		sprintf(hist_name_b12, "Binnedf1_1285_%.3f_beam_6", minus_t_higher);
		sprintf(hist_name_b7, "Binnedf1_1285_%.3f_beam_7", minus_t_higher);
		sprintf(hist_name_b8, "Binnedf1_1285_%.3f_beam_8", minus_t_higher);
		sprintf(hist_name_b9, "Binnedf1_1285_%.3f_beam_9", minus_t_higher);
		sprintf(hist_name_b10, "Binnedf1_1285_%.3f_beam_10", minus_t_higher);


		dHist_IM_KsKpPim_binned_full_med[i] = new TH1F(hist_name4, hist_title, 50, 1, 1.7);
		dHist_f1_1285_binned_full_med[i] = new TH1F(hist_name5, hist_title, 50, 1, 1.7);

		dHist_f1_1285_beam_5_med[i] = new TH1F(hist_name_b11, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_6_med[i] = new TH1F(hist_name_b12, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_7_med[i] = new TH1F(hist_name_b7, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_8_med[i] = new TH1F(hist_name_b8, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_9_med[i] = new TH1F(hist_name_b9, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_10_med[i] = new TH1F(hist_name_b10, hist_title, 50, 1, 1.7);

	}
	
	//high T range
	for(int i = 0; i < 2; i++){
		double minus_t_higher = 0.9 + (0.5 * (i + 1));
		double minus_t_lower = 0.9 + (0.5 * i);


		char hist_name5[40];
		char hist_name4[40];
		char hist_name_b7[40];
		char hist_name_b8[40];
		char hist_name_b9[40];
		char hist_name_b10[40];
		char hist_name_b11[40];
		char hist_name_b12[40];
		char hist_title[100];

		sprintf(hist_title, ";IM(Ks K+ pi-) for %.3f < -t <= %.3f GeV", minus_t_lower, minus_t_higher);
		sprintf(hist_name4, "Binnedf1_%.3f_fullbeam", minus_t_higher);
		sprintf(hist_name5, "Binnedf1_1285_%.3f_fullbeam", minus_t_higher);
		sprintf(hist_name_b11, "Binnedf1_1285_%.3f_beam_5", minus_t_higher);
		sprintf(hist_name_b12, "Binnedf1_1285_%.3f_beam_6", minus_t_higher);
		sprintf(hist_name_b7, "Binnedf1_1285_%.3f_beam_7", minus_t_higher);
		sprintf(hist_name_b8, "Binnedf1_1285_%.3f_beam_8", minus_t_higher);
		sprintf(hist_name_b9, "Binnedf1_1285_%.3f_beam_9", minus_t_higher);
		sprintf(hist_name_b10, "Binnedf1_1285_%.3f_beam_10", minus_t_higher);


		dHist_IM_KsKpPim_binned_full_high[i] = new TH1F(hist_name4, hist_title, 50, 1, 1.7);
		dHist_f1_1285_binned_full_high[i] = new TH1F(hist_name5, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_5_high[i] = new TH1F(hist_name_b11, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_6_high[i] = new TH1F(hist_name_b12, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_7_high[i] = new TH1F(hist_name_b7, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_8_high[i] = new TH1F(hist_name_b8, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_9_high[i] = new TH1F(hist_name_b9, hist_title, 50, 1, 1.7);
		dHist_f1_1285_beam_10_high[i] = new TH1F(hist_name_b10, hist_title, 50, 1, 1.7);
	}

	for(int i = 0; i < 15; i++){
		double minus_t_higher = 0.2 * (i + 1);
		double minus_t_lower = 0.2 * i;

		char hist_name[30];
		char hist_title[100];
		sprintf(hist_title, ";IM(Ks K- pi+) for %.3f < -t' <= %.3f GeV^2", minus_t_lower, minus_t_higher);
		sprintf(hist_name, "Binnedf1_%.3f_fullbeam_tprime", minus_t_higher);

		dHist_f1_1285_tmin[i] = new TH1F(hist_name, hist_title, 150, 1, 2.25);
	}

	/************************** EXAMPLE USER INITIALIZATION: CUSTOM OUTPUT BRANCHES - MAIN TREE *************************/

	//EXAMPLE MAIN TREE CUSTOM BRANCHES (OUTPUT ROOT FILE NAME MUST FIRST BE GIVEN!!!! (ABOVE: TOP)):
	//The type for the branch must be included in the brackets
	//1st function argument is the name of the branch
	//2nd function argument is the name of the branch that contains the size of the array (for fundamentals only)
	/*
	dTreeInterface->Create_Branch_Fundamental<Int_t>("my_int"); //fundamental = char, int, float, double, etc.
	dTreeInterface->Create_Branch_FundamentalArray<Int_t>("my_int_array", "my_int");
	dTreeInterface->Create_Branch_FundamentalArray<Float_t>("my_combo_array", "NumCombos");
	dTreeInterface->Create_Branch_NoSplitTObject<TLorentzVector>("my_p4");
	dTreeInterface->Create_Branch_ClonesArray<TLorentzVector>("my_p4_array");
	*/

	/************************** EXAMPLE USER INITIALIZATION: CUSTOM OUTPUT BRANCHES - FLAT TREE *************************/

	//EXAMPLE FLAT TREE CUSTOM BRANCHES (OUTPUT ROOT FILE NAME MUST FIRST BE GIVEN!!!! (ABOVE: TOP)):
	//The type for the branch must be included in the brackets
	//1st function argument is the name of the branch
	//2nd function argument is the name of the branch that contains the size of the array (for fundamentals only)
	/*
	dFlatTreeInterface->Create_Branch_Fundamental<Int_t>("flat_my_int"); //fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_FundamentalArray<Int_t>("flat_my_int_array", "flat_my_int");
	dFlatTreeInterface->Create_Branch_NoSplitTObject<TLorentzVector>("flat_my_p4");
	dFlatTreeInterface->Create_Branch_ClonesArray<TLorentzVector>("flat_my_p4_array");
	*/

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("e_beam"); //fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("accidental_weight"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("minus_t");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pimkpks_e"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pimkpks_px"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pimkpks_py"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pimkpks_pz"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pimkpks_phi"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pimkpks_theta");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_e"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_px"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_py"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_pz"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kstar_m");  
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("w"); 
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("tmin");  


	/************************************* ADVANCED EXAMPLE: CHOOSE BRANCHES TO READ ************************************/

	//TO SAVE PROCESSING TIME
		//If you know you don't need all of the branches/data, but just a subset of it, you can speed things up
		//By default, for each event, the data is retrieved for all branches
		//If you know you only need data for some branches, you can skip grabbing data from the branches you don't need
		//Do this by doing something similar to the commented code below

	//dTreeInterface->Clear_GetEntryBranches(); //now get none
	//dTreeInterface->Register_GetEntryBranch("Proton__P4"); //manually set the branches you want

	/************************************** DETERMINE IF ANALYZING SIMULATED DATA *************************************/

	dIsMC = (dTreeInterface->Get_Branch("MCWeight") != NULL);

}

Bool_t DSelector_f1_pimkpks::Process(Long64_t locEntry)
{
	// The Process() function is called for each entry in the tree. The entry argument
	// specifies which entry in the currently loaded tree is to be processed.
	//
	// This function should contain the "body" of the analysis. It can contain
	// simple or elaborate selection criteria, run algorithms on the data
	// of the event and typically fill histograms.
	//
	// The processing can be stopped by calling Abort().
	// Use fStatus to set the return value of TTree::Process().
	// The return value is currently not used.

	//CALL THIS FIRST
	DSelector::Process(locEntry); //Gets the data from the tree for the entry
	//cout << "RUN " << Get_RunNumber() << ", EVENT " << Get_EventNumber() << endl;
	//TLorentzVector locProductionX4 = Get_X4_Production();

	/******************************************** GET POLARIZATION ORIENTATION ******************************************/

	//Only if the run number changes
	//RCDB environment must be setup in order for this to work! (Will return false otherwise)
	UInt_t locRunNumber = Get_RunNumber();
	if(locRunNumber != dPreviousRunNumber)
	{
		dIsPolarizedFlag = dAnalysisUtilities.Get_IsPolarizedBeam(locRunNumber, dIsPARAFlag);
		dPreviousRunNumber = locRunNumber;
	}

	/********************************************* SETUP UNIQUENESS TRACKING ********************************************/

	//ANALYSIS ACTIONS: Reset uniqueness tracking for each action
	//For any actions that you are executing manually, be sure to call Reset_NewEvent() on them here
	Reset_Actions_NewEvent();
	dAnalyzeCutActions->Reset_NewEvent(); // manual action, must call Reset_NewEvent()

	//PREVENT-DOUBLE COUNTING WHEN HISTOGRAMMING
		//Sometimes, some content is the exact same between one combo and the next
			//e.g. maybe two combos have different beam particles, but the same data for the final-state
		//When histogramming, you don't want to double-count when this happens: artificially inflates your signal (or background)
		//So, for each quantity you histogram, keep track of what particles you used (for a given combo)
		//Then for each combo, just compare to what you used before, and make sure it's unique

	//EXAMPLE 1: Particle-specific info:
	set<Int_t> locUsedSoFar_BeamEnergy; //Int_t: Unique ID for beam particles. set: easy to use, fast to search

	//EXAMPLE 2: Combo-specific info:
		//In general: Could have multiple particles with the same PID: Use a set of Int_t's
		//In general: Multiple PIDs, so multiple sets: Contain within a map
		//Multiple combos: Contain maps within a set (easier, faster to search)
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MissingMass;
	set<set<Int_t> > locUsedSoFar_IM_PipPim2;
	set<set<Int_t> > locUsedSoFar_Im_Pim1P;
	set<set<Int_t> > locUsedSoFar_IM_KsKpPim;
	set<set<Int_t> > locUsedSoFar_IM_KsPim;
	set<set<Int_t> > locUsedSoFar_IM_PKp;
	set<set<Int_t> > locUsedSoFar_IM_KsKp;
	set<set<Int_t> > locUsedSoFar_IM_KpPim;
	set<set<Int_t> > locUsedSoFar_IM_PKs;
	set<set<Int_t> > locUsedSoFar_KsKpPim_Dalitz;


	//INSERT USER ANALYSIS UNIQUENESS TRACKING HERE

	/**************************************** EXAMPLE: FILL CUSTOM OUTPUT BRANCHES **************************************/

	/*
	Int_t locMyInt = 7;
	dTreeInterface->Fill_Fundamental<Int_t>("my_int", locMyInt);

	TLorentzVector locMyP4(4.0, 3.0, 2.0, 1.0);
	dTreeInterface->Fill_TObject<TLorentzVector>("my_p4", locMyP4);

	for(int loc_i = 0; loc_i < locMyInt; ++loc_i)
		dTreeInterface->Fill_Fundamental<Int_t>("my_int_array", 3*loc_i, loc_i); //2nd argument = value, 3rd = array index
	*/

	/************************************************* LOOP OVER COMBOS *************************************************/

	//Loop over combos
	for(UInt_t loc_i = 0; loc_i < Get_NumCombos(); ++loc_i)
	{
		// cout<<Get_RunNumber()<<endl;
		//Set branch array indices for combo and all combo particles
		dComboWrapper->Set_ComboIndex(loc_i);

		// Is used to indicate when combos have been cut
		if(dComboWrapper->Get_IsComboCut()) // Is false when tree originally created
			continue; // Combo has been cut previously

		/********************************************** GET PARTICLE INDICES *********************************************/

		//Used for tracking uniqueness when filling histograms, and for determining unused particles

		//Step 0
		Int_t locBeamID = dComboBeamWrapper->Get_BeamID();
		Int_t locPiMinus1TrackID = dPiMinus1Wrapper->Get_TrackID();
		Int_t locKPlusTrackID = dKPlusWrapper->Get_TrackID();
		Int_t locProtonTrackID = dProtonWrapper->Get_TrackID();

		//Step 1
		Int_t locPiMinus2TrackID = dPiMinus2Wrapper->Get_TrackID();
		Int_t locPiPlusTrackID = dPiPlusWrapper->Get_TrackID();

		/*********************************************** GET FOUR-MOMENTUM **********************************************/

		// Get P4's: //is kinfit if kinfit performed, else is measured
		//dTargetP4 is target p4
		//Step 0
		TLorentzVector locBeamP4 = dComboBeamWrapper->Get_P4();
		TLorentzVector locPiMinus1P4 = dPiMinus1Wrapper->Get_P4();
		TLorentzVector locKPlusP4 = dKPlusWrapper->Get_P4();
		TLorentzVector locProtonP4 = dProtonWrapper->Get_P4();
		//Step 1
		TLorentzVector locPiMinus2P4 = dPiMinus2Wrapper->Get_P4();
		TLorentzVector locPiPlusP4 = dPiPlusWrapper->Get_P4();

		// Get Measured P4's:
		//Step 0
		TLorentzVector locBeamP4_Measured = dComboBeamWrapper->Get_P4_Measured();
		TLorentzVector locPiMinus1P4_Measured = dPiMinus1Wrapper->Get_P4_Measured();
		TLorentzVector locKPlusP4_Measured = dKPlusWrapper->Get_P4_Measured();
		TLorentzVector locProtonP4_Measured = dProtonWrapper->Get_P4_Measured();
		//Step 1
		TLorentzVector locPiMinus2P4_Measured = dPiMinus2Wrapper->Get_P4_Measured();
		TLorentzVector locPiPlusP4_Measured = dPiPlusWrapper->Get_P4_Measured();

		// Get X4's: //is kinfit if kinfit performed, else is measured
		//dTargetX4 is target x4
		//Step 0
		TLorentzVector locBeamX4 = dComboBeamWrapper->Get_X4();
		TLorentzVector locPiMinus1X4 = dPiMinus1Wrapper->Get_X4();
		TLorentzVector locKPlusX4 = dKPlusWrapper->Get_X4();
		TLorentzVector locProtonX4 = dProtonWrapper->Get_X4();
		//Step 1
		TLorentzVector locPiMinus2X4 = dPiMinus2Wrapper->Get_X4();
		TLorentzVector locPiPlusX4 = dPiPlusWrapper->Get_X4();

		// Get Measured X4's:
		//Step 0
		//TLorentzVector locBeamX4_Measured = dComboBeamWrapper->Get_X4_Measured();
		TLorentzVector locPiMinus1X4_Measured = dPiMinus1Wrapper->Get_X4_Measured();
		TLorentzVector locKPlusX4_Measured = dKPlusWrapper->Get_X4_Measured();
		TLorentzVector locProtonX4_Measured = dProtonWrapper->Get_X4_Measured();
		//Step 1
		TLorentzVector locPiMinus2X4_Measured = dPiMinus2Wrapper->Get_X4_Measured();
		TLorentzVector locPiPlusX4_Measured = dPiPlusWrapper->Get_X4_Measured();

		// Get boosted CM vectors
		TLorentzVector cms = locBeamP4 + dTargetP4;
		TVector3 locBoost_cms = -cms.BoostVector();
		TLorentzVector locCMSKPlusP4_Measured = dKPlusWrapper->Get_P4_Measured();
		locCMSKPlusP4_Measured.Boost(locBoost_cms);
		TLorentzVector locCMSPiMinus1P4_Measured = dPiMinus1Wrapper->Get_P4_Measured();
		locCMSPiMinus1P4_Measured.Boost(locBoost_cms);
		TLorentzVector locCMSPiMinus2P4_Measured = dPiMinus2Wrapper->Get_P4_Measured();
		locCMSPiMinus2P4_Measured.Boost(locBoost_cms);
		TLorentzVector locCMSPiPlusP4_Measured = dPiPlusWrapper->Get_P4_Measured();
		locCMSPiPlusP4_Measured.Boost(locBoost_cms);

		/********************************************* GET COMBO RF TIMING INFO *****************************************/

		TLorentzVector locBeamX4_Measured = dComboBeamWrapper->Get_X4_Measured();
		Double_t locBunchPeriod = dAnalysisUtilities.Get_BeamBunchPeriod(Get_RunNumber());
		Double_t locDeltaT_RF = dAnalysisUtilities.Get_DeltaT_RF(Get_RunNumber(), locBeamX4_Measured, dComboWrapper);
		Int_t locRelBeamBucket = dAnalysisUtilities.Get_RelativeBeamBucket(Get_RunNumber(), locBeamX4_Measured, dComboWrapper); // 0 for in-time events, non-zero integer for out-of-time photons
		Int_t locNumOutOfTimeBunchesInTree = 4; //YOU need to specify this number
			//Number of out-of-time beam bunches in tree (on a single side, so that total number out-of-time bunches accepted is 2 times this number for left + right bunches) 

		Bool_t locSkipNearestOutOfTimeBunch = true; // True: skip events from nearest out-of-time bunch on either side (recommended).
		Int_t locNumOutOfTimeBunchesToUse = locSkipNearestOutOfTimeBunch ? locNumOutOfTimeBunchesInTree-1:locNumOutOfTimeBunchesInTree; 
		Double_t locAccidentalScalingFactor = dAnalysisUtilities.Get_AccidentalScalingFactor(Get_RunNumber(), locBeamP4.E(), dIsMC); // Ideal value would be 1, but deviations require added factor, which is different for data and MC.
		Double_t locAccidentalScalingFactorError = dAnalysisUtilities.Get_AccidentalScalingFactorError(Get_RunNumber(), locBeamP4.E()); // Ideal value would be 1, but deviations observed, need added factor.
		Double_t locHistAccidWeightFactor = locRelBeamBucket==0 ? 1 : -locAccidentalScalingFactor/(2*locNumOutOfTimeBunchesToUse) ; // Weight by 1 for in-time events, ScalingFactor*(1/NBunches) for out-of-time
		if(locSkipNearestOutOfTimeBunch && abs(locRelBeamBucket)==1) { // Skip nearest out-of-time bunch: tails of in-time distribution also leak in
			dComboWrapper->Set_IsComboCut(true); 
			continue; 
		} 

		// FLIGHT SIGNIFIGANCE CALCULATIONS AND CUT
		TLorentzVector locProdSpacetimeVertex = dComboBeamWrapper->Get_X4();
		TLorentzVector locDecayingKShortX4 = dTreeInterface->Get_TObject<TLorentzVector>("DecayingKShort__X4",loc_i);
		TLorentzVector locDeltaSpacetimeKs = locProdSpacetimeVertex - locDecayingKShortX4;
		double locPathLengthKs = locDeltaSpacetimeKs.Vect().Mag();
 		float locPathLengthSigmaKs = Get_Fundamental<Float_t>("DecayingKShort__PathLengthSigma", loc_i);
 		double locPathLengthSignificanceKs = locPathLengthKs/locPathLengthSigmaKs;

		if(locPathLengthSignificanceKs < 5){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		/********************************************* COMBINE FOUR-MOMENTUM ********************************************/

		// DO YOUR STUFF HERE

		// Combine 4-vectors
		TLorentzVector locMissingP4_Measured = locBeamP4_Measured + dTargetP4;
		locMissingP4_Measured -= locPiMinus1P4_Measured + locKPlusP4_Measured + locProtonP4_Measured + locPiMinus2P4_Measured + locPiPlusP4_Measured;
		TLorentzVector locPimP = locProtonP4 + locPiMinus1P4;
		TLorentzVector locKs = locPiMinus2P4 + locPiPlusP4;
		TLorentzVector locKpP = locKPlusP4 + locProtonP4;
		TLorentzVector locKsKpPim = locKs  + locKPlusP4 + locPiMinus1P4;
		TLorentzVector locKsKp = locKs  + locKPlusP4;
		TLorentzVector locKsPim = locKs + locPiMinus1P4;
		TLorentzVector locKpPim = locKPlusP4 + locPiMinus1P4;
		TLorentzVector locPKs = locKs + locProtonP4;
		TLorentzVector locCMSF1 = locCMSKPlusP4_Measured + locCMSPiMinus1P4_Measured + locCMSPiMinus2P4_Measured + locCMSPiPlusP4_Measured;


		/******************************************** EXECUTE ANALYSIS ACTIONS *******************************************/

		// Loop through the analysis actions, executing them in order for the active particle combo
		dAnalyzeCutActions->Perform_Action(); // Must be executed before Execute_Actions()
		if(!Execute_Actions()) //if the active combo fails a cut, IsComboCutFlag automatically set
			continue;

		//if you manually execute any actions, and it fails a cut, be sure to call:
			//dComboWrapper->Set_IsComboCut(true);

		/**************************************** EXAMPLE: FILL CUSTOM OUTPUT BRANCHES **************************************/

		/*
		TLorentzVector locMyComboP4(8.0, 7.0, 6.0, 5.0);
		//for arrays below: 2nd argument is value, 3rd is array index
		//NOTE: By filling here, AFTER the cuts above, some indices won't be updated (and will be whatever they were from the last event)
			//So, when you draw the branch, be sure to cut on "IsComboCut" to avoid these.
		dTreeInterface->Fill_Fundamental<Float_t>("my_combo_array", -2*loc_i, loc_i);
		dTreeInterface->Fill_TObject<TLorentzVector>("my_p4_array", locMyComboP4, loc_i);
		*/

		double locKinFit_CL = dComboWrapper->Get_ConfidenceLevel_KinFit("");

		if(locKinFit_CL < 1E-3){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		/**************************************** EXAMPLE: HISTOGRAM BEAM ENERGY *****************************************/

		//Histogram beam energy (if haven't already)
		if(locUsedSoFar_BeamEnergy.find(locBeamID) == locUsedSoFar_BeamEnergy.end())
		{
			dHist_BeamEnergy->Fill(locBeamP4.E()); // Fills in-time and out-of-time beam photon combos
			//dHist_BeamEnergy->Fill(locBeamP4.E(),locHistAccidWeightFactor); // Alternate version with accidental subtraction

			locUsedSoFar_BeamEnergy.insert(locBeamID);
		}

		/************************************ EXAMPLE: HISTOGRAM MISSING MASS SQUARED ************************************/

		//Missing Mass Squared
		double locMissingMassSquared = locMissingP4_Measured.M2();

		//Uniqueness tracking: Build the map of particles used for the missing mass
			//For beam: Don't want to group with final-state photons. Instead use "Unknown" PID (not ideal, but it's easy).
		map<Particle_t, set<Int_t> > locUsedThisCombo_MissingMass;
		locUsedThisCombo_MissingMass[Unknown].insert(locBeamID); //beam
		locUsedThisCombo_MissingMass[PiMinus].insert(locPiMinus1TrackID);
		locUsedThisCombo_MissingMass[KPlus].insert(locKPlusTrackID);
		locUsedThisCombo_MissingMass[Proton].insert(locProtonTrackID);
		locUsedThisCombo_MissingMass[PiMinus].insert(locPiMinus2TrackID);
		locUsedThisCombo_MissingMass[PiPlus].insert(locPiPlusTrackID);

		//compare to what's been used so far
		if(locUsedSoFar_MissingMass.find(locUsedThisCombo_MissingMass) == locUsedSoFar_MissingMass.end())
		{
			//unique missing mass combo: histogram it, and register this combo of particles
			dHist_MissingMassSquared->Fill(locMissingMassSquared); // Fills in-time and out-of-time beam photon combos
			//dHist_MissingMassSquared->Fill(locMissingMassSquared,locHistAccidWeightFactor); // Alternate version with accidental subtraction

			locUsedSoFar_MissingMass.insert(locUsedThisCombo_MissingMass);
		}

		//E.g. Cut
		if((locMissingMassSquared < -0.03) || (locMissingMassSquared > 0.03))
		{
			dComboWrapper->Set_IsComboCut(true);
			continue;
		}


/************************************ EXAMPLE: DOCA AND COLINIEARITY ************************************/

		// -------- FOR K_SHORT DECAY VERTEX -------------

		TVector3 PiPlus_P3 = locPiPlusP4_Measured.Vect();
		TVector3 PiMinus2_P3 = locPiMinus2P4_Measured.Vect();


		TVector3 PiMinus2_X3 = locPiMinus2X4_Measured.Vect();
		TVector3 PiPlus_X3 = locPiPlusX4_Measured.Vect();


		TVector3 locUnitDir1 = PiPlus_P3.Unit();
		TVector3 locUnitDir2 = PiMinus2_P3.Unit();
		TVector3 locVertex1 = PiPlus_X3;
		TVector3 locVertex2 = PiMinus2_X3;

		TVector3 locPOCA1;
		TVector3 locPOCA2;

		double DOCA_a = 0.;

		//Calc_DOCA(locUnitDir1, locUnitDir2, locVertex1, locVertex2);

		double locUnitDot = locUnitDir1.Dot(locUnitDir2);
		double locDenominator = locUnitDot*locUnitDot - 1.0; // scalar product of directions
		double locDistVertToInterDOCA1 = 0.0, locDistVertToInterDOCA2 = 0.0; //distance from vertex to DOCA point

		if(fabs(locDenominator) < 1.0e-15) //parallel
		{
			locDistVertToInterDOCA1 = (locVertex2 - locVertex1).Dot(locUnitDir2)/locUnitDot; //the opposite
			locDistVertToInterDOCA2 = (locVertex1 - locVertex2).Dot(locUnitDir1)/locUnitDot;
		}
		else
		{
			double locA = (locVertex1 - locVertex2).Dot(locUnitDir1);
			double locB = (locVertex1 - locVertex2).Dot(locUnitDir2);
			locDistVertToInterDOCA1 = (locA - locUnitDot*locB)/locDenominator;
			locDistVertToInterDOCA2 = (locUnitDot*locA - locB)/locDenominator;
		}

		locPOCA1 = locVertex1 + locDistVertToInterDOCA1*locUnitDir1; //intersection point of DOCA line and track 1
		locPOCA2 = locVertex2 + locDistVertToInterDOCA2*locUnitDir2; //intersection point of DOCA line and track 2

		DOCA_a = (locPOCA1 - locPOCA2).Mag();


		TVector3 locDOCAVertex_K_s;

		locDOCAVertex_K_s = 0.5*(locPOCA1 + locPOCA2); // Find Secondary vertex(decay vertex of K_s)



		// -------- FOR PRIMARY VERTEX -------------


		TVector3 BeamP3 = locBeamP4_Measured.Vect();
		TVector3 ProtonP3 = locProtonP4_Measured.Vect();

		TVector3 BeamX3 = locBeamX4_Measured.Vect();
		TVector3 ProtonX3 = locProtonX4_Measured.Vect();

		TVector3 locUnitDir3 = (1.0/BeamP3.Mag())*BeamP3;
		TVector3 locUnitDir4 = (1.0/ProtonP3.Mag())*ProtonP3;
		TVector3 locVertex3 = BeamX3;
		TVector3 locVertex4 = ProtonX3;

		TVector3 locPOCA3;
		TVector3 locPOCA4;

		double DOCA_b = 0.;

		//Calc_DOCA(locUnitDir1, locUnitDir2, locVertex1, locVertex2);

		double locUnitDot2 = locUnitDir3.Dot(locUnitDir4);
		double locDenominator2 = locUnitDot2*locUnitDot2 - 1.0; // scalar product of directions
		double locDistVertToInterDOCA3 = 0.0, locDistVertToInterDOCA4 = 0.0; //distance from vertex to DOCA point

		if(fabs(locDenominator2) < 1.0e-15) //parallel
		{
			locDistVertToInterDOCA3 = (locVertex4 - locVertex3).Dot(locUnitDir4)/locUnitDot2; //the opposite
			locDistVertToInterDOCA4 = (locVertex3 - locVertex4).Dot(locUnitDir3)/locUnitDot2;
		}
		else
		{
			double locC = (locVertex3 - locVertex4).Dot(locUnitDir3);
			double locD = (locVertex3 - locVertex4).Dot(locUnitDir4);
			locDistVertToInterDOCA3 = (locC - locUnitDot2*locD)/locDenominator2;
			locDistVertToInterDOCA4 = (locUnitDot2*locC - locD)/locDenominator2;
		}

		locPOCA3 = locVertex3 + locDistVertToInterDOCA3*locUnitDir3; //intersection point of DOCA line and track 1
		locPOCA4 = locVertex4 + locDistVertToInterDOCA4*locUnitDir4; //intersection point of DOCA line and track 2

		DOCA_b = (locPOCA3 - locPOCA4).Mag();


		TVector3 locDOCAVertex_proton;

		locDOCAVertex_proton = 0.5*(locPOCA3 + locPOCA4); // Find Primary vertex


		//------- For K-short ---------------------

		TVector3 DOCA_line_Ks; // line connecting the primary vertex and secondary vertex of Ks_1

		DOCA_line_Ks = locDOCAVertex_K_s - locDOCAVertex_proton;

		TVector3 K_s_momentum; // K_short momentum vector

		K_s_momentum = PiPlus_P3 + PiMinus2_P3;

		double theta_col = DOCA_line_Ks.Angle(K_s_momentum);

		double cos_theta_col = TMath::Cos(theta_col);

		double vertex_distance_Ks = 0.;

		vertex_distance_Ks = (locDOCAVertex_K_s - locDOCAVertex_proton).Mag();

		if(vertex_distance_Ks < 2.0){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		if(cos_theta_col < 0.98){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		/********************************************************************************************************/

		double im_pippim2 = locKs.M();
		
		set<Int_t> locUsedThisCombo_IM_PipPim2;
		locUsedThisCombo_IM_PipPim2.insert(locPiMinus2TrackID);
		locUsedThisCombo_IM_PipPim2.insert(locPiPlusTrackID);


		if(locUsedSoFar_IM_PipPim2.find(locUsedThisCombo_IM_PipPim2) == locUsedSoFar_IM_PipPim2.end()){
			dHist_DOCA_vs_IM_PipPim->Fill(im_pippim2, vertex_distance_Ks, locHistAccidWeightFactor);
			dHist_CosTheta_vs_IM_PipPim->Fill(im_pippim2, cos_theta_col, locHistAccidWeightFactor);
			dHist_IM_PipPim2->Fill(im_pippim2, locHistAccidWeightFactor);
			dHist_Ks_vs_FlightSig->Fill(im_pippim2, locPathLengthSignificanceKs, locHistAccidWeightFactor);

			locUsedSoFar_IM_PipPim2.insert(locUsedThisCombo_IM_PipPim2);
		}

		if(im_pippim2 > 0.55 || im_pippim2 < 0.45){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		double im_kppim = locKpPim.M();
		set<Int_t> locUsedThisCombo_KpPim;
		locUsedThisCombo_KpPim.insert(locKPlusTrackID);
		locUsedThisCombo_KpPim.insert(locPiMinus1TrackID);

		if(locUsedSoFar_IM_KpPim.find(locUsedThisCombo_KpPim) == locUsedSoFar_IM_KpPim.end()){
			dHist_IM_KpPim->Fill(im_kppim);

			locUsedSoFar_IM_KpPim.insert(locUsedThisCombo_KpPim);
		}

		double im_kspim = locKsPim.M();
		double im_kskppim = locKsKpPim.M();

		set<Int_t> locUsedThisCombo_KsPim;
		locUsedThisCombo_KsPim.insert(locPiPlusTrackID);
		locUsedThisCombo_KsPim.insert(locPiMinus2TrackID);
		locUsedThisCombo_KsPim.insert(locPiMinus1TrackID);

		if(locUsedSoFar_IM_KsPim.find(locUsedThisCombo_KsPim) == locUsedSoFar_IM_KsPim.end()){
			dHist_IM_KsPim->Fill(im_kspim);

			locUsedSoFar_IM_KsPim.insert(locUsedThisCombo_KsPim);
		}

		set<Int_t> locUsedThisCombo_KsKpPim_Dalitz;
		locUsedThisCombo_KsKpPim_Dalitz.insert(locPiMinus1TrackID);
		locUsedThisCombo_KsKpPim_Dalitz.insert(locPiMinus2TrackID);
		locUsedThisCombo_KsKpPim_Dalitz.insert(locKPlusTrackID);
		locUsedThisCombo_KsKpPim_Dalitz.insert(locPiPlusTrackID);

		if(locUsedSoFar_KsKpPim_Dalitz.find(locUsedThisCombo_KsKpPim_Dalitz) == locUsedSoFar_KsKpPim_Dalitz.end()){
			if(im_kskppim > 1.1 && im_kskppim <= 1.3){
				dHist_KsPim_KpPim_Dalitz_1100_1350->Fill(locKsPim.M2(), locKpPim.M2(), locHistAccidWeightFactor);
			}
			if(im_kskppim > 1.3 && im_kskppim <= 1.5){
				dHist_KsPim_KpPim_Dalitz_1350_1500->Fill(locKsPim.M2(), locKpPim.M2(), locHistAccidWeightFactor);

			}
			if(im_kskppim > 1.5){
				dHist_KsPim_KpPim_Dalitz_1500->Fill(locKsPim.M2(), locKpPim.M2(), locHistAccidWeightFactor);

			}
			locUsedSoFar_KsKpPim_Dalitz.insert(locUsedThisCombo_KsKpPim_Dalitz);
		}

		double im_ppim = locPimP.M();
		set<Int_t> locUsedThisCombo_PPim;
		locUsedThisCombo_PPim.insert(locPiMinus1TrackID);
		locUsedThisCombo_PPim.insert(locProtonTrackID);

		if(locUsedSoFar_Im_Pim1P.find(locUsedThisCombo_PPim) == locUsedSoFar_Im_Pim1P.end()){
			dHist_IM_Pim1P->Fill(im_ppim);

			locUsedSoFar_Im_Pim1P.insert(locUsedThisCombo_PPim);
		}

		if(im_ppim < 1.8){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		if(im_kspim > 0.8 && im_kspim < 1.0){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		double kpp = locKpP.M();
		set<Int_t> locUsedThisCombo_IM_PKp;
		locUsedThisCombo_IM_PKp.insert(locKPlusTrackID);
		locUsedThisCombo_IM_PKp.insert(locProtonTrackID);

		if(locUsedSoFar_IM_PKp.find(locUsedThisCombo_IM_PKp) == locUsedSoFar_IM_PKp.end()){
			dHist_IM_PKp->Fill(kpp);

			locUsedSoFar_IM_PKp.insert(locUsedThisCombo_IM_PKp);
		}


/////////////////////////////////////// 

		// double im_kskppim = locKsKpPim.M();	
		double minus_t = -1 * (dTargetP4 - locProtonP4_Measured).M2();
		double beam_energy = locBeamP4.E();
		int t_index = minus_t / 0.2;
		double f1_phi = locKsKpPim.Phi();
		double f1_theta = locKsKpPim.Theta();
		double w = (locBeamP4_Measured + dTargetP4).M();
		double s = w * w;
		int w_index = (w - 3.3)/0.28;
		double cosThetaCM = locCMSF1.CosTheta();

		double target_mass2 = dTargetP4.M2();
		double m2_kskppim = im_kskppim * im_kskppim;
		double m2_p = locProtonP4_Measured.M2();

		double lambda1 = s*s + target_mass2 * target_mass2 - 2*s*target_mass2;
		double lambda2 = s*s + m2_kskppim*m2_kskppim + m2_p*m2_p - 2*(s*m2_kskppim + s*m2_p + m2_kskppim*m2_p);

		double q1 = sqrt(lambda1/s)/2;
		double q2 = sqrt(lambda2/s)/2;
		double tmin = (-1*target_mass2 + m2_p - m2_kskppim) * (-1*target_mass2 + m2_p - m2_kskppim) / (4 * s) - pow(q1-q2, 2);

		double tprime = minus_t + tmin;
		int tprime_index = tprime / 0.2;

		int polAngle;

		set<Int_t> locUsedThisCombo_IM_KsKpPim;
		locUsedThisCombo_IM_KsKpPim.insert(locPiMinus1TrackID);
		locUsedThisCombo_IM_KsKpPim.insert(locPiPlusTrackID); 
		locUsedThisCombo_IM_KsKpPim.insert(locKPlusTrackID);
		locUsedThisCombo_IM_KsKpPim.insert(locPiMinus2TrackID);
		locUsedThisCombo_IM_KsKpPim.insert(locProtonTrackID);

		if(locUsedSoFar_IM_KsKpPim.find(locUsedThisCombo_IM_KsKpPim) == locUsedSoFar_IM_KsKpPim.end()){
			locUsedSoFar_IM_KsKpPim.insert(locUsedThisCombo_IM_KsKpPim);
			// dHist_Pip1P_vs_KsKpPim->Fill(im_kskppim, im_ppip, locHistAccidWeightFactor);
			// dHist_KmP_KsKpPim->Fill(im_kskppim, im_kmp, locHistAccidWeightFactor);
			// dHist_DOCA_vs_IM_KsKpPim->Fill(im_kskppim, vertex_distance_Ks, locHistAccidWeightFactor);
			// dHist_CosTheta_vs_IM_KsKpPim->Fill(im_kskppim, cos_theta_col, locHistAccidWeightFactor);
			dHist_IM_KsKpPim->Fill(im_kskppim, locHistAccidWeightFactor);
			dHist_W->Fill(w);
			dHist_TMin->Fill(tmin);

			//f1_1285
			//if(im_kmpip < 0.8 || im_kmpip > 1.0){ uncomment to cut k*0

			dHist_IM_KsKpPim_1285->Fill(im_kskppim, locHistAccidWeightFactor);
			dHist_KsKp_vs_PimKpKs->Fill(im_kskppim, locKsKp.M(), locHistAccidWeightFactor);
			dHist_KsPim_vs_PimKpKs->Fill(im_kskppim, locKsPim.M(), locHistAccidWeightFactor);
			dHist_KpPim_vs_PimKpKs->Fill(im_kskppim, locKpPim.M(), locHistAccidWeightFactor);
				
			if(tprime < 3){
				dHist_f1_1285_tmin[tprime_index]->Fill(im_kskppim, locHistAccidWeightFactor);
				}
				
				if(minus_t <=0.4){
					t_index = minus_t / 0.1;
					dHist_f1_1285_binned_full_low[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					
					if(beam_energy > 4.5 && beam_energy < 5.5){
						dHist_f1_1285_beam_5_low[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 5.5 && beam_energy < 6.5){
						dHist_f1_1285_beam_6_low[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 6.5 && beam_energy < 7.5){
						dHist_f1_1285_beam_7_low[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 7.5 && beam_energy < 8.5){
						dHist_f1_1285_beam_8_low[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 8.5 && beam_energy < 9.5){
						dHist_f1_1285_beam_9_low[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 9.5 && beam_energy < 10.5){
						dHist_f1_1285_beam_10_low[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
				}

				else if(minus_t > 0.4 && minus_t <= 0.9){
					t_index = (minus_t - 0.4 ) / 0.25;

					dHist_f1_1285_binned_full_med[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					
					if(beam_energy > 4.5 && beam_energy < 5.5){
						dHist_f1_1285_beam_5_med[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 5.5 && beam_energy < 6.5){
						dHist_f1_1285_beam_6_med[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 6.5 && beam_energy < 7.5){
						dHist_f1_1285_beam_7_med[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 7.5 && beam_energy < 8.5){
						dHist_f1_1285_beam_8_med[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 8.5 && beam_energy < 9.5){
						dHist_f1_1285_beam_9_med[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 9.5 && beam_energy < 10.5){
						dHist_f1_1285_beam_10_med[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
				}

				else if(minus_t > 0.9 && minus_t <= 1.9){
					t_index = (minus_t - 0.9 ) / 0.5;

					dHist_f1_1285_binned_full_high[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					
					if(beam_energy > 4.5 && beam_energy < 5.5){
						dHist_f1_1285_beam_5_high[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 5.5 && beam_energy < 6.5){
						dHist_f1_1285_beam_6_high[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 6.5 && beam_energy < 7.5){
						dHist_f1_1285_beam_7_high[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 7.5 && beam_energy < 8.5){
						dHist_f1_1285_beam_8_high[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 8.5 && beam_energy < 9.5){
						dHist_f1_1285_beam_9_high[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
					if(beam_energy > 9.5 && beam_energy < 10.5){
						dHist_f1_1285_beam_10_high[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
					}
				}
			//} uncomment to cut out the k*0

			// if(minus_t < 2){
			// 	// dHist_IM_KsKmPip_binned_full[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 	dHist_W_vs_IM_KsKmPip->Fill(im_kskmpip, w, locHistAccidWeightFactor);
			// 	if(minus_t<=1){
			// 		t_index = minus_t / 0.1;
			// 		dHist_IM_KsKmPip_binned_full_low[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 	}
			// 	else{
			// 		t_index
			// 		dHist_IM_KsKmPip_binned_full_high[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);

			// 	}
			// }

			// // if(minus_t < 1 && beam_energy >= 8.2 && beam_energy <= 8.8){
			// // 	dHist_IM_KsKmPip_binned[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// // }

			// // if((im_kmpip > 0.8 && im_kmpip < 1.0 && im_kspip < 0.8 && im_kspip > 1.0)
			// // || (im_kmpip < 0.8 && im_kmpip > 1.0 && im_kspip > 0.8 && im_kspip < 1.0)){
			// // 	dHist_IM_KsKmPip_1420->Fill(im_kskmpip, locHistAccidWeightFactor);
			// // 	if(minus_t < 1 && beam_energy >= 8.2 && beam_energy <= 8.8){
			// // 		dHist_IM_KsKmPip_1420_binned[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// // 	}

			// }else if((im_kmpip < 0.8 || im_kmpip > 1.0) && (im_kspip < 0.8 || im_kspip > 1.0)){
			// 	dHist_IM_KsKmPip_1285->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 	dHist_MinusT->Fill(minus_t);
			// 	// if(beam_energy > 7.0 && beam_energy < 7.5){
			// 	// 	dHist_IM_KsKmPip_vs_t_70_75->Fill(im_kskmpip, minus_t, locHistAccidWeightFactor);
			// 	// }
			// 	// else if(beam_energy > 7.5 && beam_energy < 8.0){
			// 	// 	dHist_IM_KsKmPip_vs_t_75_80->Fill(im_kskmpip, minus_t, locHistAccidWeightFactor);
			// 	// }
			// 	// else if(beam_energy > 8.0 && beam_energy < 8.5){
			// 	// 	dHist_IM_KsKmPip_vs_t_80_85->Fill(im_kskmpip, minus_t, locHistAccidWeightFactor);
			// 	// }
			// 	// else if(beam_energy > 8.5 && beam_energy < 9.0){
			// 	// 	dHist_IM_KsKmPip_vs_t_85_90->Fill(im_kskmpip, minus_t, locHistAccidWeightFactor);
			// 	// }
				
			// 	if(w > 3.3 && w < 4.7){
			// 		dHist_W_binned_f1[w_index]->Fill(im_kskmpip);
			// 		if(im_kskmpip < 1.45){
			// 			dHist_CosThetaCM[w_index]->Fill(cosThetaCM);
			// 		}
			// 	}

			// 	if(minus_t < 2){
			// 		dHist_f1_1285_binned_full[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);

			// 		if(beam_energy > 6.5 && beam_energy < 7.5){
			// 			dHist_f1_1285_beam_7[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 		}
			// 		if(beam_energy > 7.5 && beam_energy < 8.5){
			// 			dHist_f1_1285_beam_8[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 		}if(beam_energy > 8.5 && beam_energy < 9.5){
			// 			dHist_f1_1285_beam_9[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 		}if(beam_energy > 9.5 && beam_energy < 10.5){
			// 			dHist_f1_1285_beam_10[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 		}
			// 	}
				
			// 	if(beam_energy >= 8.2 && beam_energy <= 8.8){
			// 		dHist_IM_KsKmPip_vs_t_82_88->Fill(im_kskmpip, minus_t, locHistAccidWeightFactor);
			// 		if(minus_t < 1 ){
			// 				dHist_IM_KsKmPip_1285_binned[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
							
			// 				if(!dAnalysisUtilities.Get_PolarizationAngle(locRunNumber,  polAngle)){
			// 					cerr<<"whoops!"<<endl;
			// 					continue;
			// 				}
			// 				if(polAngle == 0){
			// 					if(im_kskmpip < 1.45){
			// 						dHist_Phi0_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
			// 					}else{
			// 						dHist_Phi0_background_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
			// 					}
			// 					dHist_f1_0_1285[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 				}
			// 				else if(polAngle == 90){
			// 					if(im_kskmpip < 1.45){
			// 						dHist_Phi90_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
			// 					}else{
			// 						dHist_Phi90_background_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
			// 					}
			// 					dHist_f1_90_1285[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 				}
			// 				else if(polAngle == 45){
			// 					if(im_kskmpip < 1.45){
			// 						dHist_Phi45_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
			// 					}else{
			// 						dHist_Phi45_background_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
			// 					}
			// 					dHist_f1_45_1285[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 				}
			// 				else if(polAngle == 135){
			// 					if(im_kskmpip< 1.45){
			// 						dHist_Phi135_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
			// 					}else{
			// 						dHist_Phi135_background_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
			// 					}
			// 					dHist_f1_135_1285[t_index]->Fill(im_kskmpip, locHistAccidWeightFactor);
			// 				}
			// 		}
				
			// 	}
		
		}


		// if(locUsedSoFar_IM_KsKpPim.find(locUsedThisCombo_IM_KsKpPim) == locUsedSoFar_IM_KsKpPim.end()){
		// 	dHist_Pim1P_vs_KsKpPim->Fill(im_kskppim, im_ppim, locHistAccidWeightFactor);
		// 	// dHist_KpP_KsKpPim->Fill(im_kskppim, im_kpp, locHistAccidWeightFactor);
		// 	dHist_DOCA_vs_IM_KsKpPim->Fill(im_kskppim, vertex_distance_Ks, locHistAccidWeightFactor);
		// 	dHist_CosTheta_vs_IM_KsKpPim->Fill(im_kskppim, cos_theta_col, locHistAccidWeightFactor);
		// 	dHist_IM_KsKpPim->Fill(im_kskppim, locHistAccidWeightFactor);
		// 	dHist_IM_KsKpPim_vs_t_82_88->Fill(im_kskppim, minus_t, locHistAccidWeightFactor);
		// 	dHist_TMin->Fill(tmin);

		// 	if(tprime < 3){
		// 		dHist_f1_1285_tmin[tprime_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 	}

		// 	if(minus_t < 2){
		// 		dHist_IM_KsKmPip_binned_full[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
				
		// 	}

		// 	if(minus_t < 1 && beam_energy >= 8.2 && beam_energy <= 8.8){
		// 		dHist_IM_KsKpPim_binned[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 	}

		// 	if(im_kspim < 0.8 || im_kspim > 1.0){//im_kppim > 0.8 && im_kppim < 1.0){
		// 		dHist_IM_KsKpPim_1285->Fill(im_kskppim, locHistAccidWeightFactor);

		// 		if(minus_t < 2){
		// 			dHist_f1_1285_binned_full[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			if(beam_energy > 6.5 && beam_energy < 7.5){
		// 				dHist_f1_1285_beam_7[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			}
		// 			if(beam_energy > 7.5 && beam_energy < 8.5){
		// 				dHist_f1_1285_beam_8[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			}if(beam_energy > 8.5 && beam_energy < 9.5){
		// 				dHist_f1_1285_beam_9[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			}if(beam_energy > 9.5 && beam_energy < 10.5){
		// 				dHist_f1_1285_beam_10[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			}
		// 		}

		// 		if(w > 3.3 && w < 4.7){
		// 			dHist_W_binned_f1[w_index]->Fill(im_kskppim);
		// 			if(im_kskppim < 1.45){
		// 				dHist_CosThetaCM[w_index]->Fill(cosThetaCM);
		// 			}
		// 		}

		// 		if(minus_t < 1 && beam_energy >= 8.2 && beam_energy <= 8.8){
		// 			dHist_IM_KsKpPim_1285_binned[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			if(!dAnalysisUtilities.Get_PolarizationAngle(locRunNumber,  polAngle)){
		// 				cerr<<"whoops!"<<endl;
		// 				continue;
		// 			}
		// 			if(polAngle == 0){
		// 				if(im_kskppim < 1.4){
		// 					dHist_Phi0_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
		// 				}else{
		// 					dHist_Phi0_background_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
		// 				}
		// 				dHist_f1_0_1285[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			}
		// 			else if(polAngle == 90){
		// 				if(im_kskppim < 1.4){
		// 					dHist_Phi90_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
		// 				}else{
		// 					dHist_Phi90_background_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
		// 				}
		// 				dHist_f1_90_1285[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			}
		// 			else if(polAngle == 45){
		// 				if(im_kskppim < 1.4){
		// 					dHist_Phi45_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
		// 				}else{
		// 					dHist_Phi45_background_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
		// 				}
		// 				dHist_f1_45_1285[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			}
		// 			else if(polAngle == 135){
		// 				if(im_kskppim < 1.4){
		// 					dHist_Phi135_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
		// 				}else{
		// 					dHist_Phi135_background_1285[t_index]->Fill(f1_phi, locHistAccidWeightFactor);
		// 				}
		// 				dHist_f1_135_1285[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			}
		// 		}

		// 	}else if(im_kspim > 0.8 && im_kspim < 1.0){
		// 		dHist_IM_KsKpPim_1420->Fill(im_kskppim, locHistAccidWeightFactor);
		// 		// if(beam_energy > 7.0 && beam_energy < 7.5){
		// 		// 	dHist_IM_KsKmPip_vs_t_70_75->Fill(im_kskmpip, minus_t, locHistAccidWeightFactor);
		// 		// }
		// 		// else if(beam_energy > 7.5 && beam_energy < 8.0){
		// 		// 	dHist_IM_KsKmPip_vs_t_75_80->Fill(im_kskmpip, minus_t, locHistAccidWeightFactor);
		// 		// }
		// 		// else if(beam_energy > 8.0 && beam_energy < 8.5){
		// 		// 	dHist_IM_KsKmPip_vs_t_80_85->Fill(im_kskmpip, minus_t, locHistAccidWeightFactor);
		// 		// }
		// 		// else if(beam_energy > 8.5 && beam_energy < 9.0){
		// 		// 	dHist_IM_KsKmPip_vs_t_85_90->Fill(im_kskmpip, minus_t, locHistAccidWeightFactor);
		// 		// }
				
		// 		if(beam_energy >= 8.2 && beam_energy <= 8.8){
		// 			if(minus_t < 1 ){
		// 					dHist_IM_KsKpPim_1420_binned[t_index]->Fill(im_kskppim, locHistAccidWeightFactor);
		// 			}
				
		// 		}
		// 	}

		// 	locUsedSoFar_IM_KsKpPim.insert(locUsedThisCombo_IM_KsKpPim);
		// }

			dFlatTreeInterface->Fill_Fundamental<Double_t>("e_beam", locBeamP4.E()); //fundamental = char, int, float, double, etc.
			dFlatTreeInterface->Fill_Fundamental<Double_t>("minus_t", minus_t); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("tmin", tmin); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("accidental_weight", locHistAccidWeightFactor); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("kstar_m", im_kppim);  
			dFlatTreeInterface->Fill_Fundamental<Double_t>("pimkpks_e", locKsKpPim.E()); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("pimkpks_px", locKsKpPim.Px()); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("pimkpks_py", locKsKpPim.Py()); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("pimkpks_pz", locKsKpPim.Pz()); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("pimkpks_phi", f1_phi); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("pimkpks_theta", f1_theta);
			dFlatTreeInterface->Fill_Fundamental<Double_t>("p_e", locProtonP4.E()); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("p_px", locProtonP4.Px()); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("p_py", locProtonP4.Py()); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("p_pz", locProtonP4.Pz()); 
			dFlatTreeInterface->Fill_Fundamental<Double_t>("w", w);  

		// if(im_kskmpip < 1.5){
		// 	dComboWrapper->Set_IsComboCut(true);

		// 	continue;
		// }

		// double im_pks = locPKs.M();

		// set<Int_t> locUsedThisCombo_IM_PKs;
		// locUsedThisCombo_IM_KsPip.insert(locPiPlus1TrackID);
		// locUsedThisCombo_IM_KsPip.insert(locProtonTrackID);
		// locUsedThisCombo_IM_KsPip.insert(locPiMinusTrackID);

		// if(locUsedSoFar_IM_PKs.find(locUsedThisCombo_IM_PKs) == locUsedSoFar_IM_PKs.end()){
		// 	dHist_IM_PKs->Fill(im_pks);
		// 	locUsedSoFar_IM_PKs.insert(locUsedThisCombo_IM_PKs);
		// }


		/****************************************** FILL FLAT TREE (IF DESIRED) ******************************************/

		/*
		//FILL ANY CUSTOM BRANCHES FIRST!!
		Int_t locMyInt_Flat = 7;
		dFlatTreeInterface->Fill_Fundamental<Int_t>("flat_my_int", locMyInt_Flat);

		TLorentzVector locMyP4_Flat(4.0, 3.0, 2.0, 1.0);
		dFlatTreeInterface->Fill_TObject<TLorentzVector>("flat_my_p4", locMyP4_Flat);

		for(int loc_j = 0; loc_j < locMyInt_Flat; ++loc_j)
		{
			dFlatTreeInterface->Fill_Fundamental<Int_t>("flat_my_int_array", 3*loc_j, loc_j); //2nd argument = value, 3rd = array index
			TLorentzVector locMyComboP4_Flat(8.0, 7.0, 6.0, 5.0);
			dFlatTreeInterface->Fill_TObject<TLorentzVector>("flat_my_p4_array", locMyComboP4_Flat, loc_j);
		}
		*/

		//FILL FLAT TREE
		Fill_FlatTree(); //for the active combo
	} // end of combo loop

	//FILL HISTOGRAMS: Num combos / events surviving actions
	Fill_NumCombosSurvivedHists();

	/******************************************* LOOP OVER THROWN DATA (OPTIONAL) ***************************************/
/*
	//Thrown beam: just use directly
	if(dThrownBeam != NULL)
		double locEnergy = dThrownBeam->Get_P4().E();

	//Loop over throwns
	for(UInt_t loc_i = 0; loc_i < Get_NumThrown(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dThrownWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
	}
*/
	/****************************************** LOOP OVER OTHER ARRAYS (OPTIONAL) ***************************************/
/*
	//Loop over beam particles (note, only those appearing in combos are present)
	for(UInt_t loc_i = 0; loc_i < Get_NumBeam(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dBeamWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
	}

	//Loop over charged track hypotheses
	for(UInt_t loc_i = 0; loc_i < Get_NumChargedHypos(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dChargedHypoWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
	}

	//Loop over neutral particle hypotheses
	for(UInt_t loc_i = 0; loc_i < Get_NumNeutralHypos(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dNeutralHypoWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
	}
*/

	/************************************ EXAMPLE: FILL CLONE OF TTREE HERE WITH CUTS APPLIED ************************************/
/*
	Bool_t locIsEventCut = true;
	for(UInt_t loc_i = 0; loc_i < Get_NumCombos(); ++loc_i) {
		//Set branch array indices for combo and all combo particles
		dComboWrapper->Set_ComboIndex(loc_i);
		// Is used to indicate when combos have been cut
		if(dComboWrapper->Get_IsComboCut())
			continue;
		locIsEventCut = false; // At least one combo succeeded
		break;
	}
	if(!locIsEventCut && dOutputTreeFileName != "")
		Fill_OutputTree();
*/

	return kTRUE;
}

void DSelector_f1_pimkpks::Finalize(void)
{
	//Save anything to output here that you do not want to be in the default DSelector output ROOT file.

	//Otherwise, don't do anything else (especially if you are using PROOF).
		//If you are using PROOF, this function is called on each thread,
		//so anything you do will not have the combined information from the various threads.
		//Besides, it is best-practice to do post-processing (e.g. fitting) separately, in case there is a problem.

	//DO YOUR STUFF HERE

	//CALL THIS LAST
	DSelector::Finalize(); //Saves results to the output file
}
