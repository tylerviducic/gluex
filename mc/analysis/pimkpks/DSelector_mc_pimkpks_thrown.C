#include "DSelector_mc_pimkpks_thrown.h"

void DSelector_mc_pimkpks_thrown::Init(TTree *locTree)
{
	// USERS: IN THIS FUNCTION, ONLY MODIFY SECTIONS WITH A "USER" OR "EXAMPLE" LABEL. LEAVE THE REST ALONE.

	// The Init() function is called when the selector needs to initialize a new tree or chain.
	// Typically here the branch addresses and branch pointers of the tree will be set.
	// Init() will be called many times when running on PROOF (once per file to be processed).

	//USERS: SET OUTPUT FILE NAME //can be overriden by user in PROOF
	dOutputFileName = "mc_pimkpks_thrown.root"; //"" for none
	//USERS: SET OUTPUT TREE FILES/NAMES //e.g. binning into separate files for AmpTools
	//dOutputTreeFileNameMap["Bin1"] = "mcgen_bin1.root"; //key is user-defined, value is output file name
	//dOutputTreeFileNameMap["Bin2"] = "mcgen_bin2.root"; //key is user-defined, value is output file name
	//dOutputTreeFileNameMap["Bin3"] = "mcgen_bin3.root"; //key is user-defined, value is output file name
	dFlatTreeFileName = "/volatile/halld/home/viducic/selector_output/f1_pimkpks/thrown/pimkpks_thrown_spring.root"; //output flat tree (one combo per tree entry), "" for none
	dFlatTreeName = "pimkpks_thrown"; //if blank, default name will be chosen
	dSaveDefaultFlatBranches = false; // False: don't save default branches, reduce disk footprint.

	//Because this function gets called for each TTree in the TChain, we must be careful:
		//We need to re-initialize the tree interface & branch wrappers, but don't want to recreate histograms
	bool locInitializedPriorFlag = dInitializedFlag; //save whether have been initialized previously
	DSelector::Init(locTree); //This must be called to initialize wrappers for each new TTree
	//gDirectory now points to the output file with name dOutputFileName (if any)
	if(locInitializedPriorFlag)
		return; //have already created histograms, etc. below: exit

	dPreviousRunNumber = 0;

	/******************************** EXAMPLE USER INITIALIZATION: STAND-ALONE HISTOGRAMS *******************************/

	/************************************* ADVANCED EXAMPLE: CHOOSE BRANCHES TO READ ************************************/

	//TO SAVE PROCESSING TIME
		//If you know you don't need all of the branches/data, but just a subset of it, you can speed things up
		//By default, for each event, the data is retrieved for all branches
		//If you know you only need data for some branches, you can skip grabbing data from the branches you don't need
		//Do this by doing something similar to the commented code below

	//dTreeInterface->Clear_GetEntryBranches(); //now get none
	//dTreeInterface->Register_GetEntryBranch("Proton__P4"); //manually set the branches you want

	dFlatTreeInterface->Create_Branch_Fundamental<Int_t>("nParticles");
	dFlatTreeInterface->Create_Branch_Fundamental<Int_t>("nThrown");


	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Beam_px");
    dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Beam_py");
    dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Beam_pz");
    dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Beam_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Target_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Target_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Target_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Target_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiMinus1_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiMinus1_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiMinus1_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiMinus1_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiMinus2_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiMinus2_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiMinus2_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiMinus2_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiPlus_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiPlus_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiPlus_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("PiPlus_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("KPlus_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("KPlus_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("KPlus_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("KPlus_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Proton_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Proton_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Proton_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Proton_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Ks_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Ks_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Ks_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("Ks_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_p");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_p");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_p");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_kp");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_kp");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_kp");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_pim1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_pim1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_pim1");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_pim2");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_pim2");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_pim2");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_pip");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_pip");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_pip");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_f1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_f1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_f1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mass_f1");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mpippim");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mKsKp");

    dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("men_s");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("men_t");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("cosTheta_f1_cm");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_f1_cm");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("cosTheta_Ks_cm");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_Ks_cm");

}

