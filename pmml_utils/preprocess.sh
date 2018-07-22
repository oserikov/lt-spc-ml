#!/bin/bash

BASE_WORKING_DIR=$1
PMML_CONVERTER_JAR="$BASE_WORKING_DIR/pmml_utils/jpmml-xgboost-executable-1.3.1.jar"
MODEL_INPUT="xgb.model"
FMAP_FILE="$BASE_WORKING_DIR/pmml_utils/xgb.model.features"
PMML_OUTPUT="spc.model.pmml"

mkdir "$BASE_WORKING_DIR/models"
mv  "$BASE_WORKING_DIR"/*RULE* "$BASE_WORKING_DIR/models/"
for d in $BASE_WORKING_DIR/models/*/
do
        cd "$d"
        java -jar $PMML_CONVERTER_JAR --fmap-input $FMAP_FILE --model-input $MODEL_INPUT --pmml-output $PMML_OUTPUT
        cd ../..
done
