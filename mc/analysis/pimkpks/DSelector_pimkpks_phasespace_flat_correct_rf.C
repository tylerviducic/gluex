#include "DSelector_pimkpks_phasespace_flat_correct_rf.h"

void DSelector_pimkpks_phasespace_flat_correct_rf::Init(TTree *locTree)
{
	// USERS: IN THIS FUNCTION, ONLY MODIFY SECTIONS WITH A "USER" OR "EXAMPLE" LABEL. LEAVE THE REST ALONE.

	// The Init() function is called when the selector needs to initialize a new tree or chain.
	// Typically here the branch addresses and branch pointers of the tree will be set.
	// Init() will be called many times when running on PROOF (once per file to be processed).

	//USERS: SET OUTPUT FILE NAME //can be overriden by user in PROOF
	dOutputFileName = ""; //"" for none
	dOutputTreeFileName = ""; //"" for none
	dFlatTreeFileName = "/work/halld/home/viducic/data/pimkpks/mc/phasespace/pimkpks_flat_bestX2.root"; // output flat tree (one combo per tree entry), "" for none
	dFlatTreeName = ""; //if blank, default name will be chosen
	//dSaveDefaultFlatBranches = true; // False: don't save default branches, reduce disk footprint.
	//dSaveTLorentzVectorsAsFundamentaFlatTree = false; // Default (or false): save particles as TLorentzVector objects. True: save as four doubles instead.

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
	dHist_MissingMassSquared = new TH1I("MissingMassSquared", ";Missing Mass Squared (GeV/c^{2})^{2}", 600, -0.06, 0.06);
	dHist_BeamEnergy = new TH1I("BeamEnergy", ";Beam Energy (GeV)", 600, 0.0, 12.0);

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

	// RECOMMENDED: CREATE ACCIDENTAL WEIGHT BRANCH
	// dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("accidweight");

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

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("e_beam"); // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("rf_time"); //fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kinfit_cl"); //fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_px"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_py"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_pz"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_E");	// fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_px"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_py"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_pz"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_E");	// fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_px"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_py"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_pz"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_E");  // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_px"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_py"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_pz"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_E");  // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_px"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_py"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_pz"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_E");	 // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_px_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_py_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_pz_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_E_measured");	 // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_px_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_py_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_pz_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_E_measured");	 // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_px_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_py_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_pz_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_E_measured");	// fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_px_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_py_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_pz_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_E_measured");  // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_px_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_py_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_pz_measured"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_E_measured");  // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_px_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_py_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_pz_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim1_E_thrown");  // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_px_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_py_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_pz_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim2_E_thrown");  // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_px_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_py_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_pz_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip_E_thrown");  // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_px_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_py_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_pz_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_E_thrown");	 // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_px_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_py_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_pz_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_E_thrown");	 // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_px_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_py_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_pz_thrown"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("p_E_thrown");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pathlength_sig"); // fundamental = char, int, float, double, etc.

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mand_t"); // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("w");	   // fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("s");

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

Bool_t DSelector_pimkpks_phasespace_flat_correct_rf::Process(Long64_t locEntry)
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
	double best_chi2 = 100000000;
	int best_combo = -1;
	//Loop over combos
	for(UInt_t loc_i = 0; loc_i < Get_NumCombos(); ++loc_i)
	{
		//Set branch array indices for combo and all combo particles
		dComboWrapper->Set_ComboIndex(loc_i);

		// Is used to indicate when combos have been cut
		if(dComboWrapper->Get_IsComboCut()) // Is false when tree originally created
			continue; // Combo has been cut previously

	/********************************************* GET COMBO RF TIMING INFO *****************************************/

	TLorentzVector locBeamX4_Measured = dComboBeamWrapper->Get_X4_Measured();
	TLorentzVector locBeamP4 = dComboBeamWrapper->Get_P4();
	Double_t locBunchPeriod = dAnalysisUtilities.Get_BeamBunchPeriod(Get_RunNumber());
	Double_t locDeltaT_RF = dAnalysisUtilities.Get_DeltaT_RF(Get_RunNumber(), locBeamX4_Measured, dComboWrapper);
	Int_t locRelBeamBucket = dAnalysisUtilities.Get_RelativeBeamBucket(Get_RunNumber(), locBeamX4_Measured, dComboWrapper); // 0 for in-time events, non-zero integer for out-of-time photons
	Int_t locNumOutOfTimeBunchesInTree = 4;																					// YOU need to specify this number
																															// Number of out-of-time beam bunches in tree (on a single side, so that total number out-of-time bunches accepted is 2 times this number for left + right bunches)

	Bool_t locSkipNearestOutOfTimeBunch = true; // True: skip events from nearest out-of-time bunch on either side (recommended).
	Int_t locNumOutOfTimeBunchesToUse = locSkipNearestOutOfTimeBunch ? locNumOutOfTimeBunchesInTree - 1 : locNumOutOfTimeBunchesInTree;
	Double_t locAccidentalScalingFactor = dAnalysisUtilities.Get_AccidentalScalingFactor(Get_RunNumber(), locBeamP4.E(), dIsMC);	 // Ideal value would be 1, but deviations require added factor, which is different for data and MC.
	Double_t locAccidentalScalingFactorError = dAnalysisUtilities.Get_AccidentalScalingFactorError(Get_RunNumber(), locBeamP4.E());	 // Ideal value would be 1, but deviations observed, need added factor.
	Double_t locHistAccidWeightFactor = locRelBeamBucket == 0 ? 1 : -locAccidentalScalingFactor / (2 * locNumOutOfTimeBunchesToUse); // Weight by 1 for in-time events, ScalingFactor*(1/NBunches) for out-of-time
	// if(locSkipNearestOutOfTimeBunch && abs(locRelBeamBucket)==0) { // Skip nearest out-of-time bunch: tails of in-time distribution also leak in
	// 	dComboWrapper->Set_IsComboCut(true);
	// 	continue;
	// }
	if (locRelBeamBucket != 0)
		{ // Skip nearest out-of-time bunch: tails of in-time distribution also leak in
			dComboWrapper->Set_IsComboCut(true);
			continue;
		}

	// Grab combo Chi^2/NDF and see if it's the best.
	// If it is, save the combo index

	double chi2 = dComboWrapper->Get_ChiSq_KinFit();
	double ndf = dComboWrapper->Get_NDF_KinFit();

	if (chi2 / ndf <= best_chi2)
		{
			best_chi2 = chi2 / ndf;
			best_combo = loc_i;
		}
	}
if (best_combo == -1)
{
	return kTRUE;
}

dComboWrapper->Set_ComboIndex(best_combo);

double locKinFit_CL = dComboWrapper->Get_ConfidenceLevel_KinFit("");

// if (locKinFit_CL < 1E-3)
// {
// 	dComboWrapper->Set_IsComboCut(true);
// 	return kTRUE;
// }

double chi2 = dComboWrapper->Get_ChiSq_KinFit();
double ndf = dComboWrapper->Get_NDF_KinFit();

if (chi2 / ndf > 20)
{
	dComboWrapper->Set_IsComboCut(true);
	return kTRUE;
}
		/********************************************** GET PARTICLE INDICES *********************************************/

		//Used for tracking uniqueness when filling histograms, and for determining unused particles

		//Step 0
		Int_t locBeamID = dComboBeamWrapper->Get_BeamID();
		Int_t locPiMinus1TrackID = dPiMinus1Wrapper->Get_TrackID();
		Int_t locKPlusTrackID = dKPlusWrapper->Get_TrackID();
		Int_t locProtonTrackID = dProtonWrapper->Get_TrackID();

		//Step 1
		Int_t locPiPlusTrackID = dPiPlusWrapper->Get_TrackID();
		Int_t locPiMinus2TrackID = dPiMinus2Wrapper->Get_TrackID();

		/*********************************************** GET FOUR-MOMENTUM **********************************************/

		// Get P4's: //is kinfit if kinfit performed, else is measured
		//dTargetP4 is target p4
		//Step 0
		TLorentzVector locBeamP4 = dComboBeamWrapper->Get_P4();
		TLorentzVector locPiMinus1P4 = dPiMinus1Wrapper->Get_P4();
		TLorentzVector locKPlusP4 = dKPlusWrapper->Get_P4();
		TLorentzVector locProtonP4 = dProtonWrapper->Get_P4();
		//Step 1
		TLorentzVector locPiPlusP4 = dPiPlusWrapper->Get_P4();
		TLorentzVector locPiMinus2P4 = dPiMinus2Wrapper->Get_P4();

		// Get Measured P4's:
		//Step 0
		TLorentzVector locBeamP4_Measured = dComboBeamWrapper->Get_P4_Measured();
		TLorentzVector locPiMinus1P4_Measured = dPiMinus1Wrapper->Get_P4_Measured();
		TLorentzVector locKPlusP4_Measured = dKPlusWrapper->Get_P4_Measured();
		TLorentzVector locProtonP4_Measured = dProtonWrapper->Get_P4_Measured();
		//Step 1
		TLorentzVector locPiPlusP4_Measured = dPiPlusWrapper->Get_P4_Measured();
		TLorentzVector locPiMinus2P4_Measured = dPiMinus2Wrapper->Get_P4_Measured();

		/*********************************************** GET X4's **********************************************/

		// Step 0
		TLorentzVector locBeamX4 = dComboBeamWrapper->Get_X4();
		TLorentzVector locPiMinus1X4 = dPiMinus1Wrapper->Get_X4();
		TLorentzVector locKPlusX4 = dKPlusWrapper->Get_X4();
		TLorentzVector locProtonX4 = dProtonWrapper->Get_X4();
		// Step 1
		TLorentzVector locPiPlusX4 = dPiPlusWrapper->Get_X4();
		TLorentzVector locPiMinus2X4 = dPiMinus2Wrapper->Get_X4();

		// Get Measured X4's:
		// Step 0
		// TLorentzVector locBeamX4_Measured = dComboBeamWrapper->Get_X4_Measured();
		TLorentzVector locPiMinus1X4_Measured = dPiMinus1Wrapper->Get_X4_Measured();
		TLorentzVector locKPlusX4_Measured = dKPlusWrapper->Get_X4_Measured();
		TLorentzVector locProtonX4_Measured = dProtonWrapper->Get_X4_Measured();
		// Step 1
		TLorentzVector locPiPlusX4_Measured = dPiPlusWrapper->Get_X4_Measured();
		TLorentzVector locPiMinus2X4_Measured = dPiMinus2Wrapper->Get_X4_Measured();

		// FLIGHT SIGNIFIGANCE CALCULATIONS
		TLorentzVector locProdSpacetimeVertex = dComboBeamWrapper->Get_X4();
		TLorentzVector locDecayingKShortX4 = dTreeInterface->Get_TObject<TLorentzVector>("DecayingKShort__X4", best_combo);
		TLorentzVector locDeltaSpacetimeKs = locProdSpacetimeVertex - locDecayingKShortX4;
		double locPathLengthKs = locDeltaSpacetimeKs.Vect().Mag();
		float locPathLengthSigmaKs = Get_Fundamental<Float_t>("DecayingKShort__PathLengthSigma", best_combo);
		double locPathLengthSignificanceKs = locPathLengthKs / locPathLengthSigmaKs;		

		/********************************************* GET COMBO RF TIMING INFO *****************************************/

		// TLorentzVector locBeamX4_Measured = dComboBeamWrapper->Get_X4_Measured();
		//Double_t locBunchPeriod = dAnalysisUtilities.Get_BeamBunchPeriod(Get_RunNumber());
		// Double_t locDeltaT_RF = dAnalysisUtilities.Get_DeltaT_RF(Get_RunNumber(), locBeamX4_Measured, dComboWrapper);
		// Int_t locRelBeamBucket = dAnalysisUtilities.Get_RelativeBeamBucket(Get_RunNumber(), locBeamX4_Measured, dComboWrapper); // 0 for in-time events, non-zero integer for out-of-time photons
		// Int_t locNumOutOfTimeBunchesInTree = XXX; //YOU need to specify this number
			//Number of out-of-time beam bunches in tree (on a single side, so that total number out-of-time bunches accepted is 2 times this number for left + right bunches) 

		// Bool_t locSkipNearestOutOfTimeBunch = true; // True: skip events from nearest out-of-time bunch on either side (recommended).
		// Int_t locNumOutOfTimeBunchesToUse = locSkipNearestOutOfTimeBunch ? locNumOutOfTimeBunchesInTree-1:locNumOutOfTimeBunchesInTree; 
		// Double_t locAccidentalScalingFactor = dAnalysisUtilities.Get_AccidentalScalingFactor(Get_RunNumber(), locBeamP4.E(), dIsMC); // Ideal value would be 1, but deviations require added factor, which is different for data and MC.
		// Double_t locAccidentalScalingFactorError = dAnalysisUtilities.Get_AccidentalScalingFactorError(Get_RunNumber(), locBeamP4.E()); // Ideal value would be 1, but deviations observed, need added factor.
		// Double_t locHistAccidWeightFactor = locRelBeamBucket==0 ? 1 : -locAccidentalScalingFactor/(2*locNumOutOfTimeBunchesToUse) ; // Weight by 1 for in-time events, ScalingFactor*(1/NBunches) for out-of-time
		// if(locSkipNearestOutOfTimeBunch && abs(locRelBeamBucket)==1) { // Skip nearest out-of-time bunch: tails of in-time distribution also leak in
		// 	dComboWrapper->Set_IsComboCut(true); 
		// 	continue; 
		// } 

		/********************************************* COMBINE FOUR-MOMENTUM ********************************************/

		// DO YOUR STUFF HERE

		// Combine 4-vectors
		TLorentzVector locMissingP4_Measured = locBeamP4_Measured + dTargetP4;
		locMissingP4_Measured -= locPiMinus1P4_Measured + locKPlusP4_Measured + locProtonP4_Measured + locPiPlusP4_Measured + locPiMinus2P4_Measured;

		/******************************************** EXECUTE ANALYSIS ACTIONS *******************************************/

		// Loop through the analysis actions, executing them in order for the active particle combo
		dAnalyzeCutActions->Perform_Action(); // Must be executed before Execute_Actions()
		if(!Execute_Actions()) //if the active combo fails a cut, IsComboCutFlag automatically set
			return kTRUE;

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
		locUsedThisCombo_MissingMass[PiMinus].insert(locPiMinus1TrackID);
		locUsedThisCombo_MissingMass[KPlus].insert(locKPlusTrackID);
		locUsedThisCombo_MissingMass[Proton].insert(locProtonTrackID);
		locUsedThisCombo_MissingMass[PiPlus].insert(locPiPlusTrackID);
		locUsedThisCombo_MissingMass[PiMinus].insert(locPiMinus2TrackID);

		//compare to what's been used so far
		if(locUsedSoFar_MissingMass.find(locUsedThisCombo_MissingMass) == locUsedSoFar_MissingMass.end())
		{
			//unique missing mass combo: histogram it, and register this combo of particles
			dHist_MissingMassSquared->Fill(locMissingMassSquared); // Fills in-time and out-of-time beam photon combos
			//dHist_MissingMassSquared->Fill(locMissingMassSquared,locHistAccidWeightFactor); // Alternate version with accidental subtraction

			locUsedSoFar_MissingMass.insert(locUsedThisCombo_MissingMass);
		}

		//E.g. Cut
		//if((locMissingMassSquared < -0.04) || (locMissingMassSquared > 0.04))
		//{
		//	dComboWrapper->Set_IsComboCut(true);
		//	continue;
		//}

		double minus_t = -1 * (dTargetP4 - locProtonP4_Measured).M2();
		double w = (locBeamP4_Measured + dTargetP4).M();
		double s = w * w;
		/****************************************** FILL FLAT TREE (IF DESIRED) ******************************************/

		// RECOMMENDED: FILL ACCIDENTAL WEIGHT
		// dFlatTreeInterface->Fill_Fundamental<Double_t>("accidweight",locHistAccidWeightFactor);

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

		dFlatTreeInterface->Fill_Fundamental<Double_t>("e_beam", locBeamP4.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("rf_time", dComboWrapper->Get_RFTime()); 
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kinfit_cl", locKinFit_CL); 

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_px", locPiMinus1P4.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_py", locPiMinus1P4.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_pz", locPiMinus1P4.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_E", locPiMinus1P4.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_px", locPiMinus2P4.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_py", locPiMinus2P4.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_pz", locPiMinus2P4.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_E", locPiMinus2P4.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_px", locPiPlusP4.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_py", locPiPlusP4.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_pz", locPiPlusP4.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_E", locPiPlusP4.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_px", locKPlusP4.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_py", locKPlusP4.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_pz", locKPlusP4.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_E", locKPlusP4.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_px", locProtonP4.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_py", locProtonP4.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_pz", locProtonP4.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_E", locProtonP4.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_py_measured", locPiMinus1P4_Measured.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_px_measured", locPiMinus1P4_Measured.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_pz_measured", locPiMinus1P4_Measured.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_E_measured", locPiMinus1P4_Measured.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_px_measured", locPiMinus2P4_Measured.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_py_measured", locPiMinus2P4_Measured.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_pz_measured", locPiMinus2P4_Measured.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_E_measured", locPiMinus2P4_Measured.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_px_measured", locPiPlusP4_Measured.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_py_measured", locPiPlusP4_Measured.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_pz_measured", locPiPlusP4_Measured.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_E_measured", locPiPlusP4_Measured.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_px_measured", locKPlusP4_Measured.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_py_measured", locKPlusP4_Measured.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_pz_measured", locKPlusP4_Measured.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_E_measured", locKPlusP4_Measured.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_py_measured", locProtonP4_Measured.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_px_measured", locProtonP4_Measured.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_pz_measured", locProtonP4_Measured.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_E_measured", locProtonP4_Measured.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pathlength_sig", locPathLengthSignificanceKs);

		dFlatTreeInterface->Fill_Fundamental<Double_t>("mand_t", minus_t);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("w", w);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("s", s);

		if (dThrownBeam != NULL)
			double locEnergy_Thrown = dThrownBeam->Get_P4().E();

		TLorentzVector dTargetP4_Thrown;
		dTargetP4.SetXYZM(0.0, 0.0, 0.0, 0.938);

		TLorentzVector locProtonP4_Thrown;
		TLorentzVector locPiMinus1P4_Thrown;
		TLorentzVector locPiPlusP4_Thrown;
		TLorentzVector locPiMinus2P4_Thrown;
		TLorentzVector locKPlusP4_Thrown;
		TLorentzVector locKShortP4_Thrown;

		TLorentzVector PiMinusHypo1_Thrown;
		TLorentzVector PiMinusHypo2_Thrown;
		Int_t KsThrown_Index;

		Bool_t piPlusChecked = false;
		Bool_t firstPiPlus = false;

		// create a vector for potential pi+ candidates indices
		vector<int> piMinusIndices;

		// Loop over throwns
		for (UInt_t loc_i = 0; loc_i < Get_NumThrown(); ++loc_i)
		{
			// 	//Set branch array indices corresponding to this particle
			dThrownWrapper->Set_ArrayIndex(loc_i);

			// 	//Do stuff with the wrapper here ...
			Particle_t locPID_Thrown = dThrownWrapper->Get_PID();
			TLorentzVector locThrownP4 = dThrownWrapper->Get_P4();
			// cout << "Thrown " << loc_i << ": " << locPID << ", " << locThrownP4.Px() << ", " << locThrownP4.Py() << ", " << locThrownP4.Pz() << ", " << locThrownP4.E() << endl;

			if (locPID_Thrown == 11)
			{
			locKPlusP4_Thrown = locThrownP4;
			}
			if (locPID_Thrown == 14)
			{
			locProtonP4_Thrown = locThrownP4;
			}
			if (locPID_Thrown == 8)
			{
			locPiPlusP4_Thrown = locThrownP4;
			}
			if (locPID_Thrown == 16)
			{
			locKShortP4_Thrown = locThrownP4;
			KsThrown_Index = loc_i;
			}
			if (locPID_Thrown == 9)
			{
			if (dThrownWrapper->Get_ParentIndex() < 0)
			{
				locPiMinus1P4_Thrown = locThrownP4;
			}
			else
			{
				piMinusIndices.push_back(loc_i);
			}
			}
		}

		// loop over pion candidate indices and see if it's parent index is equal to the Ks. if it is, make that pion's 4 vector the pi+2
		for (int i = 0; i < piMinusIndices.size(); i++)
		{
			dThrownWrapper->Set_ArrayIndex(piMinusIndices[i]);
			if (dThrownWrapper->Get_ParentIndex() == KsThrown_Index)
			{
			locPiMinus2P4_Thrown = dThrownWrapper->Get_P4();
			}
		}

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_px_thrown", locPiMinus1P4_Thrown.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_py_thrown", locPiMinus1P4_Thrown.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_pz_thrown", locPiMinus1P4_Thrown.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim1_E_thrown", locPiMinus1P4_Thrown.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_px_thrown", locPiMinus2P4_Thrown.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_py_thrown", locPiMinus2P4_Thrown.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_pz_thrown", locPiMinus2P4_Thrown.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim2_E_thrown", locPiMinus2P4_Thrown.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_px_thrown", locPiPlusP4_Thrown.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_py_thrown", locPiPlusP4_Thrown.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_pz_thrown", locPiPlusP4_Thrown.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pip_E_thrown", locPiPlusP4_Thrown.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_px_thrown", locKPlusP4_Thrown.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_py_thrown", locKPlusP4_Thrown.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_pz_thrown", locKPlusP4_Thrown.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_E_thrown", locKPlusP4_Thrown.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_px_thrown", locKShortP4_Thrown.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_py_thrown", locKShortP4_Thrown.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_pz_thrown", locKShortP4_Thrown.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_E_thrown", locKShortP4_Thrown.E());

		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_px_thrown", locProtonP4_Thrown.Px());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_py_thrown", locProtonP4_Thrown.Py());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_pz_thrown", locProtonP4_Thrown.Pz());
		dFlatTreeInterface->Fill_Fundamental<Double_t>("p_E_thrown", locProtonP4_Thrown.E());

		//FILL FLAT TREE
		Fill_FlatTree(); //for the active combo
	//} // end of combo loop

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

void DSelector_pimkpks_phasespace_flat_correct_rf::Finalize(void)
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
