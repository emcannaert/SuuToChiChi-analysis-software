#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class DummyAnalyzer : public edm::EDAnalyzer {
public:
  explicit DummyAnalyzer(const edm::ParameterSet&) {}
  void analyze(const edm::Event&, const edm::EventSetup&) override {}
};

DEFINE_FWK_MODULE(DummyAnalyzer);
