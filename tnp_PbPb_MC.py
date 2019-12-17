import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/himc/HINPbPbAutumn18DR/JPsi_pThat-2_TuneCP5_HydjetDrumMB_5p02TeV_Pythia8/AODSIM/mva98_103X_upgrade2018_realistic_HI_v11-v1/280001/2F35FF90-AE38-3540-8917-FA1BF93A278E.root'),
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.GlobalTag.globaltag = cms.string('103X_upgrade2018_realistic_HI_v11')

## PbPb centrality bin producer
process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
    cms.PSet(record = cms.string("HeavyIonRcd"),
        tag = cms.string("CentralityTable_HFtowers200_HydjetDrum5F_v1032x01_mc"),
        connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
        label = cms.untracked.string("HFtowers")
        ),
    ])

## ==== FILTERS ====
### PbPb Event Selection
process.load("MuonAnalysis.TagAndProbe.OfflinePrimaryVerticesRecovery_cfi")
process.load('MuonAnalysis.TagAndProbe.collisionEventSelection_cff')
### Trigger selection
process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")
process.triggerResultsFilter.triggerConditions = cms.vstring( 'HLT_HIUPC_SingleMu0_NotMBHF2AND_v*' )
process.triggerResultsFilter.hltResults = cms.InputTag("TriggerResults","","HLT")
process.triggerResultsFilter.l1tResults = cms.InputTag("") # keep empty!
process.triggerResultsFilter.throw = False
### Filter sequence
process.goodVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2"),
    filter = cms.bool(True),
)
process.fastFilter = cms.Sequence(process.triggerResultsFilter + process.offlinePrimaryVerticesRecovery)

##    __  __
##   |  \/  |_   _  ___  _ __  ___
##   | |\/| | | | |/ _ \| '_ \/ __|
##   | |  | | |_| | (_) | | | \__ \
##   |_|  |_|\__,_|\___/|_| |_|___/
##
## ==== Merge CaloMuons and Tracks into the collection of reco::Muons  ====

InAcceptance_Ups = '(abs(eta)<2.4 && pt>=3.0)'

from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.mergedMuons = cms.EDProducer("CaloMuonMerger",
    mergeTracks = cms.bool(True),
    mergeCaloMuons = cms.bool(False), # AOD
    muons     = cms.InputTag("muons"),
    caloMuons = cms.InputTag("calomuons"),
    tracks    = cms.InputTag("generalTracks"),
    minCaloCompatibility = calomuons.minCaloCompatibility,
    ## Apply some minimal pt cut
    muonsCut     = cms.string(InAcceptance_Ups + " && track.isNonnull"),
    caloMuonsCut = cms.string(InAcceptance_Ups),
    tracksCut    = cms.string(InAcceptance_Ups),
)
process.twoMuons = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("mergedMuons"), minNumber = cms.uint32(2))

## ==== Trigger matching
process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
changeRecoMuonInput(process, "mergedMuons")
## For trigger muons
switchOffAmbiguityResolution(process)
## For L1 muons
addHLTL1Passthrough(process)
useL1Stage2Candidates(process) # Enable L1 stage2 setup
process.muonMatchHLTL1.useStage2L1 = cms.bool(True)
process.muonMatchHLTL1.useMB2InOverlap = cms.bool(True)
process.muonMatchHLTL1.preselection = cms.string("")
appendL1MatchingAlgo(process)
process.muonL1Info.maxDeltaR = 0.3
process.muonL1Info.maxDeltaEta = 0.2
process.muonL1Info.fallbackToME1 = True
process.muonMatchHLTL1.maxDeltaR = 0.3
process.muonMatchHLTL1.maxDeltaEta = 0.2
process.muonMatchHLTL1.fallbackToME1 = True
process.patTrigger.collections.remove("hltL1extraParticles")
process.patTrigger.collections.append("hltGtStage2Digis:Muon")
process.muonL1Info.matched = cms.InputTag("gtStage2Digis:Muon")
process.muonMatchHLTL1.matchedCuts = cms.string('coll("hltGtStage2Digis:Muon")')

