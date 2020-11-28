from CRABClient.UserUtilities import config
config = config()

config.section_('General')
config.General.requestName = 'data_20201127'
config.General.workArea = 'crab_projects_Acc2'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'tnp_PbPb_data.py'
config.JobType.maxMemoryMB = 4000
config.JobType.maxJobRuntimeMin = 1220
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.inputDataset ='/HIForward/HIRun2018A-04Apr2019-v1/AOD'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'global'
config.Data.unitsPerJob = 50
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/HI/PromptReco/Cert_326381-327564_HI_PromptReco_Collisions18_JSON_HF_and_MuonPhys.txt'
config.Data.runRange = '326381-327564'
config.Data.outLFNDirBase = '/store/user/%s/TagAndProbe/PbPb2018/TnP/%s' % ("mwalczak", config.General.requestName)
config.Data.publication = False
config.Data.outputDatasetTag = config.General.requestName

config.section_('Site')
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_US_*','T2_US_*','T1_FR_*','T2_FR_*','T2_CH_CERN']
#config.Site.storageSite = 'T2_CH_CERN'
config.Site.storageSite = 'T2_US_Vanderbilt'
#config.Site.storageSite = 'T2_PL_Swierk'
