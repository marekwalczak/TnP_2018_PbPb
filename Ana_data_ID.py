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
PDFName = "cbcbPlusPol2_fixed" #cbcbPlusPol2, cbPlusPol1, cbPlusPol2, cbGausPlusPol1, cbGausPlusPol2, cbcbPlusPol1

# defines a set of efficiency calculations, what PDF to use for fitting and how to bin the data;
# there will be a separate output directory for each calculation that includes a simultaneous fit, side band subtraction and counting. 


VEFFICIENCYSET =cms.VPSet(

   cms.PSet(
      TrkMu_1bin = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("SoftId", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            #pair_dz = cms.vdouble(0.0,0.2),
            pt = cms.vdouble(1.0, 10.0),
            eta = cms.vdouble(-2.4, 2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ), 

   cms.PSet(
      Trk_ID_absetadep = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("SoftId", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            #pair_dz = cms.vdouble(0.0,0.2),
            pt = cms.vdouble(1.0, 10.0),
            abseta = cms.vdouble(0.0,1.2,1.6,2.1,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  
      
   cms.PSet(        
      Trk_ID_pTdep_abseta00_10 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("SoftId", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            #pair_dz = cms.vdouble(0.0,0.2),
            pt = cms.vdouble(3.3,3.8,4.5,6.0,10),
            abseta = cms.vdouble(0.0, 1.0),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),

   cms.PSet(        
      Trk_ID_pTdep_abseta10_16 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("SoftId", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            #pair_dz = cms.vdouble(0.0,0.2),
            pt = cms.vdouble(1.0,1.25,1.5,2.0,2.5,3.0,4.0,9), #             pt = cms.vdouble(1.0,1.25,1.5,2.0,2.5,3.0,4.0,10),   pt = cms.vdouble(1.0,1.7,2.5,3.3,4.3,10),             pt = cms.vdouble(1.0,1.25,1.35,1.45,1.55,1.65,1.75,1,85,2.5,3.3,4.3,10),
            abseta = cms.vdouble(1.0, 1.6),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),

   cms.PSet(        
      Trk_ID_pTdep_abseta16_21 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("SoftId", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            #pair_dz = cms.vdouble(0.0,0.2),
            pt = cms.vdouble(1.0,1.2,1.5,2.0,3.0,8),
            abseta = cms.vdouble(1.6, 2.1),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),
      
   cms.PSet(        
      Trk_ID_pTdep_abseta21_24 = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("SoftId", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            #pair_dz = cms.vdouble(0.0,0.2),
            pt = cms.vdouble(1.0,1.2,1.5,2.0,3.0,7),
            abseta = cms.vdouble(2.1, 2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),




  cms.PSet(
      Trk_ID_centdep = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("SoftId", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            abseta = cms.vdouble(0.0, 2.4),
            pt = cms.vdouble(1.0, 10.0),
            tag_hiBin = cms.vdouble(140,150,160,170,180,190,200),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),

   cms.PSet(
      Trk_ID_etadep = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("SoftId", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            #pair_dz = cms.vdouble(0.0,0.2),
            pt = cms.vdouble(1.0, 10.0),
            eta = cms.vdouble(-2.4,-1.2,0.0,1.2,2.4),
            ),
         BinToPDFmap = cms.vstring(PDFName)
         )
      ),  

   cms.PSet(
      Trk_ID_absetavspT = cms.PSet(
         EfficiencyCategoryAndState = cms.vstring("SoftId", "true"),
         UnbinnedVariables = cms.vstring("mass"),
         BinnedVariables = cms.PSet(
            tag_hiBin = cms.vdouble(180,200),
            #pair_dz = cms.vdouble(0.0,0.2),
            #pt = cms.vdouble(2.0,2.5,3.0, 3.5, 4.0, 4.5, 5.0, 5.5),
            pt = cms.vdouble(1.0,2.0,3.0,4.0,5.0,6.0,10),
            #eta = cms.vdouble(-2.4, 2.4),
            abseta = cms.vdouble(0.0,1.2,1.6,2.1,2.4),
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
if scenario == "7": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[6])
if scenario == "8": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[7])
if scenario == "10": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[2], VEFFICIENCYSET[3], VEFFICIENCYSET[4], VEFFICIENCYSET[5])
if scenario == "11": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[4], VEFFICIENCYSET[5])
if scenario == "0": EFFICIENCYSET = cms.PSet(VEFFICIENCYSET[0],VEFFICIENCYSET[1],VEFFICIENCYSET[2], VEFFICIENCYSET[3], VEFFICIENCYSET[4], VEFFICIENCYSET[5], VEFFICIENCYSET[6], VEFFICIENCYSET[7])


process.TagProbeFitTreeAnalyzer = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    # IO parameters:
    InputFileNames = cms.vstring("file:Trees/Both_v1_data.root"),
    #InputFileNames = cms.vstring("file:Trees/tnpJpsi_Data_PbPb_200130_pTa1.root"),
    InputDirectoryName = cms.string("tpTree"),
    InputTreeName = cms.string("fitter_tree"),
    OutputFileName = cms.string("Output/Data/tnp_DATA_ID_scenario_%s_syst_bkg_pol2.root" % (scenario) ), #"mass2834" for mass range systematics 
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
                         mass             = cms.vstring("Tag-Probe Mass", "2.85", "3.4", "GeV/c^{2}"),  # mass range syst: 2.85 - 3.4       # oryginal: mass range syst: 2.8-3.4, nominal: 2.6-3.5
                         pt               = cms.vstring("Probe p_{T}", "0.0", "1000", "GeV/c"),
                         eta              = cms.vstring("Probe #eta", "-2.4", "2.4", ""),
                         abseta           = cms.vstring("Probe |#eta|", "0", "2.5", ""),
                         tag_hiBin        = cms.vstring("Centrality bin", "0", "200", ""),
                         pair_dz          = cms.vstring("pair_dz", "0", "5", ""),

    ),
    # defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
    Categories = cms.PSet(
                          TM = cms.vstring("TM", "dummy[true=1,false=0]"),
                          SoftId = cms.vstring("SoftId", "dummy[true=1,false=0]"),
                          #HLT_HIUPC_SingleMu0_NotMBHF2AND_v1 = cms.vstring("HLT_HIUPC_SingleMu0_NotMBHF2AND_v1", "dummy[true=1,false=0]"),
                          tag_TightIdReco = cms.vstring("tag_TightIdReco", "dummy[true=1,false=0]"),
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
       #cb + cb:
      cbcbPlusPol1_fixed = cms.vstring(
        "CBShape::signal1(mass, mean[3.08,3.00,3.2], sigma1[0.03, 0.01, 0.10], alpha[3, 2, 4], n[3, 2, 4])", # alpha[1.85, 0.1, 50], n[1.7, 0.2, 50]
        "RooFormulaVar::sigma2('@0*@1',{fracS[1.8,1.2,2.4],sigma1})",
        "CBShape::signal2(mass, mean, sigma2, alpha, n)",
        "SUM::signal(frac[0.8,0.1,1.]*signal1,signal2)",
        "Chebychev::backgroundPass(mass, {cPass[0.,-2,2]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-2,2]})",
        "efficiency[0.9,0.0,1.0]",
        "signalFractionInPassing[0.9]"
      ),
        #cb + cb:
      cbcbPlusPol1_loose = cms.vstring(
        "CBShape::signal1(mass, mean[3.08,3.00,3.3], sigma1[0.03, 0.005, 0.20], alpha[1.85, 0.05, 100], n[1.7, 0.1, 100])",  # loose
        "RooFormulaVar::sigma2('@0*@1',{fracS[1.8,1.0,3.0],sigma1})",
        "CBShape::signal2(mass, mean, sigma2, alpha, n)",
        "SUM::signal(frac[0.8,0.05,2.]*signal1,signal2)",
        "Chebychev::backgroundPass(mass, {cPass[0.,-4,4]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-4,4]})",
        "efficiency[0.9,0.0,1.0]",
        "signalFractionInPassing[0.9]"
      ),
      

        #cb + cb: n[2, 1, 3])", 
      cbcbPlusPol2_fixed = cms.vstring(
        "CBShape::signal1(mass, mean[3.08,3.00,3.2], sigma1[0.03, 0.01, 0.10], alpha[3, 2, 4], n[3, 2, 4])", # alpha[1.85, 0.1, 50], n[1.7, 0.2, 50]
        "RooFormulaVar::sigma2('@0*@1',{fracS[1.8,1.2,2.4],sigma1})",
        "CBShape::signal2(mass, mean, sigma2, alpha, n)",
        "SUM::signal(frac[0.8,0.1,1.]*signal1,signal2)",
        "Chebychev::backgroundPass(mass, {cPass[0.,-2,2], cPass2[0.,-2,2]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-2,2], cFail2[0.,-2,2]})",
        "efficiency[0.9,0.0,1.0]",
        "signalFractionInPassing[0.9]"
      ),      
      
    ),
   Efficiencies = EFFICIENCYSET

)

process.fitness = cms.Path(
    process.TagProbeFitTreeAnalyzer
)



'''
LOOSE

        #cb + cb:
      cbcbPlusPol1 = cms.vstring(
        "CBShape::signal1(mass, mean[3.08,3.00,3.2], sigma1[0.03, 0.01, 0.10], alpha[1.85, 0.1, 50], n[1.7, 0.2, 50])",
        "RooFormulaVar::sigma2('@0*@1',{fracS[1.0,0.1,10.0],sigma1})",
        "CBShape::signal2(mass, mean, sigma2, alpha2[1.85, 0.1, 50], n2[1.7, 0.2, 50])",
        "SUM::signal(frac[1.0,0.1,10.0]*signal1,signal2)",
        "Chebychev::backgroundPass(mass, {cPass[0.,-2,2]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-2,2]})",
        "efficiency[0.9,0.0,1.0]",
        "signalFractionInPassing[0.9]"
      ),
      
LOOSE

        #signal syst:
      cbGausPlusPol1 = cms.vstring(
        "CBShape::signal1(mass, mean[3.08,3.00,3.2], sigma1[0.03, 0.01, 0.10], alpha[1.85, 0.1, 50], n[1.7, 0.2, 50])",
        "RooFormulaVar::sigma2('@0*@1',{fracS[1.0,0.1,10.0],sigma1})",
        "Gaussian::signal2(mass, mean, sigma2)",
        "SUM::signal(frac[1.0,0.1,10.0]*signal1,signal2)",
        "Chebychev::backgroundPass(mass, {cPass[0.,-2,2]})",
        "Chebychev::backgroundFail(mass, {cFail[0.,-2,2]})",
        "efficiency[0.9,0.0,1.0]",
        "signalFractionInPassing[0.9]"
      ),

NOMINAL:

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
      
      


NOMINAL:

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

'''

