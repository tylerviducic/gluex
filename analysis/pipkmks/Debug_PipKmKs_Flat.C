// debug of flat tree generation

void Debug_PipKmKs_Flat(){

    gROOT->ProcessLine("TChain* ch = new TChain(\"pipkmks__B4_M16_Tree\")");
    gROOT->ProcessLine("ch->Add(\"/cache/halld/RunPeriod-2018-01/analysis/ver03/tree_pipkmks__B4_M16/merged/tree_pipkmks__B4_M16_0425*.root\")");
    //gROOT->ProcessLine("ch->Add(\"/cache/halld/RunPeriod-2018-01/analysis/ver03/tree_pipkmks__B4_M16/merged/tree_pipkmks__B4_M16_04*.root\")");
    //gROOT->ProcessLine("ch->Add(\"/cache/halld/RunPeriod-2018-08/analysis/ver06/tree_pipkmks__B4_M16/merged/tree_pipkmks__B4_M16_05*.root\")");
    gROOT->ProcessLine(".x $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C");
    gROOT->ProcessLine("DPROOFLiteManager::Process_Chain(ch, \"DSelector_pipkmks_flat_bestchi2.C+\", 4)");
}     