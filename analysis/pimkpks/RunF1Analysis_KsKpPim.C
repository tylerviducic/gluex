void RunF1Analysis_KsKpPim(){

    gROOT->ProcessLine("TChain* ch = new TChain(\"pimkpks__B4_M16_Tree\")");
    // gROOT->ProcessLine("ch->Add(\"/cache/halld/RunPeriod-2018-01/analysis/ver03/tree_pimkpks__B4_M16/merged/tree_pimkpks__B4_M16_04*.root\")");
    gROOT->ProcessLine("ch->Add(\"/cache/halld/RunPeriod-2018-08/analysis/ver16/tree_pimkpks__B4_M16/merged/*.root\")");
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_f1_pimkpks.C+\", 12)");

}