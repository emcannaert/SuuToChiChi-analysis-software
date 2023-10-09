#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_29/src/BESTEvaluation.h"
#include <fstream>
#include <sstream>

//========================================================================================
// Loads the BEST Neural Network using the tensforflow interface -------------------------
//----------------------------------------------------------------------------------------

void BESTEvaluation::configure(const edm::ParameterSet& iConfig){
  if(isConfigured_) return;
  name_ = iConfig.getParameter<std::string>("name");
  path_ = iConfig.getParameter<edm::FileInPath>("path");
  paramPath_ = iConfig.getParameter<edm::FileInPath>("means");

  std::string fullParamPath = paramPath_.fullPath();
  std::ifstream inputParamsFile(fullParamPath);
  std::string line, word, besVar, scaler;
  float param1, param2;

  while (std::getline(inputParamsFile, line)) {
    std::istringstream ss(line);
    std::getline(ss,word,',');
    besVar = word;
    std::getline(ss,word,',');
    scaler = word;
    std::getline(ss,word,',');
    param1 = std::stof(word);
    std::getline(ss,word,',');
    param2 = std::stof(word);
    listOfBESTVars.push_back(besVar); // ordered list of bes vars
    paramDict_[besVar] = std::make_tuple(scaler, param1, param2); // dictionary containing the scaler and parameters for each bes var
  }
  inputParamsFile.close();

  // The input name needs to match the name of the input layer in the data/constantgraph.pb file
  inputNames_.push_back("input_1");
  inputShapes_.push_back(tensorflow::TensorShape{1, NumBESTInputs_});
  // kBEST is the number of different input branches. It was 4 when we used 1 dense network plus 4 CNN image branches
  kBEST_ = 0;
  // The output name needs to match the name of the output layer in the data/constantgraph.pb file
  outputName_ = "dense_4/Softmax";


  //Now set the internal tensor list to the size of your inputs

  inputTensors_.resize(inputShapes_.size());


  //Now make each element have the correct name and shape


  for (size_t i=0; i<inputShapes_.size(); i++) {
    inputTensors_[i] = tensorflow::NamedTensor(inputNames_[i], tensorflow::Tensor(tensorflow::DT_FLOAT, inputShapes_.at(i)));
  }
  //This class must be constructed after the global cache was created and passed to it
  //Get the graph from the cache

  auto graph = cache_->getGraph();

  //The rest of this is a sanity check
  for (size_t i=0; i<inputShapes_.size(); i++){
    const auto& name = graph.node(i).name();
    auto it = std::find(inputNames_.begin(), inputNames_.end(), name);
    if (it==inputNames_.end()) { //Check if input layer name is in the graph
      throw cms::Exception("BESTEvaluation")
	<< "Processing graph " << name_ << ".\n"
	<< "Unknown input name " << name;
    }

    const auto& shape = graph.node(i).attr().at("shape").shape();
    int j = std::distance(inputNames_.begin(),it); //Do inputs in correct order, even if they weren't declared in correct order
    for (int d=1; d<inputShapes_.at(j).dims(); d++) {
      if (shape.dim(d).size() != inputShapes_.at(j).dim_size(d)) {
	throw cms::Exception("BESTEvaluation")
	  << "Number of inputs in graph does not match those expected for " << name_ << ".\n"
	  << "Expected input " << j << " dim " << d << " = " << inputShapes_.at(j).dim_size(d) << "."
	  << " Found " << shape.dim(d).size() << ".";
      }
    }
  }

  const auto& outName = graph.node(graph.node_size() - 1).name();

  if (outName!=outputName_) {
    throw cms::Exception("BESTEvaluation")
      << "Processing graph " << name_ << ".\n"
      << "Unexpected output name. Expected " << outputName_ << " found " << outName << ".";
  }
  isConfigured_ = true;
}

//========================================================================================
// Get a prediction using the BEST Neural Network ----------------------------------------
//----------------------------------------------------------------------------------------

std::vector<float> BESTEvaluation::getPrediction(std::map<std::string, float> &BESTInputs){
// std::vector<float> BESTEvaluation::getPrediction(const std::vector<float> &BESTInputs){
  //std::vector<float> BESTEvaluation::getPrediction(const float HImage[31][31], const float TImage[31][31], const float WImage[31][31], const float ZImage[31][31], const std::vector<float> &BESTInputs){
  std::vector<tensorflow::Tensor> pred_vector; //vector of predictions to allow for evaluation multiple jets, but only using one at the moment
  tensorflow::Tensor prediction;
  std::vector<float> NNoutputs;

  inputTensors_.at(kBEST_).second.flat<float>().setZero();

  //Setup the BES variable inputs
  for (int n=0; n < NumBESTInputs_; n++){
    // inputTensors_.at(kBEST_).second.matrix<float>()(0, n) = getScaledValue(BESTInputs.at(n), means_[n], sigmas_[n]); //BESTInputs MUST be constructed in the correct order
    float value = BESTInputs[listOfBESTVars[n]];
    auto [scalerString, param1, param2] = paramDict_[listOfBESTVars[n]];
    inputTensors_.at(kBEST_).second.matrix<float>()(0, n) = getScaledValue(value, scalerStringToInt_[scalerString], param1, param2); //BESTInputs MUST be constructed in the correct order
  }

  //Evaluate
  tensorflow::run(&(cache_->getSession()),
                  inputTensors_,
                  {outputName_},
                  &pred_vector);


  prediction = tensorflow::Tensor(tensorflow::DT_FLOAT, {1, 4}); //6 here for the number of outputs
  for (int k = 0; k < 4; ++k) {
    const float pred = pred_vector[0].flat<float>()(k);
    if (!(pred >= 0 && pred <= 1)) {
      throw cms::Exception("BESTEvaluation")
	<< "invalid prediction = " << pred << " for pred_index = " << k;
    }
    prediction.matrix<float>()(0, k) = pred;
  }
  for (int i = 0; i < 4; i++){
    NNoutputs.push_back(prediction.matrix<float>()(0,i)); //0,5 determined by number of outputs
  }
  return NNoutputs;
}

