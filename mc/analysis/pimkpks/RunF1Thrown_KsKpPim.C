void RunF1Thrown_KsKpPim(){

    gROOT->ProcessLine("TChain* ch = new TChain(\"Thrown_Tree\")");
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pimkpks_s17_100m_v50_rt_t29_3248/root/thrown/*.root\")"); // 2017
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pimkpks_s18_100m_v50_rt_t29_3249/root/thrown/*.root\")"); // 2018 spring
    gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pimkpks_f18_100m_v50_rt_t29_3250/root/thrown/*.root\")"); // 2018 fall
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_mc_pimkpks_thrown.C+\", 6)");

}

// for phasespace
//file paths for whenever I get around to writing this

// fall18 phasespace
// /lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pimkpks_phasespace_f18_100m_v50_rt_t29_3251/
// 2017 phasespace
// /lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pimkpks_phasespace_s17_100m_v50_rt_t29_3253/
// spring2018 phasespace
// /lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/pimkpks_phasespace_s18_100m_v50_rt_t29_3252/



// OLD FILES 
    //gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pimkpks_20210820040225pm/root/thrown/*.root\")"); // fall
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pimkpks_20210820040849pm/root/thrown/*.root\")"); // spring
    //gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pimkpks_f18_100m_v16_rt_20230117103653am/root/thrown/*.root\")"); // fall
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/f1_pimkpks_s18_100m_v16_rt_20230117101753am/root/thrown/*.root\")"); // fall