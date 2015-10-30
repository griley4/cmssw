#Grant Riley October 27 2015

## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.source = cms.Source("PoolSource",
                duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
                skipEvents = cms.untracked.uint32(0),
                fileNames = cms.untracked.vstring(
                        'file:/uscms_data/d3/griley4/UpsilonTest/HuntForMoreStatistics/CMSSW_5_3_7_patch5/src/C8A43BFC-058F-E211-8E2B-003048678FB8.root'
                        )
                )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.GlobalTag.globaltag = cms.string('FT_53_V21_AN3::All')
#remove MC Matching for Real data
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, names=['All'],outputModules=[])
# switch on PAT trigger info
from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTrigger( process )
#try to trigger skim?
process.triggerSelection = cms.EDFilter( "TriggerResultsFilter",
                triggerConditions = cms.vstring(
                        'HLT_Dimuon0_Upsilon_Muon_v*',
                        'HLT_Dimuon0_Jpsi_Muon_v*' ),
                hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
                l1tResults = cms.InputTag( "gtDigis" ),
                l1tIgnoreMask = cms.bool( False ),
                l1techIgnorePrescales = cms.bool( False ),
                daqPartitions = cms.uint32( 1 ),
                throw = cms.bool( True )
                )
process.TrigSkim = cms.Path(process.triggerSelection)
#make J/Psi cands from muons
##Add Muon candidates
from PhysicsTools.PatAlgos.tools.muonTools import *
process.goodMuons = cms.EDFilter("MuonSelector",
                src = cms.InputTag("patMuons"),
                cut = cms.string(""),
                )
process.makeGoodMuons = cms.Path(process.goodMuons)
process.UpsCand = cms.EDProducer("CandViewShallowCloneCombiner",
                decay = cms.string('goodMuons@+ goodMuons@-'),
                cut = cms.string(''),
                name = cms.string('Upsilon_Candidate_Grant')
                )
process.makeUpsCand = cms.Path(process.UpsCand)
process.DiMuCand = cms.EDProducer("CandViewShallowCloneCombiner",
                decay = cms.string('goodMuons@+ goodMuons@-'),
                cut = cms.string(''),
                name = cms.string('Dimuon_Candidate_Grant')
                )
process.makeDiMuCand = cms.Path(process.DiMuCand)
process.FourMuCand= cms.EDProducer("CandViewShallowCloneCombiner",
                decay = cms.string('UpsCand DiMuCand'),
                cut = cms.string(''),
                name = cms.string('Fourmuon_Candidate_Grant')
                )
process.makeFourMuCand = cms.Path(process.FourMuCand)
## let it run
process.pat = cms.Path(
                process.patDefaultSequence
                )

#produce output

process.out = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('patUTTuple.root'),
## save only events passing the full path
                SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('TrigSkim') ),
                ## save PAT output; you need a '*' to unpack the list of commands
#                outputCommands = cms.untracked.vstring('drop *', 'keep *reco*', 'keep *pat*', 'keep *hlt*)


                )
process.outpath = cms.EndPath(process.out)
# Schedule
process.schedule = cms.Schedule(process.TrigSkim,process.pat,process.makeGoodMuons,process.makeUpsCand,process.makeDiMuCand,process.makeFourMuCand,process.outpath)

