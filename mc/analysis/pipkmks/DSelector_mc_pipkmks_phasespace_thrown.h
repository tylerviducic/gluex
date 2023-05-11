#ifndef DSelector_mc_pipkmks_phasespace_thrown_h
#define DSelector_mc_pipkmks_phasespace_thrown_h

#include <iostream>

#include "DSelector/DSelector.h"

#include "TH1I.h"
#include "TH2I.h"

class DSelector_mc_pipkmks_phasespace_thrown : public DSelector
{
	public:

		DSelector_mc_pipkmks_phasespace_thrown(TTree* locTree = NULL) : DSelector(locTree){}
		virtual ~DSelector_mc_pipkmks_phasespace_thrown(){}

		void Init(TTree *tree);
		Bool_t Process(Long64_t entry);

	private:

		void Finalize(void);

		// BEAM POLARIZATION INFORMATION
		UInt_t dPreviousRunNumber;
		bool dIsPolarizedFlag; //else is AMO
		bool dIsPARAFlag; //else is PERP or AMO

	ClassDef(DSelector_mc_pipkmks_phasespace_thrown, 0);
};

#endif // DSelector_mc_pipkmks_phasespace_thrown_h
