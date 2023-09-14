void RunVerTest23(string filename){

    #include "TProof.h"
    #include "TProofDebug.h"
    R__LOAD_LIBRARY(libDSelector);

    TChain *ch = new TChain("pipkmks__ks_pippim__B4_M16_Tree");
    char *cstr = new char[filename.length() + 1];
    strcpy(cstr, filename.c_str());
    ch->Add(cstr);
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    DPROOFLiteManager *dproof = new DPROOFLiteManager();
    dproof->Process_Chain(ch, "/work/halld/home/viducic/analysis/pipkmks/ver_test_dselectors/DSelector_pipkmks_flat_bestX2_ver23.C++", 6);
}