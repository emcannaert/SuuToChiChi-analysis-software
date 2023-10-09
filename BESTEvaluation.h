#ifndef BEST_EVALUATION_H
#define BEST_EVALUATION_H

#include <Math/VectorUtil.h>
//#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "PhysicsTools/TensorFlow/interface/TensorFlow.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
//#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
//#include "DataFormats/Common/interface/AssociationMap.h"
#include "CacheHandler.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
//#include "DataFormats/PatCandidates/interface/PackedCandidate.h"


class BESTEvaluation {
 public:
  BESTEvaluation(const CacheHandler* cache)
    : isConfigured_(false),
    cache_(cache)
    {}
  void configure(const edm::ParameterSet&);
  //std::vector<float> getPrediction(const std::vector<float> &BESTInputs);
  std::vector<float> getPrediction(std::map<std::string, float> &BESTInputs);

  //std::vector<float> getPrediction(const float HImage[31][31], const float TImage[31][31], const float WImage[31][31], const float ZImage[31][31], const std::vector<float> &BESTInputs);
  ~BESTEvaluation() {}
  std::vector<std::string> listOfBESTVars;


 private:
  //static float getScaledValue(float value, float mean, float sigma){
    // float result = (value-mean)/sigma;
    //return result;
  //}

  static float getScaledValue(float value, int scaler, float param1, float param2){
    float result;
    // std::unordered_map<std::string,int> const scalerInt = { {"NoScale",0}, {"MinMax",1}, {"Standard",2}, {"MaxAbs",3} };
    switch(scaler){
      case 0: // NoScale: result = value
        result = value; break;
      case 1: // MinMax: result = ( value - var_min[param1] ) / ( var_max[param2] - var_min[param1] )
        result = (value-param1)/(param2-param1); break;
      case 2: // Standard: result = (value - mean[param2]) / std_dev[param1]
        result = (value-param2)/param1; break;
      case 3: // MaxAbs: result = value / max_value[param1]
        result = value/param1; break;
      default: // If one of the four scalers is not found, something bad is happening
        throw cms::Exception("BESTEvaluation") << "invalid scaler = " << scaler; break;
    }
    return result;
  }

  bool isConfigured_;
  const CacheHandler* cache_;
  std::string name_;
  edm::FileInPath path_;
  edm::FileInPath paramPath_;
  std::map< std::string, std::tuple<std::string,float,float> > paramDict_; 
  //std::vector<float> means_;
  //std::vector<float> sigmas_;
  std::vector<tensorflow::TensorShape> inputShapes_;
  std::vector<std::string> inputNames_;
  tensorflow::NamedTensorList inputTensors_;
  //size_t kHiggs_;
  //size_t kTop_;
  //size_t kW_;
  //size_t kZ_;
  size_t kBEST_;
  std::string outputName_;
  //int NumBESTInputs_ = 94;
  //int NumBESTInputs_ = 142;
  int NumBESTInputs_ = 73;
  std::unordered_map<std::string,int> scalerStringToInt_ = { {"NoScale",0}, {"MinMax",1}, {"Standard",2}, {"MaxAbs",3} };

};
#endif