## ==== Tag and probe variables
from MuonAnalysis.TagAndProbe.common_variables_cff import *
process.load("MuonAnalysis.TagAndProbe.common_modules_cff")
## PbPb centrality variables
from MuonAnalysis.TagAndProbe.heavyIon_variables_cff import *
process.load("MuonAnalysis.TagAndProbe.heavyIon_modules_cff")
## Flags
### Muon Id
#SoftIdReco = "muonID('TMOneStationTight') && innerTrack.hitPattern.trackerLayersWithMeasurement > 5 && innerTrack.hitPattern.pixelLayersWithMeasurement > 0 && innerTrack.quality(\"highPurity\")"
SoftId = "passed('SoftCutBasedId')"
### Trigger
LowPtTriggerProbeFlags = cms.PSet(
    # Double Muon Trigger Paths
    HLT_HIUPC_DoubleMu0_NotMBHF2AND_v1 = cms.string("!triggerObjectMatchesByPath('HLT_HIUPC_DoubleMu0_NotMBHF2AND_v*',1,0).empty()"),
    # Double Muon Trigger Filters
    HLT_HIUPC_DoubleMu0_NotMBHF2AND_Filter = cms.string("!triggerObjectMatchesByFilter('hltL1sDoubleMu0NotMBHF2AND').empty()"),

    # Single Muon Trigger Paths
    HLT_HIUPC_SingleMu0_NotMBHF2AND_v1 = cms.string("!triggerObjectMatchesByPath('HLT_HIUPC_SingleMu0_NotMBHF2AND_v*',1,0).empty()"),
    # Single Muon Trigger Filters
    HLT_HIUPC_SingleMu0_NotMBHF2AND_Filter = cms.string("!triggerObjectMatchesByFilter('hltL1sSingleMu0NotMBHF2AND').empty()"),
)
### Tracking
TRACK_CUTS = "track.isNonnull"

## ==== Tag muons
process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string(InAcceptance_Ups+" && "+SoftId+" && !triggerObjectMatchesByPath('HLT_HIUPC_SingleMu0_NotMBHF2AND_v*',1,0).empty()"),
)
process.oneTag = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagMuons"), minNumber = cms.uint32(1))
process.pseudoTag = cms.EDFilter("MuonSelector",
    src = cms.InputTag("mergedMuons"),
    cut = cms.string(InAcceptance_Ups+" && "+SoftId),
)
process.onePseudoTag = process.oneTag.clone(src = cms.InputTag("pseudoTag"))

## ==== Probe muons
process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string(InAcceptance_Ups+" && isTrackerMuon"),
)
process.oneProbe = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("probeMuons"), minNumber = cms.uint32(1))
process.pseudoProbe = cms.EDFilter("MuonSelector",
    src = cms.InputTag("mergedMuons"),
    cut = process.probeMuons.cut,
)
process.onePseudoProbe = process.oneProbe.clone(src = cms.InputTag("pseudoProbe"))

## ==== Tag and Probe muon pairs
process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('2.0 < mass < 4.0'),
    decay = cms.string('tagMuons@+ probeMuons@-')
)
process.onePair = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairs"), minNumber = cms.uint32(1))
process.pseudoPairs = process.tpPairs.clone(
    decay = cms.string('pseudoTag@+ pseudoProbe@-')
)
process.onePseudoPair = process.onePair.clone(src = cms.InputTag("pseudoPairs"))

process.fastPseudoTnP = cms.Sequence(process.mergedMuons + process.twoMuons + process.pseudoTag + process.onePseudoTag + process.pseudoProbe + process.onePseudoProbe + process.pseudoPairs + process.onePseudoPair)

