from Python_Files.trainingModel import trainModel
from Python_Files.training_Validation_Insertion import train_validation
from Python_Files.prediction_Validation_Insertion import pred_validation
from Python_Files.predictFromModel import prediction
import os

current_working_directory = os.getcwd().replace("\\","//")

training_files_path  = f"{current_working_directory}//Input//Training_Batch_Files"
pred_file_path       = f"{current_working_directory}//Input//Prediction_Batch_files"
training_schema_path = f"{current_working_directory}//Python_Files"
pred_schema_path     = f"{current_working_directory}//Python_Files"

train_valObj = train_validation(training_files_path,training_schema_path) #object initialization
train_valObj.train_validation()#calling the training_validation function
trainModelObj = trainModel(current_working_directory)
trainModelObj.trainingModel()

pred_val = pred_validation(pred_file_path,pred_schema_path) #object initialization
pred_val.prediction_validation() #calling the prediction_validation function
pred = prediction(pred_file_path,pred_schema_path,current_working_directory) #object initialization
path = pred.predictionFromModel() # predicting for dataset present in database




