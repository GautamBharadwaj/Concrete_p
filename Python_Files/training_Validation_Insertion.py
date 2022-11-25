from datetime import datetime
from Python_Files.training_rawValidation import Raw_Data_validation
from Python_Files.training_DataTransformation import dataTransform

class train_validation:
    def __init__(self,batch_files_path,training_schema_path):
        self.raw_data = Raw_Data_validation(batch_files_path,training_schema_path)
        self.dataTransform = dataTransform()

    def train_validation(self):
        try:
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()
            regex = self.raw_data.manualRegexCreation()
            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            
            self.raw_data.validateColumnLength(noofcolumns)
            self.raw_data.validateMissingValuesInWholeColumn()
            #self.raw_data.deleteExistingGoodDataTrainingFolder()
            #self.raw_data.moveBadFilesToArchiveBad()

        except Exception as e:
            raise e









