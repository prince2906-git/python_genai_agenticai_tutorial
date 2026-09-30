from sklearn.linear_model import LinearRegression 

model = LinearRegression() # Creating a model with empty brain.  

#Preparing training data 
hours = [[1],[2],[3],[4],[5],[6],[7]] # Input Data : 2D Numpy Array
marks = [35,40,50,60,75,83,85] 
# Output Data : Currently provided as an input training dataset , For Hour input model have to predict marks as an output

model.fit(hours,marks) # Training the model

print(model.predict([[3.5]])) # Asking Model to Predict marks now. 56.4821
print(model.predict([[10]])) # 117.07
print(model.predict([[4]]))