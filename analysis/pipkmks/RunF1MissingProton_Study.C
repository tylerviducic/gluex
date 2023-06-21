void RunF1MissingProton_Study(){


    // MXP KS UNCONSTRAINED
    // gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmksmissprot__ks_pippim__B4_M16_Tree\")");
    // gROOT->ProcessLine("ch->Add(\"/volatile/halld/home/viducic/pipkmks_mpx/combined_runs/tree_pipkmksmissprot__ks_pippim__B4_M16_0408*.root\")");
    // gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    // gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_pipkmks_mxp_unconstrained.C+\", 4)");


    // MXP KS CONSTRAINED
    // gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmksmissprot__ks_pippim__B4_Tree\")");
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/volatile/halld/home/viducic/mxp_study/mxp_ks_constrained/combined_runs/tree_pipkmksmissprot__ks_pippim__B4_0408*.root\")");
    // gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    // gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_pipkmks_mxp_constrained.C+\", 6)");

    // PD KS UNCONSTRAINED
    gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmks__ks_pippim__B4_M16_Tree\")");
    gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/volatile/halld/home/viducic/pipkmks_pd/combined_runs/tree_pipkmks__ks_pippim__B4_M16_040*.root\")");
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_pipkmks_pd_unconstrained.C+\", 6)");
    
    // PD KS CONSTRAINED
    // gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmks__ks_pippim__B4_Tree\")");
    // gROOT->ProcessLine("ch->Add(\"/lustre19/expphy/volatile/halld/home/viducic/mxp_study/pd_ks_constrained/combined_runs/tree_pipkmks__ks_pippim__B4_0408*.root\")");
    // gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    // gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_pipkmks_pd_constrained.C+\", 6)");

}