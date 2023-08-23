void RunF1MC_KsKmPip(){

    gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmks__ks_pippim__B4_M16_Tree\")");
    // TChain* ch = new TChain("pipkmks__ks_pippim__B4_M16_Tree");
    // ch->Add("/volatile/halld/home/viducic/pipkmks_mc/signal/tree_pipkmks__ks_pippim__B4_M16/04*"); //spring 18
    gROOT->ProcessLine("ch->Add(\"/volatile/halld/home/viducic/pipkmks_mc/signal/tree_pipkmks__ks_pippim__B4_M16/04*"); //spring 18
    // ch->Add("/volatile/halld/home/viducic/pipkmks_mc/signal/tree_pipkmks__ks_pippim__B4_M16/05*") //fall 18
    // ch->Add("/volatile/halld/home/viducic/pipkmks_mc/signal/tree_pipkmks__ks_pippim__B4_M16/03*") // 17 spring
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_mc_pipkmks_flat.C++\", 6)");
    // ch.Process("DSelector_mc_pipkmks_flat.C++", 6)

    // DPROOFLiteManager *dproof = new DPROOFLiteManager();
    // dproof->Process_Chain(&ch, "DSelector_mc_pipkmks_flat.C++", 6, "outfilehist.root", "outfiletree.root"); 

    // PHASESPACE MC ONLY

    // gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmks__ks_pippim__B4_M16_Tree\")"); // only for phasespace
    // // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_phasespace_s18_100m_v16_rt_t29_3246/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp/*.root\")"); // spring 18 phasespace 
    // // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_phasespace_f18_100m_v16_rt_t29_3247/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp/*.root\")"); // fall 18 phasespace 
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_phasespace_s17_100m_v16_rt_t29_3245/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp/*.root\")"); //2017 phasespace
    // gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    // gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_mc_pipkmks_phasespace_flat.C++\", 6)");

}


// OLD FILE PATHS //

    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_s18_100m_v16_rt_20220419034710pm/root/trees/*.root\")"); //spring OLD
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_f18_100m_v16_rt_20220419034345pm/root/trees/*.root\")"); //fall OLD
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pipkmks_17_100m_v50_rt_20230117125849pm/root/trees/*.root\")"); //2017 OLD
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_bgk_flat_20220720035959pm/root/trees/*.root\")"); //flat bkg
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_20220310040819pm/root/trees/*.root\")"); //2017
    // gROOT->ProcessLine("ch->Add(\"/w/halld-scshelf2101/home/viducic/f1_mc/bggen/combined_bggen_total_fall_batch01.root\")"); //2017


        // // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_s18_100m_v16_rt_t29_3237/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp/*.root\")"); //spring
    // // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_f18_100m_v16_rt_t29_3238/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp/*.root\")"); //fall
    // //gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pipkmks_f18_100m_v16_rt_t29_3239/root/trees/tree_pipkmks__ks_pippim__B4_M16_gen_amp/*.root\")"); //THIS IS 2017 THERE WAS A NAMING ERROR