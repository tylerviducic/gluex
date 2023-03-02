#ifndef DSelector_mc_pipkmks_recon_h
#define DSelector_mc_pipkmks_recon_h

#include <iostream>

#include "DSelector/DSelector.h"
#include "DSelector/DHistogramActions.h"
#include "DSelector/DCutActions.h"

#include "TH1I.h"
#include "TH2I.h"

class DSelector_mc_pipkmks_recon : public DSelector
{ 
	public:

		DSelector_mc_pipkmks_recon(TTree* locTree = NULL) : DSelector(locTree){}
		virtual ~DSelector_mc_pipkmks_recon(){}

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
		DChargedTrackHypothesis* dPiPlus1Wrapper;
		DChargedTrackHypothesis* dKMinusWrapper;
		DChargedTrackHypothesis* dProtonWrapper;

		//Step 1
		DParticleComboStep* dStep1Wrapper;
		DChargedTrackHypothesis* dPiPlus2Wrapper;
		DChargedTrackHypothesis* dPiMinusWrapper;

// DEFINE YOUR HISTOGRAMS HERE
		// EXAMPLES:
		TH1F* dHist_MissingMassSquared;
		TH1F* dHist_BeamEnergy;
		TH1F* dHist_IM_Pip2Pim;
		TH1F* dHist_IM_Pip1P;
		TH1F* dHist_IM_KsPip;
		TH1F* dHist_IM_KmPip;
		TH1F* dHist_IM_KmP;
		TH1F* dHist_IM_KsKmPip;
		TH1F* dHist_IM_KsKmPip_1285;
		TH1F* dHist_IM_KsKmPip_1420;
		TH1F* dHist_IM_PKs;
		TH1F* dHist_W; 
		TH1F* dHist_MinusT;


		TH2F* dHist_Ks_vs_FlightSig;
		TH2F* dHist_Pip1P_vs_KsKmPip;
		TH2F* dHist_KmP_KsKmPip;
		TH2F* dHist_DOCA_vs_IM_PipPim;
		TH2F* dHist_DOCA_vs_IM_KsKmPip;
		TH2F* dHist_CosTheta_vs_IM_PipPim;
		TH2F* dHist_CosTheta_vs_IM_KsKmPip;
		TH2F* dHist_W_vs_IM_KsKmPip;

		TH2F* dHist_IM_KsKmPip_vs_t_70_75;
		TH2F* dHist_IM_KsKmPip_vs_t_75_80;
		TH2F* dHist_IM_KsKmPip_vs_t_80_85;
		TH2F* dHist_IM_KsKmPip_vs_t_85_90;
		TH2F* dHist_IM_KsKmPip_vs_t_82_88;
 
		TH1F* dHist_IM_KsKmPip_1285_binned[5];
		TH1F* dHist_IM_KsKmPip_1420_binned[5];
		TH1F* dHist_IM_KsKmPip_binned[5];
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

		TH1F* dHist_IM_KsKmPip_binned_full_low[8];
		TH1F* dHist_f1_1285_binned_full_low[8];
		
		TH1F* dHist_IM_KsKmPip_binned_full_med[5];
		TH1F* dHist_f1_1285_binned_full_med[5];
		
		TH1F* dHist_IM_KsKmPip_binned_full_high[5];
		TH1F* dHist_f1_1285_binned_full_high[5];
		
		TH1F* dHist_f1_1285_beam_5_low[4];
		TH1F* dHist_f1_1285_beam_6_low[4];
		TH1F* dHist_f1_1285_beam_7_low[4];
		TH1F* dHist_f1_1285_beam_8_low[4];
		TH1F* dHist_f1_1285_beam_9_low[4];
		TH1F* dHist_f1_1285_beam_10_low[4];
		
		TH1F* dHist_f1_1285_beam_5_med[2];
		TH1F* dHist_f1_1285_beam_6_med[2];
		TH1F* dHist_f1_1285_beam_7_med[2];
		TH1F* dHist_f1_1285_beam_8_med[2];
		TH1F* dHist_f1_1285_beam_9_med[2];
		TH1F* dHist_f1_1285_beam_10_med[2];
		
		TH1F* dHist_f1_1285_beam_5_high[2];
		TH1F* dHist_f1_1285_beam_6_high[2];
		TH1F* dHist_f1_1285_beam_7_high[2];
		TH1F* dHist_f1_1285_beam_8_high[2];
		TH1F* dHist_f1_1285_beam_9_high[2];
		TH1F* dHist_f1_1285_beam_10_high[2];


		TH1F* dHist_CosThetaCM[5];
		TH1F* dHist_W_binned_f1[5];

	ClassDef(DSelector_mc_pipkmks_recon, 0);
};

void DSelector_mc_pipkmks_recon::Get_ComboWrappers(void)
{
	//Step 0
	dStep0Wrapper = dComboWrapper->Get_ParticleComboStep(0);
	dComboBeamWrapper = static_cast<DBeamParticle*>(dStep0Wrapper->Get_InitialParticle());
	dPiPlus1Wrapper = static_cast<DChargedTrackHypothesis*>(dStep0Wrapper->Get_FinalParticle(0));
	dKMinusWrapper = static_cast<DChargedTrackHypothesis*>(dStep0Wrapper->Get_FinalParticle(1));
	dProtonWrapper = static_cast<DChargedTrackHypothesis*>(dStep0Wrapper->Get_FinalParticle(3));

	//Step 1
	dStep1Wrapper = dComboWrapper->Get_ParticleComboStep(1);
	dPiPlus2Wrapper = static_cast<DChargedTrackHypothesis*>(dStep1Wrapper->Get_FinalParticle(0));
	dPiMinusWrapper = static_cast<DChargedTrackHypothesis*>(dStep1Wrapper->Get_FinalParticle(1));
}

#endif // DSelector_mc_pipkmks_recon_h
