#ifndef DSelector_pq_h
#define DSelector_pq_h

#include <iostream>

#include "DSelector/DSelector.h"
#include "DSelector/DHistogramActions.h"
#include "DSelector/DCutActions.h"

#include "TH1I.h"
#include "TH2I.h"

class DSelector_pq : public DSelector
{
	public:

		DSelector_pq(TTree* locTree = NULL) : DSelector(locTree){}
		virtual ~DSelector_pq(){}

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
		DChargedTrackHypothesis* dPiMinusWrapper;
		DChargedTrackHypothesis* dPiPlus2Wrapper;

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
		TH1F* dHist_IM_PKs;
		TH1F* dHist_W; 
		TH1F* dHist_MinusT;
		TH1F* dHist_TMin;
		TH1F* dHist_KmKs;
		TH1F* dHist_KsP;

		TH2F* dHist_Ks_vs_FlightSig;
		TH2F* dHist_Pip1P_vs_KsKmPip;
		TH2F* dHist_KmP_KsKmPip;
		TH2F* dHist_DOCA_vs_IM_PipPim;
		TH2F* dHist_DOCA_vs_IM_KsKmPip;
		TH2F* dHist_CosTheta_vs_IM_PipPim;
		TH2F* dHist_CosTheta_vs_IM_KsKmPip;
		TH2F* dHist_W_vs_IM_KsKmPip;
		TH2F* dHist_KmP_KsP;

	ClassDef(DSelector_pq, 0);
};

void DSelector_pq::Get_ComboWrappers(void)
{
	//Step 0
	dStep0Wrapper = dComboWrapper->Get_ParticleComboStep(0);
	dComboBeamWrapper = static_cast<DBeamParticle*>(dStep0Wrapper->Get_InitialParticle());
	dPiPlus1Wrapper = static_cast<DChargedTrackHypothesis*>(dStep0Wrapper->Get_FinalParticle(0));
	dKMinusWrapper = static_cast<DChargedTrackHypothesis*>(dStep0Wrapper->Get_FinalParticle(1));
	dProtonWrapper = static_cast<DChargedTrackHypothesis*>(dStep0Wrapper->Get_FinalParticle(3));

	//Step 1
	dStep1Wrapper = dComboWrapper->Get_ParticleComboStep(1);
	dPiMinusWrapper = static_cast<DChargedTrackHypothesis*>(dStep1Wrapper->Get_FinalParticle(0));
	dPiPlus2Wrapper = static_cast<DChargedTrackHypothesis*>(dStep1Wrapper->Get_FinalParticle(1));
}

#endif // DSelector_pq_h