## ==== Tag and Probe tree
process.tpTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # choice of tag and probe pairs, and arbitration
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("None"),
    # probe variables: all useful ones
    variables = cms.PSet(
        KinematicVariables,
        MuonIDVariables,
        TrackQualityVariables,
        GlobalTrackQualityVariables,
        L1Variables,
        dxyPVdzmin = cms.InputTag("muonDxyPVdzmin","dxyPVdzmin"),
        dzPV = cms.InputTag("muonDxyPVdzmin","dzPV"),
        dxyPV = cms.InputTag("muonDxyPVdzmin","dxyPV"),
    ),
    flags = cms.PSet(
        LowPtTriggerProbeFlags,
        TrackQualityFlags,
        MuonIDFlags,
        SoftId = cms.string(SoftId),
        InAcceptance_Ups = cms.string(InAcceptance_Ups),
        TrackCuts = cms.string(TRACK_CUTS),
    ),
    tagVariables = cms.PSet(
        KinematicVariables,
        MuonIDVariables,
        TrackQualityVariables,
        GlobalTrackQualityVariables,
        CentralityVariables,
        nVertices = cms.InputTag("nverticesModule"),
        dxyPVdzmin = cms.InputTag("muonDxyPVdzminTags","dxyPVdzmin"),
        dzPV = cms.InputTag("muonDxyPVdzminTags","dzPV"),
        dxyPV = cms.InputTag("muonDxyPVdzminTags","dxyPV"),
    ),
    tagFlags = cms.PSet(
        LowPtTriggerProbeFlags,
    ),
    pairVariables = cms.PSet(
        dz = cms.string("daughter(0).vz - daughter(1).vz"),
        pt = cms.string("pt"),
        rapidity = cms.string("rapidity"),
        deltaR = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)"),
        probeMultiplicity = cms.InputTag("probeMultiplicity"),
        probeMultiplicity_TMGM = cms.InputTag("probeMultiplicityTMGM"),
#        genWeight = cms.InputTag("genWeightInfo", "genWeight"),
    ),
    pairFlags = cms.PSet(
        BestJPsi = cms.InputTag("bestPairByJpsiMass"),
    ),
    isMC = cms.bool(False),
    addRunLumiInfo = cms.bool(True),
)

process.nverticesModule = cms.EDProducer("VertexMultiplicityCounter",
    probes = cms.InputTag("tagMuons"),
    objects = cms.InputTag("offlinePrimaryVertices"),
    objectSelection = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2")
)
process.bestPairByJpsiMass = cms.EDProducer("BestPairByMass",
    pairs = cms.InputTag("tpPairs"),
    mass  = cms.double(3.096916)
)
process.probeMultiplicity = cms.EDProducer("ProbeMulteplicityProducer",
    pairs = cms.InputTag("tpPairs")
)
process.probeMultiplicityTMGM = process.probeMultiplicity.clone(
    probeCut = cms.string("isTrackerMuon || isGlobalMuon")
)
process.muonDxyPVdzmin = cms.EDProducer("MuonDxyPVdzmin",
    probes = cms.InputTag("probeMuons")
)
process.muonDxyPVdzminTags = process.muonDxyPVdzmin.clone(
    probes = cms.InputTag("tagMuons")
)
#process.genWeightInfo = process.genAdditionalInfo.clone(
#    pairTag = cms.InputTag("tpPairs")
#)

process.tnpSimpleSequence = cms.Sequence(
    process.tagMuons +
    process.oneTag     +
    process.probeMuons +
    process.oneProbe   +
    process.tpPairs    +
    process.onePair    +
    process.nverticesModule +
    process.muonDxyPVdzmin + process.muonDxyPVdzminTags +
    process.probeMultiplicity + process.probeMultiplicityTMGM +
    process.bestPairByJpsiMass +
    process.centralityInfo +
    process.centralityBinInfo +
#    process.genWeightInfo +
    process.tpTree
)

process.tagAndProbe = cms.Path(
    process.fastFilter
    * process.fastPseudoTnP
    * process.centralityBin
    * process.mergedMuons * process.patMuonsWithTriggerSequence
    * process.tnpSimpleSequence
)


##    _____               _    _
##   |_   _| __ __ _  ___| | _(_)_ __   __ _
##     | || '__/ _` |/ __| |/ / | '_ \ / _` |
##     | || | | (_| | (__|   <| | | | | (_| |
##     |_||_|  \__,_|\___|_|\_\_|_| |_|\__, |
##                                     |___/

