import FWCore.ParameterSet.Config as cms

import sys
args =sys.argv[1:]
if len(args) < 2: scenario = "0"
else: 
   scenario = args[1]
print("Will run scenario " + scenario) 

# scenario: 1 pT, 2-3 pT in abseta bins, 4 abseta, 5 eta, 6 centrality, 7 runNb, 0 (or no parameter) run all

process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )    
PDFName = "cbcbPlusPol1" #cbPlusPol1, cbPlusPol2, cbGausPlusPol1, cbGausPlusPol2, cbcbPlusPol1

# defines a set of efficiency calculations, what PDF to use for fitting and how to bin the data;
# there will be a separate output directory for each calculation that includes a simultaneous fit, side band subtraction and counting. 




VEFFICIENCYSET =cms.VPSet(

   cms.PSet(
      Trk_absetadep_pT1_1d5 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(1.0, 1.5),
            abseta = cms.vdouble(0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  
      
   cms.PSet(
      Trk_absetadep_pT1d5_2 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(1.5, 2.0),
            abseta = cms.vdouble(0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  
      
   cms.PSet(
      Trk_absetadep_pT2_2d5 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(2.0, 2.5),
            abseta = cms.vdouble(0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  

   cms.PSet(
      Trk_absetadep_pT2d5_3 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(2.5, 3.0),
            abseta = cms.vdouble(0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  
      
   cms.PSet(
      Trk_absetadep_pT3_5 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(3.0, 5.0),
            abseta = cms.vdouble(0,0.4,0.8,1.2,1.6,2.0,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  
   cms.PSet(
      Trk_absetadep_pT5_7 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(5.0, 7.0),
            abseta = cms.vdouble(0,0.4,0.8,1.2,1.6,2.0,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  
   cms.PSet(
      Trk_absetadep_pT7_10 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(7.0, 10.0),
            abseta = cms.vdouble(0,0.4,0.8,1.2,1.6,2.0,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  
      
   cms.PSet(
      Trk_absetadep_pT1_10 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(1.0, 10.0),
            abseta = cms.vdouble(0,0.4,0.8,1.2,1.6,2.0,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  
      
   cms.PSet(        
      Trk_pTdep_abseta00_08 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,7.0,10),
            abseta = cms.vdouble(0.0, 0.8),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),

   cms.PSet(        
      Trk_pTdep_abseta08_16 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,7.0,10),
            abseta = cms.vdouble(0.8, 1.6),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),

   cms.PSet(        
      Trk_pTdep_abseta16_24 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            pt = cms.vdouble(1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,7.0,10),
            abseta = cms.vdouble(1.6, 2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),

   cms.PSet(
      Trk_absetavspT = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            #pt = cms.vdouble(2.0,2.5,3.0, 3.5, 4.0, 4.5, 5.0, 5.5),
            pt = cms.vdouble(1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5),
            #eta = cms.vdouble(-2.4, 2.4),
            abseta = cms.vdouble(0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),

  cms.PSet(
      Trk_centdep = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("TM", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            eta = cms.vdouble(-2.4,2.4),
            #pt = cms.vdouble(0.,30.0),
            pt = cms.vdouble(3.0, 5.5),
            #tag_hiBin = cms.vdouble(0,10,20,40,60,80,100,150,200),
            #tag_hiBin = cms.vdouble(0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,300),
            #tag_hiBin = cms.vdouble(0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220),
            #tag_hiBin = cms.vdouble(100,110,120,130,140,150,160,170,180,190,200,210,220),
            tag_hiBin = cms.vdouble(130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,205,210),
            #tag_hiBin = cms.vdouble(0,50,100,150,200,250,300,350,500),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),





    )

#Actual selection
if scenario == "1": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[0])
if scenario == "2": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[1])
if scenario == "3": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[2])
if scenario == "4": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[3])
if scenario == "5": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[4])
if scenario == "6": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[5])
if scenario == "9": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[8])
if scenario == "0": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[0],VEFFICIENCYSET[1],VEFFICIENCYSET[2], VEFFICIENCYSET[3], VEFFICIENCYSET[4], VEFFICIENCYSET[5])
if scenario == "10": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[0],VEFFICIENCYSET[1],VEFFICIENCYSET[2], VEFFICIENCYSET[3], VEFFICIENCYSET[4], VEFFICIENCYSET[5],VEFFICIENCYSET[6], VEFFICIENCYSET[7], VEFFICIENCYSET[8],VEFFICIENCYSET[9], VEFFICIENCYSET[10])
if scenario == "11": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[0],VEFFICIENCYSET[1],VEFFICIENCYSET[2], VEFFICIENCYSET[3])



process.TagProbeFitTreeAnalyzer = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    # IO parameters:
    InputFileNames = cms.vstring("file:Trees/tnpJpsi_MC_PbPb_200514_Acc.root"),
    InputDirectoryName = cms.string("tpTreeTrk"),
    InputTreeName = cms.string("fitter_tree"),
    OutputFileName = cms.string("Output/MC/tnp_MC_1_scenario_%s_Acc_180.root" % (scenario) ), #"mass2834" for mass range systematics 


   #numbrer of CPUs to use for fitting
    NumCPU = cms.uint32(25),
    # specifies whether to save the RooWorkspace containing the data for each bin and
    # the pdf object with the initial and final state snapshots
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(50),
    binsForMassPlots = cms.uint32(50),
    SaveWorkspace = cms.bool(False),
    
    # defines all the real variables of the probes available in the input tree and intended for use in the efficiencies
    Variables = cms.PSet(
                         mass             = cms.vstring("Tag-Probe Mass", "2.8", "3.4", "GeV/c^{2}"),  # mass range syst: 2.8-3.4, nominal: 2.6-3.5
                         pt               = cms.vstring("Probe p_{T}", "0.0", "1000", "GeV/c"),
                         eta              = cms.vstring("Probe #eta", "-2.4", "2.4", ""),
                         abseta           = cms.vstring("Probe |#eta|", "0", "2.5", ""),
                         tag_hiBin        = cms.vstring("Centrality bin", "0", "300", ""),
    ),
    # defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
    Categories = cms.PSet(
                          TM = cms.vstring("TM", "dummy[true=1,false=0]"),
    ),

    # defines all the PDFs that will be available for the efficiency calculations; uses RooFit's "factory" syntax;
    # each pdf needs to define "signal", "backgroundPass", "backgroundFail" pdfs, "efficiency[0.9,0,1]" and "signalFractionInPassing[0.9]" are used for initial values  
    PDFs = cms.PSet(
        #nominal:
       cbPlusPol1 = cms.vstring(
        "CBShape::signal(mass, mean[3.08,3.00,3.2], sigma[0.03, 0.01, 0.10], alpha[1.85, 0.1, 50], n[1.7, 0.2, 50])",
        "Chebychev::backgroundPass(mass, {cPass[0.,-2,2]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-2,2]})",
        "efficiency[0.9,0,1]",
        "signalFractionInPassing[0.9]"
      ), 
        #background syst:
        cbPlusPol2 = cms.vstring(
        "CBShape::signal(mass, mean[3.08,3.00,3.2], sigma[0.03, 0.01, 0.10], alpha[1.85, 0.1, 50], n[1.7, 0.2, 50])",
        "Chebychev::backgroundPass(mass, {cPass[0.,-2,2], cPass2[0.,-2,2]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-2,2], cFail2[0.,-2,2]})",
        "efficiency[0.9,0,1]",
        "signalFractionInPassing[0.9]"
      ),
        #signal syst:
      cbGausPlusPol1 = cms.vstring(
        "CBShape::signal1(mass, mean[3.08,3.00,3.2], sigma1[0.03, 0.01, 0.10], alpha[1.85, 0.1, 50], n[1.7, 0.2, 50])",
        "RooFormulaVar::sigma2('@0*@1',{fracS[1.8,1.2,2.4],sigma1})",
        "Gaussian::signal2(mass, mean, sigma2)",
        "SUM::signal(frac[0.8,0.1,1.]*signal1,signal2)",
        "Chebychev::backgroundPass(mass, {cPass[0.,-2,2]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-2,2]})",
        "efficiency[0.9,0,1]",
        "signalFractionInPassing[0.9]"
      ),
      cbGausPlusPol2 = cms.vstring(
        "CBShape::signal1(mass, mean[3.08,3.00,3.2], sigma1[0.03, 0.01, 0.10], alpha[1.85, 0.1, 50], n[1.7, 0.2, 50])",
        "RooFormulaVar::sigma2('@0*@1',{fracS[1.8,1.2,2.4],sigma1})",
        "Gaussian::signal2(mass, mean, sigma2)",
        "SUM::signal(frac[0.8,0.1,1.]*signal1,signal2)",
        "Chebychev::backgroundPass(mass, {cPass[0.,-2,2], cPass2[0.,-2,2]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-2,2], cFail2[0.,-2,2]})",
        "efficiency[0.9,0,1]",
        "signalFractionInPassing[0.9]"
      ),
        #cb + cb:
      cbcbPlusPol1 = cms.vstring(
        "CBShape::signal1(mass, mean[3.08,3.00,3.2], sigma1[0.03, 0.01, 0.10], alpha[1.85, 0.1, 50], n[1.7, 0.2, 50])",
        "RooFormulaVar::sigma2('@0*@1',{fracS[1.8,1.2,2.4],sigma1})",
        "CBShape::signal2(mass, mean, sigma2, alpha, n)",
        "SUM::signal(frac[0.8,0.1,1.]*signal1,signal2)",
        "Chebychev::backgroundPass(mass, {cPass[0.,-2,2]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-2,2]})",
        "efficiency[0.9,0.0,1.0]",
        "signalFractionInPassing[0.9]"
      ),
      

    ),
   Efficiencies = EFFICIENCYSET

)

process.fitness = cms.Path(
    process.TagProbeFitTreeAnalyzer
)
