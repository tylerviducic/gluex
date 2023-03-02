void RunThrownDSelector_PipKmKs(){

    gROOT->ProcessLine("TChain* ch = new TChain(\"Thrown_Tree\")");
    gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_20220314034550pm/root/thrown/tree_thrown_gen_amp_03105*.root\")"); //fall
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_acceptance_study_pipkmks_thrown.C++\", 4)");

}