## Then make another collection for standalone muons, using standalone track to define the 4-momentum
process.muonsSta = cms.EDProducer("RedefineMuonP4FromTrack",
    src   = cms.InputTag("muons"),
    track = cms.string("outer"),
)
## Match to trigger, to measure the efficiency of HLT tracking
from PhysicsTools.PatAlgos.tools.helpers import *
process.patMuonsWithTriggerSequenceSta = cloneProcessingSnippet(process, process.patMuonsWithTriggerSequence, "Sta")
process.patMuonsWithTriggerSequenceSta.replace(process.patTriggerFullSta, process.patTriggerFull)
process.patTriggerSta.src = cms.InputTag("patTriggerFull")
process.muonMatchHLTL2Sta.maxDeltaR = 0.5
process.muonMatchHLTL3Sta.maxDeltaR = 0.5
massSearchReplaceAnyInputTag(process.patMuonsWithTriggerSequenceSta, "mergedMuons", "muonsSta")

## Define probes and T&P pairs
process.probeMuonsSta = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTriggerSta"),
    cut = cms.string("outerTrack.isNonnull"), # no real cut now
)
process.oneProbeSta = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("probeMuonsSta"), minNumber = cms.uint32(1))
process.pseudoProbeSta = cms.EDFilter("MuonSelector",
    src = cms.InputTag("muonsSta"),
    cut = process.probeMuonsSta.cut,
)
process.onePseudoProbeSta = process.oneProbeSta.clone(src = cms.InputTag("pseudoProbeSta"))

process.tpPairsSta = process.tpPairs.clone(
    cut = cms.string('2. < mass < 5.'),
    decay = cms.string('tagMuons@+ probeMuonsSta@-')
)
process.onePairSta = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairsSta"), minNumber = cms.uint32(1))
process.pseudoPairsSta = process.tpPairsSta.clone(
    decay = cms.string('pseudoTag@+ pseudoProbeSta@-')
)
process.onePseudoPairSta = process.onePairSta.clone(src = cms.InputTag("pseudoPairsSta"))

process.fastPseudoTnPSta = cms.Sequence(process.mergedMuons + process.pseudoTag + process.onePseudoTag + process.muonsSta + process.pseudoProbeSta + process.onePseudoProbeSta + process.pseudoPairsSta + process.onePseudoPairSta)

process.staToTkMatch.maxDeltaR = 0.3
process.staToTkMatch.maxDeltaPtRel = 2.
process.staToTkMatchNoJPsi.maxDeltaR = 0.3
process.staToTkMatchNoJPsi.maxDeltaPtRel = 2.
process.staToTkMatchNoBestJPsi.maxDeltaR = 0.3
process.staToTkMatchNoBestJPsi.maxDeltaPtRel = 2.

process.load("MuonAnalysis.TagAndProbe.tracking_reco_info_cff")

