from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics  import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')

class Model_Finder:

    def __init__(self):
        self.linearReg = LinearRegression()
        self.RandomForestReg = RandomForestRegressor()


    def get_best_params_for_Random_Forest_Regressor(self, train_x, train_y):
        try:
            # initializing with different combination of parameters
            self.param_grid_Random_forest_Tree = {
                                "n_estimators": [10,20,30],
                                "max_features": ["auto", "sqrt", "log2"],
                                "min_samples_split": [2,4,8],
                                "bootstrap": [True, False]
                                                     }

            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(self.RandomForestReg, self.param_grid_Random_forest_Tree, verbose=3, cv=5)
            # finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.max_features = self.grid.best_params_['max_features']
            self.min_samples_split = self.grid.best_params_['min_samples_split']
            self.bootstrap = self.grid.best_params_['bootstrap']

            # creating a new model with the best parameters
            self.decisionTreeReg = RandomForestRegressor(n_estimators=self.n_estimators, max_features=self.max_features,
                                                         min_samples_split=self.min_samples_split, bootstrap=self.bootstrap)
            # training the mew models
            self.decisionTreeReg.fit(train_x, train_y)
            return self.decisionTreeReg
        except Exception as e:
            raise Exception()

    def get_best_params_for_linearReg(self,train_x,train_y):
        try:
            # initializing with different combination of parameters
            self.param_grid_linearReg = {
                'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False]

            }
            # Creating an object of the Grid Search class
            self.grid= GridSearchCV(self.linearReg,self.param_grid_linearReg, verbose=3,cv=5)
            # finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.fit_intercept = self.grid.best_params_['fit_intercept']
            self.normalize = self.grid.best_params_['normalize']
            self.copy_X = self.grid.best_params_['copy_X']

            # creating a new model with the best parameters
            self.linReg = LinearRegression(fit_intercept=self.fit_intercept,normalize=self.normalize,copy_X=self.copy_X)
            # training the mew model
            self.linReg.fit(train_x, train_y)
            return self.linReg
        except Exception as e:
            raise Exception()
    
    def get_best_params_for_xgboost(self,train_x,train_y):
        try:
            self.param_grid = {
                            'n_estimators': [400, 700, 1000],
                            'colsample_bytree': [0.7, 0.8],
                            'max_depth': [15,20,25],
                            'reg_alpha': [1.1, 1.2, 1.3],
                            'reg_lambda': [1.1, 1.2, 1.3],
                            'subsample': [0.7, 0.8, 0.9]
                        }
            self.xgb_grid = GridSearchCV(XGBRegressor(), self.param_grid, verbose=3, cv=5)
            # finding the best parameters
            self.xgb_grid.fit(train_x, train_y)
            self.colsample_bytree = self.xgb_grid.best_params_['colsample_bytree']
            self.max_depth = self.xgb_grid.best_params_['max_depth']
            self.n_estimators = self.xgb_grid.best_params_['n_estimators']
            self.reg_alpha = self.xgb_grid.best_params_['reg_alpha']
            self.reg_lambda = self.xgb_grid.best_params_['reg_lambda']
            self.subsample = self.xgb_grid.best_params_['subsample']

            self.xgbreg = XGBRegressor(colsample_bytree =self.colsample_bytree, max_depth=self.max_depth,n_estimators=self.n_estimators,reg_alpha = self.reg_alpha,reg_lambda = self.reg_lambda,subsample = self.subsample)
            self.xgbreg.fit(train_x, train_y)
            return self.xgbreg
        except Exception as e:
            raise Exception()



    def get_best_model(self,train_x,train_y,test_x,test_y):
        # create best model for Linear Regression
        try:
            models = {}
            model_names = {}

            self.LinearReg= self.get_best_params_for_linearReg(train_x, train_y)
            self.prediction_LinearReg = self.LinearReg.predict(test_x) # Predictions using the LinearReg Model
            self.LinearReg_error = r2_score(test_y,self.prediction_LinearReg)
            models[self.LinearReg] = self.LinearReg_error
            model_names['LinearRegression'] = self.LinearReg

            self.randomForestReg = self.get_best_params_for_Random_Forest_Regressor(train_x, train_y)
            self.prediction_randomForestReg = self.randomForestReg.predict(test_x)  # Predictions using the randomForestReg Model
            self.prediction_randomForestReg_error = r2_score(test_y,self.prediction_randomForestReg)
            models[self.randomForestReg] = self.prediction_randomForestReg_error
            model_names['RandomForestRegressor'] = self.randomForestReg

            self.XGBReg = self.get_best_params_for_xgboost(train_x, train_y)
            self.prediction_XGBReg = self.XGBReg.predict(test_x) # Predictions using the LinearReg Model
            self.XGBReg_error = r2_score(test_y,self.prediction_XGBReg)
            models[self.XGBReg] = self.XGBReg_error
            model_names['XGBoostRegressor'] = self.XGBReg

            best_model = max(zip(models.values(), models.keys()))[1]
            best_model_name = list(model_names.keys())[list(model_names.values()).index(best_model)]
            return best_model_name,best_model

        except Exception as e:
            raise Exception()

