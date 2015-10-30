import FWCore.ParameterSet.Config as cms

process = cms.Process("Test")

process.source = cms.Source("PoolSource",
                fileNames = cms.untracked.vstring(
                        "file:/uscms_data/d3/griley4/UpsilonTest/HuntForMoreStatistics/CMSSW_5_3_7_patch5/src/Run2012C/patUTTuple.root"
                        )
                )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.MessageLogger = cms.Service("MessageLogger")

## ---
## This is an example of the use of the plain edm::Tuple dumper to analyze pat::Muons
process.patMuonAnalyzer = cms.EDProducer(
                "CandViewNtpProducer", 
                src = cms.InputTag("patMuons"),
                lazyParser = cms.untracked.bool(True),
                prefix = cms.untracked.string(""),
                eventInfo = cms.untracked.bool(True),
                variables = cms.VPSet(
                        cms.PSet(
                                tag = cms.untracked.string("pt"),
                                quantity = cms.untracked.string("pt")
                                ),
                        cms.PSet(
                                tag = cms.untracked.string("energy"),
                                quantity = cms.untracked.string("energy")
                                ),
                        cms.PSet(
                                tag = cms.untracked.string("eta"),
                                quantity = cms.untracked.string("eta")
                                ),
                        cms.PSet(
                                tag = cms.untracked.string("phi"),
                                quantity = cms.untracked.string("phi")
                                ),
                        )  
                )
process.patJpsiAnalyzer = cms.EDProducer(
                "CandViewNtpProducer",
                src = cms.InputTag("JPsiToMuMu"),
                lazyParser = cms.untracked.bool(True),
                prefix = cms.untracked.string(""),
                eventInfo = cms.untracked.bool(True),
                variables = cms.VPSet(
                        cms.PSet(
                                tag = cms.untracked.string("mass"),
                                quantity = cms.untracked.string("mass")
                                ),
                        )
                )

process.p = cms.Path(process.patMuonAnalyzer * process.patJpsiAnalyzer)

process.out = cms.OutputModule("PoolOutputModule",
                fileName = cms.untracked.string('edmTuple.root'),
                # save only events passing the full path
                SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                # save PAT Layer 1 output; you need a '*' to
                # unpack the list of commands 'patEventContent'
                outputCommands = cms.untracked.vstring('drop *', 'keep *_patMuonAnalyzer_*_*', 'keep *_patJpsiAnalyzer_*_*')
                )

process.outpath = cms.EndPath(process.out)
