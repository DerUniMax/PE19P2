import pandas as pd
import argparse
import net_predictor
from net_parser import parse
from net_edges import edges

def main():
  parser = argparse.ArgumentParser()
  
  parser.add_argument('-b', '--build', action="store_true", help="""flag for forcing the program to create a new Bayesian Network depending on the input data. 
                      The predictions for the file using the --predictionfile arg will still be performed""")
  
  parser.add_argument('-d', '--dataset', default="P1_DP13_Wohnungen_X.csv",help="csv file (';' seperated) with the base dataset")
  
  parser.add_argument('-o', '--outfile', default="net.json", help='file path for the save file of the created Bayesian Network')
  
  parser.add_argument('-p', '--predictionfile', default="input.csv", help="csv file (';' seperated) with the incomplete Datasets for prediction")
  
  parser.add_argument('-n', '--netfile', default="net.json", help="json file with the Bayesian Network to use in the prediction")
  
  parser.add_argument('-pf', '--printfiles', action="store_true", help="Set if the prediction output should also be printed to files")
  
  args = parser.parse_args()
  
  predict_set = pd.read_csv(args.predictionfile, sep=";")
  
  if args.build:
    dataset = pd.read_csv(args.dataset, sep=";")

    net = parse(dataset, edges, args.outfile)
    
    prediction_results = net_predictor.predict_net(net, predict_set)
    
    # printing the prediction results
    for result in prediction_results:
      print(result)
    
  else:
    prediction_results = net_predictor.predict_file(args.netfile, predict_set)
    
    
    # printing the prediction results
    if args.printfiles:
      for (i, result) in enumerate(prediction_results):
        result.to_csv(f"output{i}.csv", sep=";")
        print(result)
    else:
      for result in prediction_results:
        print(result)

if __name__ == '__main__':
  main()