Bool_t DSelector_mc_pimkpks_thrown::Process(Long64_t locEntry)
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

	//INSERT USER ANALYSIS UNIQUENESS TRACKING HERE

	/******************************************* LOOP OVER THROWN DATA ***************************************/

	//Thrown beam: just use directly
	double locBeamEnergyUsedForBinning = 0.0;
	if(dThrownBeam != NULL)
		locBeamEnergyUsedForBinning = dThrownBeam->Get_P4().E();
		TLorentzVector locBeamP4 = dThrownBeam->Get_P4();
		TLorentzVector locProdSpacetimeVertex =dThrownBeam->Get_X4();//Get production vertex


	TLorentzVector dTargetP4;
	dTargetP4.SetXYZM(0.0,0.0,0.0,0.938);

	TLorentzVector locProtonP4;
	TLorentzVector locPiMinus1P4;
	TLorentzVector locPiPlusP4;
	TLorentzVector locPiMinus2P4;
	TLorentzVector locKPlusP4;
	TLorentzVector locKShortP4;

	// TLorentzVector PiPlusHypo1;
	// TLorentzVector PiPlusHypo2;
	

	Bool_t piMinusChecked = false;
	int nparticles = 0;
	int nThrown = Get_NumThrown();

	//Loop over throwns
	for(UInt_t loc_i = 0; loc_i < Get_NumThrown(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dThrownWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
		Particle_t locPID = dThrownWrapper->Get_PID();
		TLorentzVector locThrownP4 = dThrownWrapper->Get_P4();
		cout << "Thrown " << loc_i << ": " << locPID << ", " << locThrownP4.Px() << ", " << locThrownP4.Py() << ", " << locThrownP4.Pz() << ", " << locThrownP4.E() << endl;
		if (locPID == 11){
			locKPlusP4 = locThrownP4;
		}
		if (locPID == 14){
			locProtonP4 = locThrownP4;
		}
		if (locPID == 8){
			locPiPlusP4 = locThrownP4;
		}
		if(locPID == 16){
			locKShortP4 = locThrownP4;
		}
		if (locPID == 9){
			if(!piMinusChecked) { 
				locPiMinus1P4 = locThrownP4;
				piMinusChecked = true;
			} 
			else{
				locPiMinus2P4 = locThrownP4;
			}
			// if (loc_i == 2) { locPiPlus2P4 = locThrownP4; }
			// if (loc_i == 4) { locPiPlus1P4 = locThrownP4; }
		}
	}	
	double proton_theta = locProtonP4.Theta() * 180/3.141592653;
	double proton_phi = locProtonP4.Phi() * 180/3.141592653;
	double proton_mom = locProtonP4.P();

	double piminus1_theta = locPiMinus1P4.Theta() * 180/3.141592653;
	double piminus1_phi = locPiMinus1P4.Phi() * 180/3.141592653;
	double piminus1_mom = locPiMinus1P4.P();

	double Kplus_theta = locKPlusP4.Theta() * 180/3.141592653;
	double Kplus_phi = locKPlusP4.Phi() * 180/3.141592653;
	double Kplus_mom = locKPlusP4.P();

	double piplus_theta = locPiPlusP4.Theta() * 180/3.141592653;
	double piplus_phi = locPiPlusP4.Phi() * 180/3.141592653;
	double piplus_mom = locPiPlusP4.P();

	double piminus2_theta = locPiMinus2P4.Theta() * 180/3.141592653;
	double piminus2_phi = locPiMinus2P4.Phi() * 180/3.141592653;
	double piminus2_mom = locPiMinus2P4.P();


	double s_men = (locBeamP4 + dTargetP4).M2();
	double w_var = (locBeamP4 + dTargetP4).M();
	double t_kmks  = (dTargetP4 - locProtonP4).M2();
	double minus_t_kmks = (-(t_kmks));

	TLorentzVector locPip2Pim_P4 = locPiMinus2P4 + locPiPlusP4;
	TLorentzVector locKpKsPim_P4 = locKPlusP4 + locPiMinus1P4 + locKShortP4;



	// double ks_theta = locPip2Pim_P4.Theta() * 180/3.141592653;
	// double ks_phi = locPip2Pim_P4.Phi() * 180/3.141592653;
	// double ks_mom = locPip2Pim_P4.P();

	double ks_theta = locKShortP4.Theta() * 180/3.141592653;
	double ks_phi = locKShortP4.Phi() * 180/3.141592653;
	double ks_mom = locKShortP4.P();

	double f1_phi = locKpKsPim_P4.Phi() * 180/3.141592653;
	double f1_theta =  locKpKsPim_P4.Theta() * 180/3.141592653;
	double f1_mom = locKpKsPim_P4.P();
	double f1_mass = locKpKsPim_P4.M();
	

	TLorentzVector locF1P4 = locKpKsPim_P4;
	// Boosting in CM frame

	TLorentzVector cms = locBeamP4 + dTargetP4;
	TVector3 locBoost_cms = -cms.BoostVector();

	TLorentzVector locBeamP4_CM = locBeamP4 ;
	TLorentzVector locPiMinus1P4_CM = locPiMinus1P4 ;
	TLorentzVector locKPlusP4_CM = locKPlusP4;
	TLorentzVector locProtonP4_CM = locProtonP4;
	//Step 1
	TLorentzVector locPiPlusP4_CM = locPiPlusP4;
	TLorentzVector locPiMinus2P4_CM = locPiMinus2P4;

	TLorentzVector locKpPim2PipP4_CM = locKpKsPim_P4;
	// TLorentzVector locKshortP4_CM = locPip2Pim_P4;
	TLorentzVector locKshortP4_CM = locKShortP4;

	TLorentzVector locF1P4_CM = locKpPim2PipP4_CM;


	locBeamP4_CM.Boost(locBoost_cms);
	locKPlusP4_CM.Boost(locBoost_cms);
	locProtonP4_CM.Boost(locBoost_cms);
	locKpPim2PipP4_CM.Boost(locBoost_cms);
	locKshortP4_CM.Boost(locBoost_cms);

	locF1P4_CM.Boost(locBoost_cms);

	// TVector3 y_hat = (locBeamP4_CM.Vect().Unit().Cross(locF1P4_CM.Vect().Unit())).Unit();
	

	// // Boosting in GJ frame
	// TVector3 boostGJ= -locF1P4_CM.BoostVector();                                 //-(locA2P4_CM.Vect())*(1.0/locA2P4_CM.E());
	
	// TLorentzVector locBeamP4_GJ = locBeamP4_CM;
	// TLorentzVector locPiPlus1P4_GJ = locPiPlus1P4_CM;
	// TLorentzVector locKMinusP4_GJ = locKMinusP4_CM;
	// TLorentzVector locProtonP4_GJ = locProtonP4_CM;
	// //Step 1
	// TLorentzVector locPiMinusP4_GJ = locPiMinusP4_CM;
	// TLorentzVector locPiPlus2P4_GJ = locPiPlus2P4_CM;
	// TLorentzVector locKshortP4_GJ = locKshortP4_CM;
	// TLorentzVector locProtonPip1P4_GJ = locProtonPip1P4_CM;
	// TLorentzVector locKmPip2PimP4_GJ = locKmPip2PimP4_CM;

	// TLorentzVector locF1P4_GJ = locF1P4_CM;
	// //TLorentzVector locDeltaP4_GJ = locDeltaP4_CM;

	// locBeamP4_GJ.Boost(boostGJ);
	// locKMinusP4_GJ.Boost(boostGJ);
	// locKshortP4_GJ.Boost(boostGJ);
	// locKmPip2PimP4_GJ.Boost(boostGJ);
	
	// locF1P4_GJ.Boost(boostGJ);
	// //locDeltaP4_GJ.Boost(boostGJ);


	// TVector3 z_GJ; 
	// z_GJ.SetXYZ(locBeamP4_GJ.X(),locBeamP4_GJ.Y(),locBeamP4_GJ.Z());//z GJ
	// TVector3 z_hat = z_GJ.Unit();
	// TVector3 x_hat = y_hat.Cross(z_hat);//x hat GJ
	// TVector3 vec_Ks(locKshortP4_GJ.Vect()*x_hat, locKshortP4_GJ.Vect()*y_hat, locKshortP4_GJ.Vect()*z_hat);

	// double cosThetaKs_GJ = vec_Ks.CosTheta();
	// double phiKs_GJ = vec_Ks.Phi()* 180/3.141592653;

	dFlatTreeInterface->Fill_Fundamental<Int_t>("nParticles", nparticles);
	dFlatTreeInterface->Fill_Fundamental<Int_t>("nThrown", nThrown);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("Beam_E", locBeamP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Beam_px", locBeamP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Beam_py", locBeamP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Beam_pz", locBeamP4.Pz());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("Target_E", dTargetP4.M());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Target_px", dTargetP4.X());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Target_py", dTargetP4.Y());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Target_pz", dTargetP4.Z());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiMinus1_E", locPiMinus1P4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiMinus1_px", locPiMinus1P4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiMinus1_py", locPiMinus1P4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiMinus1_pz", locPiMinus1P4.Pz());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiMinus2_E", locPiMinus2P4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiMinus2_px", locPiMinus2P4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiMinus2_py", locPiMinus2P4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiMinus2_pz", locPiMinus2P4.Pz());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiPlus_E", locPiPlusP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiPlus_px", locPiPlusP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiPlus_py", locPiPlusP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("PiPlus_pz", locPiPlusP4.Pz());


	dFlatTreeInterface->Fill_Fundamental<Double_t>("KPlus_E", locKPlusP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("KPlus_px", locKPlusP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("KPlus_py", locKPlusP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("KPlus_pz", locKPlusP4.Pz());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("Ks_E", locKShortP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Ks_px", locKShortP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Ks_py", locKShortP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Ks_pz", locKShortP4.Pz());
	// dFlatTreeInterface->Fill_Fundamental<Double_t>("Ks_E", locPip2Pim_P4.E());
	// dFlatTreeInterface->Fill_Fundamental<Double_t>("Ks_px", locPip2Pim_P4.Px());
	// dFlatTreeInterface->Fill_Fundamental<Double_t>("Ks_py", locPip2Pim_P4.Py());
	// dFlatTreeInterface->Fill_Fundamental<Double_t>("Ks_pz", locPip2Pim_P4.Pz());


	dFlatTreeInterface->Fill_Fundamental<Double_t>("Proton_E", locProtonP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Proton_px", locProtonP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Proton_py", locProtonP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("Proton_pz", locProtonP4.Pz());


	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_p", proton_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_p",proton_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_p", proton_phi);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_pim1", piminus1_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_pim1", piminus1_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_pim1", piminus1_phi );

	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_kp", Kplus_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_kp",Kplus_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_kp", Kplus_phi);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_pim2", piminus2_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_pim2", piminus2_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_pim2", piminus2_phi );

	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_pip", piplus_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_pip", piplus_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_pip", piplus_phi);				

	dFlatTreeInterface->Fill_Fundamental<Double_t>("mass_f1", f1_mass);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("mpippim",locPip2Pim_P4.M());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mKsKp", locKpKsPim_P4.M());


	dFlatTreeInterface->Fill_Fundamental<Double_t>("men_s",s_men);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("men_t",minus_t_kmks);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("cosTheta_Ks_cm", locKshortP4_CM.CosTheta());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_Ks_cm", locKshortP4_CM.Phi()*180/3.141592653);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("cosTheta_f1_cm", locF1P4_CM.CosTheta());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_f1_cm", locF1P4_CM.Phi()*180/3.141592653);

	// dFlatTreeInterface->Fill_Fundamental<Double_t>("cosTheta_Ks_gj",cosThetaKs_GJ);
	// dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_Ks_gj", phiKs_GJ);

	//OR Manually:
	//BEWARE: Do not expect the particles to be at the same array indices from one event to the next!!!!
	//Why? Because while your channel may be the same, the pions/kaons/etc. will decay differently each event.

	//BRANCHES: https://halldweb.jlab.org/wiki/index.php/Analysis_TTreeFormat#TTree_Format:_Simulated_Data
	TClonesArray** locP4Array = dTreeInterface->Get_PointerToPointerTo_TClonesArray("Thrown__P4");
	TBranch* locPIDBranch = dTreeInterface->Get_Branch("Thrown__PID");
/*
	Particle_t locThrown1PID = PDGtoPType(((Int_t*)locPIDBranch->GetAddress())[0]);
	TLorentzVector locThrown1P4 = *((TLorentzVector*)(*locP4Array)->At(0));
	cout << "Particle 1: " << locThrown1PID << ", " << locThrown1P4.Px() << ", " << locThrown1P4.Py() << ", " << locThrown1P4.Pz() << ", " << locThrown1P4.E() << endl;
	Particle_t locThrown2PID = PDGtoPType(((Int_t*)locPIDBranch->GetAddress())[1]);
	TLorentzVector locThrown2P4 = *((TLorentzVector*)(*locP4Array)->At(1));
	cout << "Particle 2: " << locThrown2PID << ", " << locThrown2P4.Px() << ", " << locThrown2P4.Py() << ", " << locThrown2P4.Pz() << ", " << locThrown2P4.E() << endl;
*/


	/******************************************* BIN THROWN DATA INTO SEPARATE TREES FOR AMPTOOLS ***************************************/

/*
	//THESE KEYS MUST BE DEFINED IN THE INIT SECTION (along with the output file names)
	if((locBeamEnergyUsedForBinning >= 8.0) && (locBeamEnergyUsedForBinning < 9.0))
		Fill_OutputTree("Bin1"); //your user-defined key
	else if((locBeamEnergyUsedForBinning >= 9.0) && (locBeamEnergyUsedForBinning < 10.0))
		Fill_OutputTree("Bin2"); //your user-defined key
	else if((locBeamEnergyUsedForBinning >= 10.0) && (locBeamEnergyUsedForBinning < 11.0))
		Fill_OutputTree("Bin3"); //your user-defined key
*/
	Fill_FlatTree();
	return kTRUE;
}

void DSelector_mc_pimkpks_thrown::Finalize(void)
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
