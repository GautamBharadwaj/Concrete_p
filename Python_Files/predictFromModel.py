import pandas as pd
from Python_Files import file_methods
from Python_Files import preprocessing
from Python_Files.prediction_rawValidation import Prediction_Data_validation
import os
import glob


class prediction:

    def __init__(self,batch_files_path,pred_schema_path,current_working_directory):
        self.pred_data_val = Prediction_Data_validation(batch_files_path,pred_schema_path)
        self.current_working_directory = current_working_directory

    def predictionFromModel(self):
        try:
            self.pred_data_val.deletePredictionFile() #deletes the existing prediction file from last run!
            #data_getter=data_loader_prediction.Data_Getter_Pred(self.file_object,self.log_writer)
            #data=data_getter.get_data()
            Good_csv_path = self.current_working_directory + '//Prediction_Raw_Files_Validated//Good_Raw//'
            all_files  = glob.glob(os.path.join(Good_csv_path , "*.csv"))
            data = pd.concat(map(pd.read_csv, all_files))
            #code change
            # wafer_names=data['Wafer']
            # data=data.drop(labels=['Wafer'],axis=1)

            preprocessor=preprocessing.Preprocessor()

            is_null_present,cols_with_missing_values=preprocessor.is_null_present(data)
            if(is_null_present):
                data=preprocessor.impute_missing_values(data)

            data  = preprocessor.logTransformation(data)

            #scale the prediction data
            data_scaled = pd.DataFrame(preprocessor.standardScalingData(data),columns=data.columns)

            #data=data.to_numpy()
            file_loader=file_methods.File_Operation()
            kmeans=file_loader.load_model('KMeans')

            clusters=kmeans.predict(data_scaled)#drops the first column for cluster prediction
            data_scaled['clusters']=clusters
            clusters=data_scaled['clusters'].unique()
            result=[] # initialize blank list for storing predicitons

            for i in clusters:
                cluster_data= data_scaled[data_scaled['clusters']==i]
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                for val in (model.predict(cluster_data.values)):
                    result.append(val)
            result = pd.DataFrame(result,columns=['Predictions'])
            path="Predictions.csv"
            result.to_csv(f"{path}",header=True) #appends result to prediction file
        except Exception as ex:
            raise ex
        return path,result

            # old code
            # i=0
            # for row in data:
            #     cluster_number=kmeans.predict([row])
            #     model_name=file_loader.find_correct_model_file(cluster_number[0])
            #
            #     model=file_loader.load_model(model_name)
            #     #row= sparse.csr_matrix(row)
            #     result=model.predict([row])
            #     if (result[0]==-1):
            #         category='Bad'
            #     else:
            #         category='Good'
            #     self.predictions.write("Wafer-"+ str(wafer_names[i])+','+category+'\n')
            #     i=i+1
            #     self.log_writer.log(self.file_object,'The Prediction is :' +str(result))
            # self.log_writer.log(self.file_object,'End of Prediction')
            #print(result)




