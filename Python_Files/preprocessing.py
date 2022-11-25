import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

class Preprocessor:

    def __init__(self):
        pass

    def remove_columns(self,data,columns):

        self.data=data
        self.columns=columns
        try:
            self.useful_data=self.data.drop(labels=self.columns, axis=1) # drop the labels specified in the columns
            return self.useful_data
        except Exception as e:
            raise Exception()

    def separate_label_feature(self, data, label_column_name):
        try:
            self.X=data.drop(labels=label_column_name,axis=1) # drop the columns specified and separate the feature columns
            self.Y=data[label_column_name] # Filter the Label columns
            return self.X,self.Y
        except Exception as e:
            raise Exception()

    def dropUnnecessaryColumns(self,data,columnNameList):
        data = data.drop(columnNameList,axis=1)
        return data

    def replaceInvalidValuesWithNull(self,data):
        for column in data.columns:
            count = data[column][data[column] == '?'].count()
            if count != 0:
                data[column] = data[column].replace('?', np.nan)
        return data

    def is_null_present(self,data):
        self.null_present = False
        self.cols_with_missing_values=[]
        self.cols = data.columns
        try:
            self.null_counts=data.isna().sum() # check for the count of null values per column
            for i in range(len(self.null_counts)):
                if self.null_counts[i]>0:
                    self.null_present=True
                    self.cols_with_missing_values.append(self.cols[i])
            if(self.null_present): # write the logs to see which columns have null values
                self.dataframe_with_null = pd.DataFrame()
                self.dataframe_with_null['columns'] = data.columns
                self.dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                self.dataframe_with_null.to_csv('preprocessing_data/null_values.csv') # storing the null column information to file
            return self.null_present, self.cols_with_missing_values
        except Exception as e:
            raise Exception()

    def encodeCategoricalValues(self,data):
     data["class"] = data["class"].map({'p': 1, 'e': 2})
     for column in data.drop(['class'],axis=1).columns:
            data = pd.get_dummies(data, columns=[column])
     return data


    def encodeCategoricalValuesPrediction(self,data):
        for column in data.columns:
            data = pd.get_dummies(data, columns=[column])
        return data

    # def handleImbalanceDataset(self,X,Y):
    #     """
    #                                                   Method Name: handleImbalanceDataset
    #                                                   Description: This method handles the imbalance in the dataset by oversampling.
    #                                                   Output: A Dataframe which is balanced now.
    #                                                   On Failure: Raise Exception
    #
    #                                                   Written By: iNeuron Intelligence
    #                                                   Version: 1.0
    #                                                   Revisions: None
    #                                """
    #
    #
    #
    #     rdsmple = RandomOverSampler()
    #     x_sampled, y_sampled = rdsmple.fit_sample(X, Y)
    #
    #     return x_sampled,y_sampled

    def standardScalingData(self,X):
        scalar = StandardScaler()
        X_scaled = scalar.fit_transform(X)
        return X_scaled

    def logTransformation(self,X):
        for column in X.columns:
            X[column] += 1
            X[column] = np.log(X[column])
        return X


    def impute_missing_values(self, data):
        self.data= data
        try:
            imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
            self.new_array=imputer.fit_transform(self.data) # impute the missing values
            # convert the nd-array returned in the step above to a Dataframe
            self.new_data=pd.DataFrame(data=(self.new_array), columns=self.data.columns)
            return self.new_data
        except Exception as e:
            raise Exception()

    def get_columns_with_zero_std_deviation(self,data):
        self.columns=data.columns
        self.data_n = data.describe()
        self.col_to_drop=[]
        try:
            for x in self.columns:
                if (self.data_n[x]['std'] == 0): # check if standard deviation is zero
                    self.col_to_drop.append(x)  # prepare the list of columns with standard deviation zero
            return self.col_to_drop

        except Exception as e:
            raise Exception()