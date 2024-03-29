void Run_KpPimGen_Cross(){

    gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmks__ks_pippim__B4_M16_Tree\")");
    //gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_s18_100m_v16_rt_20220419034710pm/root/trees/*.root\")"); //spring
    gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/kp_gen_km_recon_20221010015754pm/root/trees/*.root\")"); //fall
    //gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_17_100m_v47_rt_20230117125357pm/root/trees/*.root\")"); //fall
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_bgk_flat_20220720035959pm/root/trees/*.root\")"); //flat bkg
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_20220310040819pm/root/trees/*.root\")"); //2017
    // gROOT->ProcessLine("ch->Add(\"/w/halld-scshelf2101/home/viducic/f1_mc/bggen/combined_bggen_total_fall_batch01.root\")"); //2017
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_mc_pipkmks_flat.C++\", 4)");

}