process.tpTreeSta = process.tpTree.clone(
    tagProbePairs = "tpPairsSta",
    arbitration   = "OneProbe",
    variables = cms.PSet(
        KinematicVariables,
        StaOnlyVariables,
        ## track matching variables
        #tk_deltaR = cms.InputTag("staToTkMatch","deltaR"),
        #tk_deltaEta = cms.InputTag("staToTkMatch","deltaEta"),
        #tk_deltaR_NoJPsi = cms.InputTag("staToTkMatchNoJPsi","deltaR"),
        #tk_deltaEta_NoJPsi = cms.InputTag("staToTkMatchNoJPsi","deltaEta"),
        #tk_deltaR_NoBestJPsi = cms.InputTag("staToTkMatchNoBestJPsi","deltaR"),
        #tk_deltaEta_NoBestJPsi = cms.InputTag("staToTkMatchNoBestJPsi","deltaEta"),
    ),
    flags = cms.PSet(
        outerValidHits = cms.string("outerTrack.numberOfValidHits > 0"),
        TM  = cms.string("isTrackerMuon"),
        tk  = cms.string("track.isNonnull"),
        isSTA = cms.string("isStandAloneMuon"),
        TrackCuts = cms.string(TRACK_CUTS),
        StaTkSameCharge = cms.string("outerTrack.isNonnull && innerTrack.isNonnull && (outerTrack.charge == innerTrack.charge)"),
        InAcceptance_Ups = cms.string(InAcceptance_Ups),
    ),
    tagVariables = cms.PSet(
        CentralityVariables,
        pt = cms.string("pt"),
        eta = cms.string("eta"),
        phi = cms.string("phi"),
        nVertices = cms.InputTag("nverticesModule"),
    ),
    tagFlags = cms.PSet(
        LowPtTriggerProbeFlags,
    ),
    pairVariables = cms.PSet(
        dz = cms.string("daughter(0).vz - daughter(1).vz"),
        pt = cms.string("pt"),
        rapidity = cms.string("rapidity"),
        deltaR = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)"),
#        genWeight = cms.InputTag("genWeightInfoSta", "genWeight"),
    ),
    pairFlags = cms.PSet(),
)

#process.genWeightInfoSta = process.genAdditionalInfo.clone(
#    pairTag = cms.InputTag("tpPairsSta")
#)

process.tnpSimpleSequenceSta = cms.Sequence(
    process.tagMuons +
    process.oneTag     +
    process.probeMuonsSta   +
    process.oneProbeSta     +
    process.tpPairsSta      +
    process.onePairSta      +
    process.nverticesModule +
    #process.staToTkMatchSequenceJPsi +
    process.centralityInfo +
    process.centralityBinInfo +
#    process.genWeightInfoSta +
    process.tpTreeSta
)

process.tagAndProbeSta = cms.Path(
    process.fastFilter
    * process.fastPseudoTnPSta
    * process.centralityBin
    * process.mergedMuons * process.patMuonsWithTriggerSequence
    * process.muonsSta * process.patMuonsWithTriggerSequenceSta
    * process.tnpSimpleSequenceSta
)

#--------------------------------------------------------------------
##    ____                   _____               _      ____            _
##   | __ )  __ _ _ __ ___  |_   _| __ __ _  ___| | __ |  _ \ _ __ ___ | |__   ___  ___
##   |  _ \ / _` | '__/ _ \   | || '__/ _` |/ __| |/ / | |_) | '__/ _ \| '_ \ / _ \/ __|
##   | |_) | (_| | | |  __/   | || | | (_| | (__|   <  |  __/| | | (_) | |_) |  __/\__ \
##   |____/ \__,_|_|  \___|   |_||_|  \__,_|\___|_|\_\ |_|   |_|  \___/|_.__/ \___||___/
##
##

process.probeMuonsTrk = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string(TRACK_CUTS + ' && ' + InAcceptance_Ups), #   muonSeededStepInOut = 13
)
process.oneProbeTrk = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("probeMuonsTrk"), minNumber = cms.uint32(1))
process.pseudoProbeTrk = cms.EDFilter("MuonSelector",
    src = cms.InputTag("mergedMuons"),
    cut = process.probeMuonsTrk.cut
)
process.onePseudoProbeTrk = process.oneProbeTrk.clone(src = cms.InputTag("pseudoProbeTrk"))

process.tpPairsTrk = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('2.5 < mass < 3.5'),
    decay = cms.string('tagMuons@+ probeMuonsTrk@-')
)
process.onePairTrk = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairsTrk"), minNumber = cms.uint32(1))
process.pseudoPairsTrk = process.tpPairsTrk.clone(
    decay = cms.string('pseudoTag@+ pseudoProbeTrk@-')
)
process.onePseudoPairTrk = process.onePairTrk.clone(src = cms.InputTag("pseudoPairsTrk"))

process.fastPseudoTnPTrk = cms.Sequence(process.mergedMuons + process.twoMuons + process.pseudoTag + process.onePseudoTag + process.pseudoProbeTrk + process.onePseudoProbeTrk + process.pseudoPairsTrk + process.onePseudoPairTrk)

