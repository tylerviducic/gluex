#ifndef DSelector_mc_pimkpks_recon_h
#define DSelector_mc_pimkpks_recon_h

#include <iostream>

#include "DSelector/DSelector.h"
#include "DSelector/DHistogramActions.h"
#include "DSelector/DCutActions.h"

#include "TH1I.h"
#include "TH2I.h"

class DSelector_mc_pimkpks_recon : public DSelector
{ 
	public:

		DSelector_mc_pimkpks_recon(TTree* locTree = NULL) : DSelector(locTree){}
		virtual ~DSelector_mc_pimkpks_recon(){}

		void Init(TTree *tree);
		Bool_t Process(Long64_t entry);

	private:

		void Get_ComboWrappers(void);
		void Finalize(void);

		// BEAM POLARIZATION INFORMATION
		UInt_t dPreviousRunNumber;
		bool dIsPolarizedFlag; //else is AMO
		bool dIsPARAFlag; //else is PERP or AMO

		bool dIsMC;

		// ANALYZE CUT ACTIONS
		// // Automatically makes mass histograms where one cut is missing
		DHistogramAction_AnalyzeCutActions* dAnalyzeCutActions;

		//CREATE REACTION-SPECIFIC PARTICLE ARRAYS

		//Step 0
		DParticleComboStep* dStep0Wrapper;
		DBeamParticle* dComboBeamWrapper;
		DChargedTrackHypothesis* dPiMinus1Wrapper;
		DChargedTrackHypothesis* dKPlusWrapper;
		DChargedTrackHypothesis* dProtonWrapper;

		//Step 1
		DParticleComboStep* dStep1Wrapper;
		DChargedTrackHypothesis* dPiPlusWrapper;
		DChargedTrackHypothesis* dPiMinus2Wrapper;

				// DEFINE YOUR HISTOGRAMS HERE
		// EXAMPLES:
		TH1F* dHist_MissingMassSquared;
		TH1F* dHist_BeamEnergy;
		TH1F* dHist_IM_PipPim2;
		TH1F* dHist_IM_Pim1P;
		TH1F* dHist_IM_KsPim;
		TH1F* dHist_IM_KpPim;
		TH1F* dHist_IM_KpP;
		TH1F* dHist_IM_KsKpPim;
		TH1F* dHist_IM_KsKpPim_1285;
		TH1F* dHist_IM_KsKpPim_1420;
		TH1F* dHist_IM_PKs; 
		TH1F* dHist_MinusT;


		TH2F* dHist_Ks_vs_FlightSig;
		TH2F* dHist_Pim1P_vs_KsKpPim;
		TH2F* dHist_KpP_KsKpPim;
		TH2F* dHist_DOCA_vs_IM_PipPim;
		TH2F* dHist_DOCA_vs_IM_KsKpPim;
		TH2F* dHist_CosTheta_vs_IM_PipPim;
		TH2F* dHist_CosTheta_vs_IM_KsKpPim;

		TH2F* dHist_IM_KsKpPim_vs_t_70_75;
		TH2F* dHist_IM_KsKpPim_vs_t_75_80;
		TH2F* dHist_IM_KsKpPim_vs_t_80_85;
		TH2F* dHist_IM_KsKpPim_vs_t_85_90;
		TH2F* dHist_IM_KsKpPim_vs_t_82_88;

		TH1F* dHist_IM_KsKpPim_1285_binned[5];
		TH1F* dHist_IM_KsKpPim_1420_binned[5];
		TH1F* dHist_IM_KsKpPim_binned[5];
		TH1F* dHist_Phi0_1285[5];
		TH1F* dHist_Phi90_1285[5];
		TH1F* dHist_Phi45_1285[5];
		TH1F* dHist_Phi135_1285[5];
		TH1F* dHist_Phi0_background_1285[5];
		TH1F* dHist_Phi90_background_1285[5];
		TH1F* dHist_Phi45_background_1285[5];
		TH1F* dHist_Phi135_background_1285[5];
		TH1F* dHist_f1_0_1285[5];
		TH1F* dHist_f1_90_1285[5];
		TH1F* dHist_f1_45_1285[5];
		TH1F* dHist_f1_135_1285[5];

		TH1F* dHist_IM_KsKmPip_binned_full[10];
		TH1F* dHist_f1_1285_binned_full[10];
		TH1F* dHist_f1_1285_beam_7[10];
		TH1F* dHist_f1_1285_beam_8[10];
		TH1F* dHist_f1_1285_beam_9[10];
		TH1F* dHist_f1_1285_beam_10[10];


		TH1F* dHist_CosThetaCM[5];
		TH1F* dHist_W_binned_f1[5];

	ClassDef(DSelector_mc_pimkpks_recon, 0);
};

void DSelector_mc_pimkpks_recon::Get_ComboWrappers(void)
{
	//Step 0
	dStep0Wrapper = dComboWrapper->Get_ParticleComboStep(0);
	dComboBeamWrapper = static_cast<DBeamParticle*>(dStep0Wrapper->Get_InitialParticle());
	dPiMinus1Wrapper = static_cast<DChargedTrackHypothesis*>(dStep0Wrapper->Get_FinalParticle(0));
	dKPlusWrapper = static_cast<DChargedTrackHypothesis*>(dStep0Wrapper->Get_FinalParticle(1));
	dProtonWrapper = static_cast<DChargedTrackHypothesis*>(dStep0Wrapper->Get_FinalParticle(3));

	//Step 1
	dStep1Wrapper = dComboWrapper->Get_ParticleComboStep(1);
	dPiPlusWrapper = static_cast<DChargedTrackHypothesis*>(dStep1Wrapper->Get_FinalParticle(0));
	dPiMinus2Wrapper = static_cast<DChargedTrackHypothesis*>(dStep1Wrapper->Get_FinalParticle(1));
}

#endif // DSelector_mc_pimkpks_recon_h
