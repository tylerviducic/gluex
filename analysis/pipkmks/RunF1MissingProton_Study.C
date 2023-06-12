void RunF1MissingProton_Study(){

    gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmksmissprot__ks_pippim__B4_M16_Tree\")");
    gROOT->ProcessLine("ch->Add(\"/volatile/halld/home/viducic/pipkmks_mpx/combined_runs/tree_pipkmksmissprot__ks_pippim__B4_M16_0408*.root\")");
    //gROOT->ProcessLine("ch->Add(\"/cache/halld/RunPeriod-2018-01/analysis/ver03/tree_pipkmks__B4_M16/merged/tree_pipkmks__B4_M16_04*.root\")");
    //gROOT->ProcessLine("ch->Add(\"/cache/halld/RunPeriod-2018-08/analysis/ver06/tree_pipkmks__B4_M16/merged/tree_pipkmks__B4_M16_05*.root\")");
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_pipkmks_mxp_unconstrained.C+\", 4)");
}