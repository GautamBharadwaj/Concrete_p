from Python_Files.prediction_rawValidation import Prediction_Data_validation
from Python_Files.prediction_DataTransformation import dataTransformPredict

class pred_validation:
    def __init__(self,batch_files_path,pred_schema_path):
        self.raw_data = Prediction_Data_validation(batch_files_path,pred_schema_path)
        self.dataTransform = dataTransformPredict()

    def prediction_validation(self):
        try:
            LengthOfDateStampInFile,LengthOfTimeStampInFile,column_names,noofcolumns = self.raw_data.valuesFromSchema()
            regex = self.raw_data.manualRegexCreation()
            self.raw_data.validationFileNameRaw(regex,LengthOfDateStampInFile,LengthOfTimeStampInFile)
            self.raw_data.validateColumnLength(noofcolumns)
            self.raw_data.validateMissingValuesInWholeColumn()
            #self.raw_data.deleteExistingGoodDataTrainingFolder()
            #self.raw_data.moveBadFilesToArchiveBad()

        except Exception as e:
            raise e









