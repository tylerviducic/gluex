#include "DSelector_pq.h"

void DSelector_pq::Init(TTree *locTree)
{
	// USERS: IN THIS FUNCTION, ONLY MODIFY SECTIONS WITH A "USER" OR "EXAMPLE" LABEL. LEAVE THE REST ALONE.

	// The Init() function is called when the selector needs to initialize a new tree or chain.
	// Typically here the branch addresses and branch pointers of the tree will be set.
	// Init() will be called many times when running on PROOF (once per file to be processed).

	//USERS: SET OUTPUT FILE NAME //can be overriden by user in PROOF
	dOutputFileName = "pq.root"; //"" for none
	dOutputTreeFileName = ""; //"" for none
	dFlatTreeFileName = ""; //output flat tree (one combo per tree entry), "" for none
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
	dHist_IM_Pip2Pim = new TH1F("IM_PipPim", ";IM(pi+ pi-) GeV", 300, 0.3, 0.8);
	dHist_IM_KsKmPip = new TH1F("IM_KsKmPip", ";IM(Ks K- Pi+) GeV", 150, 1, 2.25);
	dHist_IM_Pip1P = new TH1F("IM_Pip1P", ";IM(pi+ p) GeV", 100, 0.8, 1.8);
	dHist_IM_KmP = new TH1F("IM_KmP", ";IM(K- p) GeV", 100, 1.0, 2.5);
	dHist_IM_KsPip = new TH1F("IM_KsPip", ";IM(Ks pi+) GeV", 100, 0, 1.5);
	dHist_IM_KmPip = new TH1F("IM_KmPip", ";IM(K- pi+) GeV", 100, 0, 1.5); 
	dHist_IM_PKs = new TH1F("IM_PKs", ";IM(p Ks) GeV", 200, 1.4, 1.8);
	dHist_W = new TH1F("W", ";W (Gev)", 100, 3, 5);
	dHist_MinusT = new TH1F("MinusT", ";-t GeV^2", 100, 0, 10);
	dHist_TMin = new TH1F("TMin", "tmin GeV^2", 100, 0, 10); 
	dHist_KmKs = new TH1F("KmKs", "M(Ks K-)", 150, 0.5, 2.0);
	dHist_KsP = new TH1F("KsP", "M(Ks P)", 150, 1, 2.5);

	dHist_Ks_vs_FlightSig = new TH2F("Ks_vs_FlightSig", ";M(Ks) vs Flight Signifigance", 100, 0.3, 0.8, 100, 0, 10);
	dHist_Pip1P_vs_KsKmPip = new TH2F("Pip1P_vs_KsKmPip", ";IM(Ks K- Pi+) vs IM(pi+ p) GeV", 100, 1, 3.5, 70, 1.0, 2.5);
	dHist_KmP_KsKmPip = new TH2F("KmP_KsKmPip", ";IM(K- p) vs IM(Ks K- Pi+) GeV", 200, 0, 3.5, 100, 1.0, 2.5);
	dHist_DOCA_vs_IM_PipPim = new TH2F("DOCA_vs_IM_PipPim", ";DOCA vs IM(pi+ pi-)", 300, 0.3, 0.8, 100, 0, 20);
	dHist_DOCA_vs_IM_KsKmPip = new TH2F("DOCA_vs_IM_KsKmPip", ";DOCA vs IM(Ks K- pi+)", 200, 0.0, 3.5, 100, 0, 20);
	dHist_CosTheta_vs_IM_PipPim = new TH2F("CosTheta_vs_IM_PipPim", ";CosTheta vs IM(pi+ pi-)", 300, 0.3, 0.8, 100, 0.9, 1.0);
	dHist_CosTheta_vs_IM_KsKmPip = new TH2F("CosTheta_vs_IM_KsKmPip", ";CosTheta vs IM(Ks K- pi+)", 200, 0.0, 3.5, 100, 0.9, 1.0);
	dHist_W_vs_IM_KsKmPip = new TH2F("W_vs_IM_KsKmPip", "W vs IM(Ks K- pi+)", 150, 1.0, 2.2, 100, 3, 5);
	dHist_KmP_KsP = new TH2F("Kpm_KsP", "M(KmP) vs M(KsP)", 150, 1, 2.5, 150, 1, 2.5);


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

Bool_t DSelector_pq::Process(Long64_t locEntry)
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
	set<set<Int_t> > locUsedSoFar_IM_Pip2Pim;
	set<set<Int_t> > locUsedSoFar_Im_Pip1P;
	set<set<Int_t> > locUsedSoFar_IM_KsKmPip;
	set<set<Int_t> > locUsedSoFar_IM_KsPip;
	set<set<Int_t> > locUsedSoFar_IM_KmP;
	set<set<Int_t> > locUsedSoFar_IM_KmPip;
	set<set<Int_t> > locUsedSoFar_IM_PKs;
	set<set<Int_t> > locUsedSoFar_PKmKs;
	set<set<Int_t> > locUsedSoFar_KmKs;
	set<set<Int_t> > locUsedSoFar_KsP;
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
		//Set branch array indices for combo and all combo particles
		dComboWrapper->Set_ComboIndex(loc_i);

		// Is used to indicate when combos have been cut
		if(dComboWrapper->Get_IsComboCut()) // Is false when tree originally created
			continue; // Combo has been cut previously

		/********************************************** GET PARTICLE INDICES *********************************************/

		//Used for tracking uniqueness when filling histograms, and for determining unused particles

		//Step 0
		Int_t locBeamID = dComboBeamWrapper->Get_BeamID();
		Int_t locPiPlus1TrackID = dPiPlus1Wrapper->Get_TrackID();
		Int_t locKMinusTrackID = dKMinusWrapper->Get_TrackID();
		Int_t locProtonTrackID = dProtonWrapper->Get_TrackID();

		//Step 1
		Int_t locPiMinusTrackID = dPiMinusWrapper->Get_TrackID();
		Int_t locPiPlus2TrackID = dPiPlus2Wrapper->Get_TrackID();

		/*********************************************** GET FOUR-MOMENTUM **********************************************/

		// Get P4's: //is kinfit if kinfit performed, else is measured
		//dTargetP4 is target p4
		//Step 0
		TLorentzVector locBeamP4 = dComboBeamWrapper->Get_P4();
		TLorentzVector locPiPlus1P4 = dPiPlus1Wrapper->Get_P4();
		TLorentzVector locKMinusP4 = dKMinusWrapper->Get_P4();
		TLorentzVector locProtonP4 = dProtonWrapper->Get_P4();
		//Step 1
		TLorentzVector locPiMinusP4 = dPiMinusWrapper->Get_P4();
		TLorentzVector locPiPlus2P4 = dPiPlus2Wrapper->Get_P4();

		// Get Measured P4's:
		//Step 0
		TLorentzVector locBeamP4_Measured = dComboBeamWrapper->Get_P4_Measured();
		TLorentzVector locPiPlus1P4_Measured = dPiPlus1Wrapper->Get_P4_Measured();
		TLorentzVector locKMinusP4_Measured = dKMinusWrapper->Get_P4_Measured();
		TLorentzVector locProtonP4_Measured = dProtonWrapper->Get_P4_Measured();
		//Step 1
		TLorentzVector locPiMinusP4_Measured = dPiMinusWrapper->Get_P4_Measured();
		TLorentzVector locPiPlus2P4_Measured = dPiPlus2Wrapper->Get_P4_Measured();

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

		/********************************************* COMBINE FOUR-MOMENTUM ********************************************/

		// DO YOUR STUFF HERE

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

		double locKinFit_CL = dComboWrapper->Get_ConfidenceLevel_KinFit("");

		if(locKinFit_CL < 1E-3){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		// Combine 4-vectors
		TLorentzVector locMissingP4_Measured = locBeamP4_Measured + dTargetP4;
		locMissingP4_Measured -= locPiPlus1P4_Measured + locKMinusP4_Measured + locProtonP4_Measured + locPiMinusP4_Measured + locPiPlus2P4_Measured;
		TLorentzVector locPip1P = locProtonP4 + locPiPlus1P4;
		TLorentzVector locKs = locPiMinusP4 + locPiPlus2P4;
		TLorentzVector locKmP = locKMinusP4 + locProtonP4;
		TLorentzVector locKsKmPip = locKs  + locKMinusP4 + locPiPlus1P4;
		TLorentzVector locKsKm = locKs  + locKMinusP4;
		TLorentzVector locKsPip = locKs + locPiPlus1P4;
		TLorentzVector locKmPip = locKMinusP4 + locPiPlus1P4;
		TLorentzVector locPKs = locKs + locProtonP4;
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
		locUsedThisCombo_MissingMass[PiPlus].insert(locPiPlus1TrackID);
		locUsedThisCombo_MissingMass[KMinus].insert(locKMinusTrackID);
		locUsedThisCombo_MissingMass[Proton].insert(locProtonTrackID);
		locUsedThisCombo_MissingMass[PiMinus].insert(locPiMinusTrackID);
		locUsedThisCombo_MissingMass[PiPlus].insert(locPiPlus2TrackID);

		//compare to what's been used so far
		if(locUsedSoFar_MissingMass.find(locUsedThisCombo_MissingMass) == locUsedSoFar_MissingMass.end())
		{
			//unique missing mass combo: histogram it, and register this combo of particles
			dHist_MissingMassSquared->Fill(locMissingMassSquared); // Fills in-time and out-of-time beam photon combos
			//dHist_MissingMassSquared->Fill(locMissingMassSquared,locHistAccidWeightFactor); // Alternate version with accidental subtraction

			locUsedSoFar_MissingMass.insert(locUsedThisCombo_MissingMass);
		}

		//E.g. Cut
		if((locMissingMassSquared < -0.04) || (locMissingMassSquared > 0.04))
		{
			dComboWrapper->Set_IsComboCut(true);
			continue;
		}


		double im_pip2pim = locKs.M();
		
		set<Int_t> locUsedThisCombo_IM_Pip2Pim;
		locUsedThisCombo_IM_Pip2Pim.insert(locPiMinusTrackID);
		locUsedThisCombo_IM_Pip2Pim.insert(locPiPlus2TrackID);


		// if(locUsedSoFar_IM_Pip2Pim.find(locUsedThisCombo_IM_Pip2Pim) == locUsedSoFar_IM_Pip2Pim.end()){
		// 	dHist_DOCA_vs_IM_PipPim->Fill(im_pip2pim, vertex_distance_Ks, locHistAccidWeightFactor);
		// 	dHist_CosTheta_vs_IM_PipPim->Fill(im_pip2pim, cos_theta_col, locHistAccidWeightFactor);
		dHist_IM_Pip2Pim->Fill(im_pip2pim, locHistAccidWeightFactor);

		if(im_pip2pim > 0.51 || im_pip2pim < 0.49){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		double m_ppip = locPip1P.M();
		double m_pipkm = locKmPip.M();
		double m_pipkmks = locKsKmPip.M();
		double m_kmks = locKsKm.M();
		double m_pkm = locKmP.M();
		double m_ksp = locPKs.M();

		set<Int_t> locUsedThisCombo_kmpip;
		locUsedThisCombo_kmpip.insert(locKMinusTrackID);
		locUsedThisCombo_kmpip.insert(locPiPlus1TrackID);

		if(locUsedSoFar_IM_KmPip.find(locUsedThisCombo_kmpip) == locUsedSoFar_IM_KmPip.end()){
			dHist_IM_KmPip->Fill(m_pipkm, locHistAccidWeightFactor);
			locUsedSoFar_IM_KmPip.insert(locUsedThisCombo_kmpip);
		}

		if(m_pipkm < 0.8 || m_pipkm > 1.0){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}


		set<Int_t> locUsedThisCombo_ppip;
		locUsedThisCombo_ppip.insert(locProtonTrackID);
		locUsedThisCombo_ppip.insert(locPiPlus1TrackID);
		
		if(locUsedSoFar_Im_Pip1P.find(locUsedThisCombo_ppip) == locUsedSoFar_Im_Pip1P.end()){
			dHist_IM_Pip1P->Fill(m_ppip, locHistAccidWeightFactor);
			locUsedSoFar_Im_Pip1P.insert(locUsedThisCombo_ppip);
		}

		// if(m_ppip < 1.4){
		// 	dComboWrapper->Set_IsComboCut(true);

		// 	continue;
		// }

		set<Int_t> locUsedThisCombo_kmks;
		locUsedThisCombo_kmks.insert(locKMinusTrackID);
		locUsedThisCombo_kmks.insert(locPiMinusTrackID);
		locUsedThisCombo_kmks.insert(locPiPlus2TrackID);

		if(locUsedSoFar_KmKs.find(locUsedThisCombo_kmks) == locUsedSoFar_KmKs.end()){
			dHist_KmKs->Fill(m_kmks, locHistAccidWeightFactor);
			locUsedSoFar_KmKs.insert(locUsedThisCombo_kmks);
		}

		// if(m_kmks < 1.43){
		// 	dComboWrapper->Set_IsComboCut(true);

		// 	continue;			
		// }

		set<Int_t> locUsedThisCombo_pipkmks;
		locUsedThisCombo_pipkmks.insert(locKMinusTrackID);
		locUsedThisCombo_pipkmks.insert(locPiMinusTrackID);
		locUsedThisCombo_pipkmks.insert(locPiPlus2TrackID);
		locUsedThisCombo_pipkmks.insert(locPiPlus1TrackID);

		if(locUsedSoFar_IM_KsKmPip.find(locUsedThisCombo_pipkmks) == locUsedSoFar_IM_KsKmPip.end()){
			dHist_IM_KsKmPip->Fill(m_pipkmks, locHistAccidWeightFactor);
			locUsedSoFar_IM_KsKmPip.insert(locUsedThisCombo_pipkmks);
		}

		// if(m_pipkmks < 1.5){
		// 	dComboWrapper->Set_IsComboCut(true);

		// 	continue;
		// }

		set<Int_t> locUsedThisCombo_pkmsks;
		locUsedThisCombo_pkmsks.insert(locKMinusTrackID);
		locUsedThisCombo_pkmsks.insert(locPiMinusTrackID);
		locUsedThisCombo_pkmsks.insert(locPiPlus2TrackID);
		locUsedThisCombo_pkmsks.insert(locProtonTrackID);

		if(locUsedSoFar_PKmKs.find(locUsedThisCombo_pkmsks) == locUsedSoFar_PKmKs.end()){
			dHist_KmP_KsP->Fill(m_ksp, m_pkm, locHistAccidWeightFactor);

			locUsedSoFar_PKmKs.insert(locUsedThisCombo_pkmsks);
		}

		if(m_pkm > 1.5){
			dComboWrapper->Set_IsComboCut(true);

			continue;
		}

		set<Int_t> locUsedThisCombo_KsP;
		locUsedThisCombo_KsP.insert(locPiMinusTrackID);
		locUsedThisCombo_KsP.insert(locPiPlus2TrackID);
		locUsedThisCombo_KsP.insert(locProtonTrackID);
		if(locUsedSoFar_KsP.find(locUsedThisCombo_KsP) == locUsedSoFar_KsP.end()){
			dHist_KsP->Fill(m_ksp, locHistAccidWeightFactor);

			locUsedSoFar_KsP.insert(locUsedThisCombo_KsP);
		}

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
		//Fill_FlatTree(); //for the active combo
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

void DSelector_pq::Finalize(void)
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
