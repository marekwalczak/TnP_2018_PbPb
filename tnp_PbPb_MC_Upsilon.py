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
process.triggerResultsFilter.triggerConditions = cms.vstring( 'HLT_HIUPC_SingleMuOpen_NotMBHF2AND_v*' )
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



# naw TRG 
InAcceptance_Ups_TRG = '( (abs(eta) < 2.4)    &&  ( (pt > 3.45) || (abs(eta)>0.3 &&  abs(eta)<1.1 &&  pt>3.3 )    ||  ( (pt > ((-1.15/0.35)*abs(eta) + 6.91429)) && (pt > 2.15) )    ||  ( (abs(eta) > 1.45) && (abs(eta) < 1.65) && (pt > 2.15))  ||  ( (pt > ((-0.95/0.45)*abs(eta) + 5.63333)) &&  (pt > 1.2) && (pt <= 2.15) ) ) )'

# new SoftID 
InAcceptance_Ups_ID = '( (abs(eta) < 2.4)    &&  ( ( pt > 3.3)     ||  ( (pt > (-4.0*abs(eta) + 7.3)) && (pt > 2.1) )    ||  ( (abs(eta) > 1.3) && (pt < 2.1) && (pt > 1.53))  ||  ( (pt > (-1.325*abs(eta) + 3.2525)) &&  (pt > 1.0) && (pt <= 1.53) ) ))'





from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.mergedMuons = cms.EDProducer("CaloMuonMerger",
    mergeTracks = cms.bool(True),
    mergeCaloMuons = cms.bool(False), # AOD
    muons     = cms.InputTag("muons"),
    caloMuons = cms.InputTag("calomuons"),
    tracks    = cms.InputTag("generalTracks"),
    minCaloCompatibility = calomuons.minCaloCompatibility,
    ## Apply some minimal pt cut
    muonsCut     = cms.string(InAcceptance_Ups_ID + " && track.isNonnull"),
    caloMuonsCut = cms.string(InAcceptance_Ups_ID),
    tracksCut    = cms.string(InAcceptance_Ups_ID),
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
TightIdReco = "isGlobalMuon && isPFMuon && globalTrack.normalizedChi2 < 10 && globalTrack.hitPattern.numberOfValidMuonHits > 0 && numberOfMatchedStations > 1 && track.hitPattern.trackerLayersWithMeasurement > 5 && track.hitPattern.numberOfValidPixelHits > 0"
### Trigger
LowPtTriggerProbeFlags = cms.PSet(

    # Double Muon Trigger Paths
    HLT_HIUPC_DoubleMu0_NotMBHF2AND_v1 = cms.string("!triggerObjectMatchesByPath('HLT_HIUPC_DoubleMu0_NotMBHF2AND_v*',1,0).empty()"),
    # Single Muon Trigger Paths
    HLT_HIUPC_SingleMu0_NotMBHF2AND_v1 = cms.string("!triggerObjectMatchesByPath('HLT_HIUPC_SingleMu0_NotMBHF2AND_v*',1,0).empty()"),
    HLT_HIUPC_SingleMuOpen_NotMBHF2AND_v1 = cms.string("!triggerObjectMatchesByPath('HLT_HIUPC_SingleMuOpen_NotMBHF2AND_v*',1,0).empty()"),

    # Double Muon Trigger Filters    
    HLT_HIUPC_DoubleMu0_NotMBHF2AND_Filter = cms.string("!triggerObjectMatchesByFilter('hltL1sDoubleMu0NotMBHF2AND').empty()"),
    # Single Muon Trigger Filters
    HLT_HIUPC_SingleMu0_NotMBHF2AND_Filter = cms.string("!triggerObjectMatchesByFilter('hltL1sSingleMu0NotMBHF2AND').empty()"),
    HLT_HIUPC_SingleMuOpen_NotMBHF2AND_Filter = cms.string("!triggerObjectMatchesByFilter('hltL1sSingleMuOpenNotMBHF2AND').empty()"),
)
### Tracking
TRACK_CUTS = "track.isNonnull"


#    _      _______            
#   | |    |__   __|           
#   | |_ _ __ | |_ __ ___  ___ 
#   | __| '_ \| | '__/ _ \/ _ \
#   | |_| |_) | | | |  __/  __/
#    \__| .__/|_|_|  \___|\___|
#       | |                    
#       |_|                    




## ==== Tag muons
process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string(InAcceptance_Ups_ID+" && "+SoftId+" && !triggerObjectMatchesByPath('HLT_HIUPC_SingleMu0_NotMBHF2AND_v*',1,0).empty()"), # +" && !triggerObjectMatchesByPath('HLT_HIUPC_SingleMu0_NotMBHF2AND_v*',1,0).empty()"
)
process.oneTag = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagMuons"), minNumber = cms.uint32(1))
process.pseudoTag = cms.EDFilter("MuonSelector",
    src = cms.InputTag("mergedMuons"),
    cut = cms.string(InAcceptance_Ups_ID+" && "+SoftId),
)
process.onePseudoTag = process.oneTag.clone(src = cms.InputTag("pseudoTag"))

## ==== Probe muons
process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string(TRACK_CUTS + ' && ' + InAcceptance_Ups_ID),
)
process.oneProbe = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("probeMuons"), minNumber = cms.uint32(1))
process.pseudoProbe = cms.EDFilter("MuonSelector",
    src = cms.InputTag("mergedMuons"),
    cut = process.probeMuons.cut,
)
process.onePseudoProbe = process.oneProbe.clone(src = cms.InputTag("pseudoProbe"))

## ==== Tag and Probe muon pairs
process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('8.5 < mass < 10.5'),
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
        TrackCuts = cms.string(TRACK_CUTS),
        InAcceptance_Ups_TRG = cms.string(InAcceptance_Ups_TRG),
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
        InAcceptance_Ups_TRG = cms.string(InAcceptance_Ups_TRG),
        TightIdReco = cms.string(TightIdReco),
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
    mass  = cms.double(9.4603)
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





process.schedule = cms.Schedule(
   process.tagAndProbe,
   #process.tagAndProbeSta,
   #process.tagAndProbeTrk,
)

process.RandomNumberGeneratorService.tkTracksNoJPsi = cms.PSet( initialSeed = cms.untracked.uint32(81) )
process.RandomNumberGeneratorService.tkTracksNoBestJPsi = cms.PSet( initialSeed = cms.untracked.uint32(81) )

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpJpsi_MC_PbPb.root"))

from HLTrigger.Configuration.CustomConfigs import MassReplaceInputTag
process = MassReplaceInputTag(process,"offlinePrimaryVertices","offlinePrimaryVerticesRecovery")
process.offlinePrimaryVerticesRecovery.oldVertexLabel = "offlinePrimaryVertices"
