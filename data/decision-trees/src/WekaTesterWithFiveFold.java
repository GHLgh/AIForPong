package cs446.homework2;

import java.io.File;
import java.io.FileReader;

import weka.classifiers.Evaluation;
import weka.core.Instances;
import cs446.weka.classifiers.trees.Id3;
import cs446.weka.classifiers.trees.SGD;

public class WekaTesterWithFiveFold {

    public static void main(String[] args) throws Exception {

	if (args.length != 12) {
	    System.err.println("Usage: WekaTester arff-file");
	    System.exit(-1);
	}

	//Five Fold Section
	for(int i = 0; i < 5; i++){
	    // Load the data
	    // Training set
	    Instances trainingData = new Instances(new FileReader(new File(args[2*i])));
	    // Testing set
	    Instances testingData = new Instances(new FileReader(new File(args[2*i+1])));

	    // The last attribute is the class label
	    trainingData.setClassIndex(trainingData.numAttributes() - 1);
	    testingData.setClassIndex(testingData.numAttributes() - 1);

	    String id3 = "Id3";
	    if(id3.equals(args[10])){
		int depth = Integer.parseInt(args[11]);
		// Create a new ID3 classifier. This is the modified one where you can
   		// set the depth of the tree.
		Id3 classifier = new Id3();

		// An example depth. If this value is -1, then the tree is grown to full
		// depth.
	   	classifier.setMaxDepth(depth);

	    	// Train
	    	classifier.buildClassifier(trainingData);

	    	// Print the classfier
	    	System.out.println(classifier);
	    	System.out.println();

	    	// Evaluate on the test set
	    	Evaluation evaluation = new Evaluation(testingData);
	    	evaluation.evaluateModel(classifier, testingData);
	    	System.out.println(evaluation.toSummaryString());
	    }
	    else{
		double learningRate = Double.parseDouble(args[10]);
		double theshold = Double.parseDouble(args[11]);

		SGD classifier = new SGD();
		classifier.setParameter(learningRate, theshold);
		classifier.buildClassifier(trainingData);

                // Print the classfier
                System.out.println(classifier);
                System.out.println();

                // Evaluate on the test set
                Evaluation evaluation = new Evaluation(testingData);
                evaluation.evaluateModel(classifier, testingData);
                System.out.println(evaluation.toSummaryString());

	    }
	}
    }
}
