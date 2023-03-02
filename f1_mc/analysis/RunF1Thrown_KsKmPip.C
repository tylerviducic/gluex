void RunF1Thrown_KsKmPip(){

    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gEnv->SetValue("ProofLite.Sandbox", "/volatile/halld/home/viducic/PROOF/.proof/");
    gROOT->ProcessLine("DPROOFLiteManager::Set_SandBox(\"/volatile/halld/home/viducic/PROOF/.proof\")");
    gROOT->ProcessLine("TChain* ch = new TChain(\"Thrown_Tree\")"); 
    // TChain* ch = new TChain("Thrown_Tree");
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_s18_100m_v16_rt_20220419034710pm/root/thrown/*.root\")"); //spring
    // ch->Add("/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_s18_100m_v16_20220409110456am/root/thrown/*.root"); //spring
    gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_f18_100m_v16_rt_20220419034345pm/root/thrown/*.root\")"); //fall
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_20220310040819pm/root/thrown/*.root\")"); //2017
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_mc_pipkmks_thrown.C++\", 4)");

}