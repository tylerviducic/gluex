// pimkpks__ks_pippim__B4_M16_Tree
void RunNstarMC_KsKpPim(string path_to_files){

    // path_to_files MUST END IN WILDCARD

    #include "TProof.h"
    #include "TProofDebug.h"
    R__LOAD_LIBRARY(libDSelector);

    TChain* ch = new TChain("pimkpks__ks_pippim__B4_M16_Tree");
    char *cstr = new char[path_to_files.length() + 1];
    strcpy(cstr, path_to_files.c_str());
    ch->Add(cstr);
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    DPROOFLiteManager *dproof = new DPROOFLiteManager();
    dproof->Process_Chain(ch, "/work/halld/home/viducic/mc/analysis/pimkpks/DSelector_mc_pimkpks_flat_correct_rf.C++", 6);

}
