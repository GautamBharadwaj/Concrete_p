from datetime import datetime
from os import listdir
import pandas

class dataTransformPredict:
     def __init__(self):
          self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"

     def addQuotesToStringValuesInColumn(self):
          try:
               onlyfiles = [f for f in listdir(self.goodDataPath)]
               for file in onlyfiles:
                    data = pandas.read_csv(self.goodDataPath + "/" + file)
                    # list of columns with string datatype variables
                    # column = ['sex', 'on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_medication', 'sick',
                    #           'pregnant',
                    #           'thyroid_surgery', 'I131_treatment', 'query_hypothyroid', 'query_hyperthyroid', 'lithium',
                    #           'goitre', 'tumor', 'hypopituitary', 'psych', 'TSH_measured', 'T3_measured',
                    #           'TT4_measured',
                    #           'T4U_measured', 'FTI_measured', 'TBG_measured', 'TBG', 'referral_source', 'Class']

                    data['DATE'] = data["DATE"].apply(lambda x: "'" + str(x) + "'")

                    # there are "hyphen" in our column name which results in failure when inserting the column names in the table
                    # so we are changing the column names by replacing the '-'
                    # for col in data.columns:
                    #      new_col = col.replace('-', '')
                    #      data = data.rename(columns={col: new_col})
                    #
                    # for col in data.columns:
                    #      data[col] = data[col].apply(lambda x: "'" + str(x) + "'")
                    # #csv.update("'"+ csv['Wafer'] +"'")
                    # csv.update(csv['Wafer'].astype(str))
                    # csv['Wafer'] = csv['Wafer'].str[6:]
                    data.to_csv(self.goodDataPath + "/" + file, index=None, header=True)

          except Exception as e:
               raise e
