package cs446.weka.classifiers.trees;

import weka.classifiers.Classifier;
import weka.classifiers.Sourcable;
import weka.core.Attribute;
import weka.core.Capabilities;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.NoSupportForMissingValuesException;
import weka.core.RevisionUtils;
import weka.core.TechnicalInformation;
import weka.core.TechnicalInformationHandler;
import weka.core.Utils;
import weka.core.Capabilities.Capability;
import weka.core.TechnicalInformation.Field;
import weka.core.TechnicalInformation.Type;

import java.util.Enumeration;
import java.util.Random;
import java.util.Arrays;

/**
 * <!-- globalinfo-start --> Class for constructing an unpruned decision tree
 * based on the ID3 algorithm. Can only deal with nominal attributes. No missing
 * values allowed. Empty leaves may result in unclassified instances. For more
 * information see: <br/>
 * <br/>
 * R. Quinlan (1986). Induction of decision trees. Machine Learning.
 * 1(1):81-106.
 * <p/>
 * <!-- globalinfo-end -->
 * 
 * <!-- technical-bibtex-start --> BibTeX:
 * 
 * <pre>
 * &#64;article{Quinlan1986,
 *    author = {R. Quinlan},
 *    journal = {Machine Learning},
 *    number = {1},
 *    pages = {81-106},
 *    title = {Induction of decision trees},
 *    volume = {1},
 *    year = {1986}
 * }
 * </pre>
 * <p/>
 * <!-- technical-bibtex-end -->
 * 
 * <!-- options-start --> Valid options are:
 * <p/>
 * 
 * <pre>
 * -D
 *  If set, classifier is run in debug mode and
 *  may output additional info to the console
 * </pre>
 * 
 * <!-- options-end -->
 * 
 * @author Eibe Frank (eibe@cs.waikato.ac.nz)
 * @version $Revision: 6404 $
 */
