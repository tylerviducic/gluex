import ROOT


# define a default style for GlueX plots
gluex_style = ROOT.TStyle("gluex", "Default GlueX Style")

gluex_style.SetCanvasBorderMode(0)
gluex_style.SetPadBorderMode(0)
gluex_style.SetPadColor(0)
gluex_style.SetCanvasColor(0)
gluex_style.SetTitleColor(ROOT.kBlack, "xyz")
gluex_style.SetStatColor(0)

# default window sizes
gluex_style.SetCanvasDefW(800)
gluex_style.SetCanvasDefH(600)

# default margins 
gluex_style.SetPadBottomMargin(0.11)
gluex_style.SetPadLeftMargin(0.11)
gluex_style.SetPadTopMargin(0.05)
gluex_style.SetPadRightMargin(0.05)

# axis labels and settings
gluex_style.SetStripDecimals(0);
gluex_style.SetLabelSize(0.035,"xyz") # size of axis value font
gluex_style.SetTitleSize(0.04,"xyz") # size of axis title font
gluex_style.SetTitleFont(42,"xyz") # font option
gluex_style.SetLabelFont(42,"xyz")  
gluex_style.SetTitleOffset(1.25,"y")  
gluex_style.SetTitleOffset(1.1,"x")  
gluex_style.SetLabelOffset(0.01,"xyz") # stop collisions of "0"s at the origin

# histogram settings
gluex_style.SetOptStat(0) # no stats box by default
gluex_style.SetOptTitle(0) # no title by default
gluex_style.SetHistLineWidth(2)  

# various histogram fill colors
gluex_style.SetHistFillColor(920) # grey
#gluex_style.SetHistFillColor(5) # yellow
#gluex_style.SetHistFillColor(38) # pale blue
#gluex_style.SetHistFillColor(600-7) # blue
#gluex_style.SetHistFillColor(632-4) # red
#gluex_style.SetHistFillColor(416+1) # green
#gluex_style.SetPadGridX(1) # Beni likes this
#gluex_style.SetPadGridY(1)


# pick a palette for 2D plots
# gluex_style.SetPalette(ROOT.kViridis) 
# #gluex_style.SetPalette(ROOT.kBird) # default
gluex_style.SetPalette(ROOT.kCividis)
# gluex_style.SetPalette(ROOT.kColorPrintableOnGrey) 
# gluex_style.SetPalette(ROOT.kDarkBodyRadiator) # I like this one better...

gluex_style.cd()