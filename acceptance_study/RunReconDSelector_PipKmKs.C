void RunReconDSelector_PipKmKs(){

    gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmks__ks_pippim__B4_M16_Tree\")");
    gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_20220314034550pm/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp_03105*.root\")"); //fall
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_acceptance_study_pipkmks.C++\", 4)");

}