public class SGD extends Classifier implements TechnicalInformationHandler,
	Sourcable {

    /** for serialization */
    static final long serialVersionUID = -2693678647096322561L;

    /** Class value if node is leaf. */
    private double m_ClassValue;

    /** Class attribute of dataset. */
    private Attribute m_ClassAttribute;

    private double[] wTheta = null;
    private double[] predictedValues = null;
    private double threshold = 0.001;
    private double learningRate = 0.001;

    /**
     * Returns a string describing the classifier.
     * 
     * @return a description suitable for the GUI.
     */
    public String globalInfo() {

	return "Class for constructing an unpruned decision tree based on the ID3 "
		+ "algorithm. Can only deal with nominal attributes. No missing values "
		+ "allowed. Empty leaves may result in unclassified instances. For more "
		+ "information see: \n\n"
		+ getTechnicalInformation().toString();
    }

    /**
     * Returns an instance of a TechnicalInformation object, containing detailed
     * information about the technical background of this class, e.g., paper
     * reference or book this class is based on.
     * 
     * @return the technical information about this class
     */
    public TechnicalInformation getTechnicalInformation() {
	TechnicalInformation result;

	result = new TechnicalInformation(Type.ARTICLE);
	result.setValue(Field.AUTHOR, "R. Quinlan");
	result.setValue(Field.YEAR, "1986");
	result.setValue(Field.TITLE, "Induction of decision trees");
	result.setValue(Field.JOURNAL, "Machine Learning");
	result.setValue(Field.VOLUME, "1");
	result.setValue(Field.NUMBER, "1");
	result.setValue(Field.PAGES, "81-106");

	return result;
    }

    /**
     * Returns default capabilities of the classifier.
     * 
     * @return the capabilities of this classifier
     */
    public Capabilities getCapabilities() {
	Capabilities result = super.getCapabilities();
	result.disableAll();

	// attributes
	result.enable(Capability.NOMINAL_ATTRIBUTES);

	// class
	result.enable(Capability.NOMINAL_CLASS);
	result.enable(Capability.MISSING_CLASS_VALUES);

	// instances
	result.setMinimumNumberInstances(0);

	return result;
    }

    /**
     * DONE
     * Builds SGD classifier.
     * 
     * @param data
     *            the training data
     * @exception Exception
     *                if classifier can't be built successfully
     */
    public void buildClassifier(Instances data) throws Exception {

	// can classifier handle the data?
	getCapabilities().testWithFail(data);

	// remove instances with missing class
	data = new Instances(data);
	data.deleteWithMissingClass();

	// initialize w and theta, storing w and theta in the same array
	System.out.print("abc");
	System.out.print(data.numAttributes());
	wTheta = new double[data.numAttributes()];
	Arrays.fill(wTheta, 0);
	
	// Allocate array for w and theta changes during SGD
	// The array does not need to initialize because each of the elements will be updated in every iteration
	predictedValues = new double[data.numInstances()];

	double error = 0;
	do{
		error = performSGD(data);
		//System.out.print(error);
		//System.out.print("\n");
	}while(error > threshold);
	System.out.print(error);
	System.out.print("\n");
    }

    private double performSGD(Instances data) throws Exception{
        // update rules: w_i = w_i + delta(w_i) = w_i - stepSize * derivative(Error(w_i)) 
    	//                   = w_i - stepSize * sum{d in D}(t_d -o_d)(-x_i,d)
    	//					 = w_i - stepSize * sum{d in D}(o_d - t_d)(x_i,d)
    	double currentError = updatePredictedValuesError(data);
    	if(currentError <= threshold)
    		return currentError;
    	// deal with theta separatly
    	//System.out.print("abd");
    	for(int i = 0; i < wTheta.length; i++){
    		Enumeration instEnum = data.enumerateInstances();
    		int indexCounter = 0;
    		double sum = 0;
    		if(i != wTheta.length-1){
    			while (instEnum.hasMoreElements()) {
    				Instance inst = (Instance) instEnum.nextElement();
    				sum += predictedValues[indexCounter] * inst.value(i);
				indexCounter++;
    			}
    		}
    		else{
    			while (instEnum.hasMoreElements()) {
    				Instance inst = (Instance) instEnum.nextElement();
    				sum += predictedValues[indexCounter];
				indexCounter++;
    			}
    		}
            wTheta[i] -= learningRate * sum;
    	}
    	return currentError;
    }
    
    private double updatePredictedValuesError(Instances data) throws Exception{
    	double error = 0;
    	Enumeration instEnum = data.enumerateInstances();
	int indexCounter = 0;
        while (instEnum.hasMoreElements()) {
            double predictedValue = 0;
            Instance inst = (Instance) instEnum.nextElement();
            for(int i = 0; i < wTheta.length-1; i++){
            	predictedValue += wTheta[i] * inst.value(i);
            }
	    if((predictedValue+wTheta[wTheta.length-1])>0.5)
		 predictedValues[indexCounter] = 1.0 - inst.classValue();
	    else
		 predictedValues[indexCounter] = 0.0 - inst.classValue();
            //predictedValues[indexCounter] = predictedValue + wTheta[wTheta.length-1] - inst.classValue();
            error += predictedValues[indexCounter] *predictedValues[indexCounter];
            indexCounter++;
        }
	//System.out.print(error);
	//System.out.print("\n");
        return (0.5 * error);
    }


    /**
     * DONE
     * Classifies a given test instance using the decision tree.
     * 
     * @param instance
     *            the instance to be classified
     * @return the classification
     * @throws NoSupportForMissingValuesException
     *             if instance has missing values
     */
    public double classifyInstance(Instance instance) throws NoSupportForMissingValuesException {
	double predictedValue = 0;
	if (instance.hasMissingValue()) {
	    throw new NoSupportForMissingValuesException(
		    "SGD: no missing values, " + "please.");
	}

	for(int i = 0; i < wTheta.length-1; i++){
    	    predictedValue += wTheta[i] * instance.value(i);
    	}

	predictedValue += wTheta[wTheta.length-1];
	//return 1;
	if(predictedValue > 0.5)
	    return 1;
	else
	    return 0;
    }

    /**
     * Computes class distribution for instance using decision tree.
     * 
     * @param instance
     *            the instance for which distribution is to be computed
     * @return the class distribution for the given instance
     * @throws NoSupportForMissingValuesException
     *             if instance has missing values
     */

    /**
     * TODO
     * Prints the decision tree using the private toString method from below.
     * 
     * @return a textual description of the classifier
     */
    public String toString() {
	return "SGD\n";
    }

    //TODO
    public void setParameter(double rate, double errorTheshold) {
	this.learningRate = rate;
	this.threshold = errorTheshold;
	System.out.print(learningRate);
	System.out.print("\n");
	System.out.print(threshold);
    }

    /**
     * Returns a string that describes the classifier as source. The classifier
     * will be contained in a class with the given name (there may be auxiliary
     * classes), and will contain a method with the signature:
     * 
     * <pre>
     * <code>
     * public static double classify(Object[] i);
     * </code>
     * </pre>
     * 
     * where the array <code>i</code> contains elements that are either Double,
     * String, with missing values represented as null. The generated code is
     * public domain and comes with no warranty. <br/>
     * Note: works only if class attribute is the last attribute in the dataset.
     * 
     * @param className
     *            the name that should be given to the source class.
     * @return the object source described by a string
     * @throws Exception
     *             if the source can't be computed
     */
    public String toSource(String className) throws Exception {
	StringBuffer result;
	int id;

	result = new StringBuffer();

	result.append("class " + className + " {\n");
	result
		.append("  private static void checkMissing(Object[] i, int index) {\n");
	result.append("    if (i[index] == null)\n");
	result.append("      throw new IllegalArgumentException(\"Null values "
		+ "are not allowed!\");\n");
	result.append("  }\n\n");
	result.append("  public static double classify(Object[] i) {\n");
	id = 0;
	result.append("    return node" + id + "(i);\n");
	result.append("  }\n");
	result.append("}\n");

	return result.toString();
    }

    /**
     * Returns the revision string.
     * 
     * @return the revision
     */
    public String getRevision() {
	return RevisionUtils.extract("$Revision: 6404 $");
    }

    /**
     * Main method.
     * 
     * @param args
     *            the options for the classifier
     */
    public static void main(String[] args) {
	runClassifier(new SGD(), args);
    }
}
