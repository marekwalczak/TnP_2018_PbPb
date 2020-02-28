from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.section_('General')
config.General.requestName = 'coh_jpsi_200227'
config.General.workArea = 'crab_projects_STARLIGHT'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'tnp_PbPb_MC.py'
config.JobType.maxMemoryMB = 4000
config.JobType.maxJobRuntimeMin = 2750
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.inputDataset = '/STARlight_CohJpsi2MuMu_PbPb5TeV/shuaiy-STARlight_CohJpsi2MuMu_PbPb5TeV_wIF_Reco_v1-4a15772ba976f0ddb208ff38f4df19d3/USER'
#config.Data.inputDataset = '/STARlight_InCohJpsi2MuMu_PbPb5TeV/shuaiy-STARlight_InCohJpsi2MuMu_PbPb5TeV_Reco_v1-4a15772ba976f0ddb208ff38f4df19d3/USER'
config.Data.inputDBS = 'phys03'
config.Data.unitsPerJob = 1
config.Data.splitting = 'FileBased'
config.Data.outLFNDirBase = '/store/user/%s/TagAndProbe/PbPb2018/TnP/%s' % (getUsernameFromSiteDB(), config.General.requestName)
config.Data.publication = False
config.Data.allowNonValidInputDataset = True
config.Data.outputDatasetTag = config.General.requestName

config.section_('Site')
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_FR_*','T1_US_*','T2_FR_*','T2_US_*','T2_CH_CERN']
#config.Site.storageSite = 'T2_CH_CERN'
#config.Site.storageSite = 'T2_US_Vanderbilt'
config.Site.storageSite = 'T2_PL_Swierk'
