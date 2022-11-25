from Python_Files.trainingModel import trainModel
from Python_Files.training_Validation_Insertion import train_validation
from Python_Files.prediction_Validation_Insertion import pred_validation
from Python_Files.predictFromModel import prediction

from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard

training_files_path  = "Input/Training_Batch_Files"
prediction_file_path = "Input/Prediction_Batch_files"
training_schema_path = "Python_Files"
pred_schema_path     = "Python_Files"
current_working_directory = os.getcwd().replace("\\","//")


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.form is not None:
            pred_file_path = request.form['filepath']
            pred_file_path = pred_file_path.replace("\\", "//")
        else:
            pred_file_path = prediction_file_path
            
        
        pred_val = pred_validation(pred_file_path,pred_schema_path) #object initialization
        pred_val.prediction_validation() #calling the prediction_validation function
        pred = prediction(pred_file_path,pred_schema_path,current_working_directory) #object initialization
        path,result = pred.predictionFromModel() # predicting for dataset present in database
        return Response(result.to_csv(index=False),mimetype="text/csv",headers={"Content-disposition":"attachment; filename=filename.csv"})
        #return Response("Prediction File is created at %s!!!" % path)
        
    except ValueError:
        return Response("Error Occurred 1! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred 2! %s" %KeyError)
    except Exception as e:
        print(e)
        return Response("Error Occurred 3! %s" %e)

@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRouteClient():

    try:
        train_valObj = train_validation(training_files_path,training_schema_path) #object initialization
        train_valObj.train_validation()#calling the training_validation function
        trainModelObj = trainModel(current_working_directory)
        trainModelObj.trainingModel()

    except ValueError:
        return Response("Error Occurred ! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred ! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred ! %s" % e)
    return Response("Training successfull!!")


port = int(os.getenv("PORT",5001))
if __name__ == "__main__":
    host='0.0.0.0'
    httpd = simple_server.make_server( host,port, app)
    print("Serving on %s %d" % ( host,port))
    httpd.serve_forever()