process.tpTreeTrk = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # choice of tag and probe pairs, and arbitration
    tagProbePairs = cms.InputTag("tpPairsTrk"),
    arbitration   = cms.string("OneProbe"),
    # probe variables: all useful ones
    variables = cms.PSet(
      KinematicVariables,
      StaOnlyVariables,
      dxyPVdzmin = cms.InputTag("muonDxyPVdzminTrk","dxyPVdzmin"),
      dzPV = cms.InputTag("muonDxyPVdzminTrk","dzPV"),
      dxyPV = cms.InputTag("muonDxyPVdzminTrk","dxyPV"),
      trackAlgo = cms.string("innerTrack.originalAlgo"),

    ),
    flags = cms.PSet(
      LowPtTriggerProbeFlags,
      TM = cms.string("isTrackerMuon"),
      SoftId = cms.string(SoftId),
      isSTA = cms.string("isStandAloneMuon"),
      Glb   = cms.string("isGlobalMuon"),
      TrackCuts = cms.string(TRACK_CUTS),
      outerValidHits = cms.string("? outerTrack.isNull() ? 0 : outerTrack.numberOfValidHits > 0"),
      InAcceptance_Ups = cms.string(InAcceptance_Ups),
    ),
    tagVariables = cms.PSet(
      TrackQualityVariables,
      GlobalTrackQualityVariables,
      CentralityVariables,
      pt  = cms.string("pt"),
      eta = cms.string("eta"),
      abseta = cms.string("abs(eta)"),
      phi = cms.string("phi"),
      nVertices = cms.InputTag("nverticesModule"),

    ),
    tagFlags = cms.PSet(
       LowPtTriggerProbeFlags,
    ),
    pairVariables = cms.PSet(
      pt = cms.string("pt"),
      y = cms.string("rapidity"),
      absy = cms.string("abs(rapidity)"),
      deltaR = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)"),
#      genWeight = cms.InputTag("genWeightInfoTrk", "genWeight"),
    ),
    pairFlags = cms.PSet(),
    isMC = cms.bool(False),
    addRunLumiInfo = cms.bool(True),
)

process.muonDxyPVdzminTrk = process.muonDxyPVdzmin.clone(
    probes = cms.InputTag("probeMuonsTrk")
)
#process.genWeightInfoTrk = process.genAdditionalInfo.clone(
#    pairTag = cms.InputTag("tpPairsTrk")
#)

process.tnpSimpleSequenceTrk = cms.Sequence(
    process.tagMuons +
    process.oneTag +
    process.probeMuonsTrk +
    process.oneProbeTrk +
    process.tpPairsTrk +
    process.onePairTrk +
    process.muonDxyPVdzminTrk +
    process.nverticesModule +
    process.centralityInfo +
    process.centralityBinInfo +
#    process.genWeightInfoTrk +
    process.tpTreeTrk
)

process.tagAndProbeTrk = cms.Path(
    process.fastFilter
    * process.fastPseudoTnPTrk
    * process.centralityBin
    * process.mergedMuons * process.patMuonsWithTriggerSequence
    * process.tnpSimpleSequenceTrk
)

process.schedule = cms.Schedule(
   process.tagAndProbe,
   process.tagAndProbeSta,
   process.tagAndProbeTrk,
)

process.RandomNumberGeneratorService.tkTracksNoJPsi = cms.PSet( initialSeed = cms.untracked.uint32(81) )
process.RandomNumberGeneratorService.tkTracksNoBestJPsi = cms.PSet( initialSeed = cms.untracked.uint32(81) )

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpJpsi_MC_PbPb_191205.root"))

from HLTrigger.Configuration.CustomConfigs import MassReplaceInputTag
process = MassReplaceInputTag(process,"offlinePrimaryVertices","offlinePrimaryVerticesRecovery")
process.offlinePrimaryVerticesRecovery.oldVertexLabel = "offlinePrimaryVertices"
