# Doing the necessary imports
from sklearn.model_selection import train_test_split
from Python_Files import preprocessing
from Python_Files import training_clustering as clustering
from Python_Files import training_tuner as tuner
from Python_Files import file_methods
import pandas as pd
import os
import glob

#Creating the common Logging object


class trainModel:

    def __init__(self,current_working_directory):
        self.current_working_directory = current_working_directory

    def trainingModel(self):
        # Logging the start of Training
        try:
            # Getting the data from the source
            Good_csv_path = self.current_working_directory + '//Training_Raw_files_validated//Good_Raw//'
            all_files  = glob.glob(os.path.join(Good_csv_path , "*.csv"))
            data = pd.concat(map(pd.read_csv, all_files))
            
            preprocessor=preprocessing.Preprocessor()
            is_null_present,cols_with_missing_values=preprocessor.is_null_present(data)
            if(is_null_present):
                data=preprocessor.impute_missing_values(data) # missing value imputation
            X, Y = preprocessor.separate_label_feature(data, label_column_name='Concrete_compressive _strength')
            X = preprocessor.logTransformation(X)
            kmeans=clustering.KMeansClustering() # object initialization.
            number_of_clusters=kmeans.elbow_plot(X)  #  using the elbow plot to find the number of optimum clusters

            # Divide the data into clusters
            X=kmeans.create_clusters(X,number_of_clusters)

            #create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels']=Y

            # getting the unique clusters from our dataset
            list_of_clusters=X['Cluster'].unique()
            Accuracy_df = pd.DataFrame(columns = ['Algorithm','accuracy'])
            for i in list_of_clusters:
                cluster_data=X[X['Cluster']==i] # filter the data for one cluster

                # Prepare the feature and Label columns
                cluster_features=cluster_data.drop(['Labels','Cluster'],axis=1)
                cluster_label= cluster_data['Labels']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3, random_state=36)

                x_train_scaled = preprocessor.standardScalingData(x_train)
                x_test_scaled = preprocessor.standardScalingData(x_test)

                model_finder=tuner.Model_Finder() # object initialization

                #getting the best model for each of the clusters
                best_model_name,best_model=model_finder.get_best_model(x_train_scaled,y_train,x_test_scaled,y_test)
                print(f"Accuracy:{best_model.score(x_test_scaled, y_test)} for model {best_model_name}")
                Accuracy_df = Accuracy_df.append({'Algorithm': best_model_name, 'accuracy': best_model.score(x_test_scaled, y_test)}, ignore_index=True)

                #saving the best model to the directory.
                file_op = file_methods.File_Operation()
                save_model=file_op.save_model(best_model,best_model_name+str(i))
            Accuracy_df.to_csv(self.current_working_directory + '//Accuracy.csv')

        except Exception:
            raise Exception