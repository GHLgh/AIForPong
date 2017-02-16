#!/bin/bash

mkdir bin

make

# Generate the example features (first and last characters of the
# first names) from the entire dataset. This shows an example of how
# the featurre files may be built. Note that don't necessarily have to
# use Java for this step.

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold1 ./../badges.fold1.test.arff

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold2 ../badges/badges.modified.data.fold3 ../badges/badges.modified.data.fold4 ../badges/badges.modified.data.fold5 ./../badges.fold1.train.arff

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold2 ./../badges.fold2.test.arff

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold1 ../badges/badges.modified.data.fold3 ../badges/badges.modified.data.fold4 ../badges/badges.modified.data.fold5 ./../badges.fold2.train.arff

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold3 ./../badges.fold3.test.arff

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold1 ../badges/badges.modified.data.fold2 ../badges/badges.modified.data.fold4 ../badges/badges.modified.data.fold5 ./../badges.fold3.train.arff

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold4 ./../badges.fold4.test.arff

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold1 ../badges/badges.modified.data.fold2 ../badges/badges.modified.data.fold3 ../badges/badges.modified.data.fold5 ./../badges.fold4.train.arff

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold5 ./../badges.fold5.test.arff

java -cp lib/weka.jar:bin cs446.homework2.FeatureGenerator ../badges/badges.modified.data.fold1 ../badges/badges.modified.data.fold2 ../badges/badges.modified.data.fold3 ../badges/badges.modified.data.fold4 ./../badges.fold5.train.arff


# Using the features generated above, train a decision tree classifier
# to predict the data. This is just an example code and in the
# homework, you should perform five fold cross-validation. 
#java -cp lib/weka.jar:bin cs446.homework2.WekaTester ./../badges.example.arff
java -cp lib/weka.jar:bin cs446.homework2.WekaTesterWithFiveFold ./../badges.fold1.train.arff ./../badges.fold1.test.arff ./../badges.fold2.train.arff ./../badges.fold2.test.arff ./../badges.fold3.train.arff ./../badges.fold3.test.arff ./../badges.fold4.train.arff ./../badges.fold4.test.arff ./../badges.fold5.train.arff ./../badges.fold5.test.arff Id3 4

java -cp lib/weka.jar:bin cs446.homework2.WekaTesterWithFiveFold ./../badges.fold1.train.arff ./../badges.fold1.test.arff ./../badges.fold2.train.arff ./../badges.fold2.test.arff ./../badges.fold3.train.arff ./../badges.fold3.test.arff ./../badges.fold4.train.arff ./../badges.fold4.test.arff ./../badges.fold5.train.arff ./../badges.fold5.test.arff 0.00001 0.00001

