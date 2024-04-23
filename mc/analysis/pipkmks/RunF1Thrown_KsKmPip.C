void RunF1Thrown_KsKmPip(){

    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gEnv->SetValue("ProofLite.Sandbox", "/volatile/halld/home/viducic/PROOF/.proof/");
    gROOT->ProcessLine("DPROOFLiteManager::Set_SandBox(\"/volatile/halld/home/viducic/PROOF/.proof\")");
    gROOT->ProcessLine("TChain* ch = new TChain(\"Thrown_Tree\")");
    gROOT->ProcessLine("ch->Add(\"/w/halld-scshelf2101/halld3/home/viducic/new_mc/f1_pipkmks_s18_3726/root/thrown/*.root\")"); //spring 2018
    // gROOT->ProcessLine("ch->Add(\"/w/halld-scshelf2101/halld3/home/viducic/new_mc/f1_pipkmks_f18_3727/root/thrown/*.root\")"); //spring 2018
    // gROOT->ProcessLine("ch->Add(\"/w/halld-scshelf2101/halld3/home/viducic/new_mc/f1_pipkmks_s17_3725/root/thrown/*.root\")"); // 2017
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_mc_pipkmks_thrown.C++\", 8)");

//  PHASSPACE MC

    // gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    // gEnv->SetValue("ProofLite.Sandbox", "/volatile/halld/home/viducic/PROOF/.proof/");
    // gROOT->ProcessLine("DPROOFLiteManager::Set_SandBox(\"/volatile/halld/home/viducic/PROOF/.proof\")");
    // gROOT->ProcessLine("TChain* ch = new TChain(\"Thrown_Tree\")"); 
    // // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_phasespace_s18_100m_v16_rt_t29_3246/root/thrown/*.root\")"); //spring 2018
    // // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_phasespace_f18_100m_v16_rt_t29_3247/root/thrown/*.root\")"); //fall 2018
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_phasespace_s17_100m_v16_rt_t29_3245/root/thrown/*.root\")"); // 2017

    // gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_mc_pipkmks_phasespace_thrown.C++\", 6)");
}




// Old stuff //

    // TChain* ch = new TChain("Thrown_Tree");
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_s18_100m_v16_rt_20220419034710pm/root/thrown/*.root\")"); //spring OLD
    // ch->Add("/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_s18_100m_v16_20220409110456am/root/thrown/*.root"); //spring OLD 
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_f18_100m_v16_rt_20220419034345pm/root/thrown/*.root\")"); //fall OLD 
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_20220310040819pm/root/thrown/*.root\")"); //2017 OLD