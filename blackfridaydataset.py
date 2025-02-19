# -*- coding: utf-8 -*-
"""BlackFridayDataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wQYhtJG86B2Cdq_yq7cAV6P7zms6IoEG

# Import
"""

import numpy as np #array conversion for better manipulation for matrix operations
import pandas as pd  # converting data into pandas dataframe
import matplotlib.pyplot as plt #plotting data
from sklearn.model_selection import train_test_split #split
from sklearn.preprocessing import StandardScaler,add_dummy_feature #helps to bring to standard scale
from sklearn.linear_model import LinearRegression #Linear Regression
from sklearn.metrics import r2_score #r2 score
from sklearn.metrics import mean_squared_error,root_mean_squared_error #MSE
from sklearn.metrics import mean_absolute_error #MAE
from sklearn.metrics import accuracy_score #Accuracy

"""# Convert into dataframe tabular format"""

data = pd.read_csv('Black Friday Dataset.csv')
data

"""#Info gathering from data"""

data.info()

#Drop columns User_ID, Product_ID
data = data.drop(["User_ID","Product_ID"],axis=1)
data.head()

#Drop row with NAN in Gender,Age,Occupation,City_Category,Stay_In_Current_City_Years,Marital_Status,Product_Category_1,Purchase
data = data.dropna(how='all') #drops the row with all values as null
data.info()

#Filling NAN values for columns Product_Category_2 and Product_Category_3 with median
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan,strategy='constant',fill_value=0)
imputer.fit(data[["Product_Category_2"]])
data[["Product_Category_2"]] = imputer.transform(data[["Product_Category_2"]])
imputer.fit(data[["Product_Category_3"]])
data[["Product_Category_3"]] = imputer.transform(data[["Product_Category_3"]])
data.info()

data

#convert Gender , Age , City_Category, Stay_In_Current_City_Years into numerical format
#Gender
from sklearn.preprocessing import LabelEncoder,OrdinalEncoder
encoder = LabelEncoder()
data["Gender"] = encoder.fit_transform(data["Gender"].values.reshape(-1,1))
data

#Age
encoder_age = LabelEncoder()
data["Age"] = encoder_age.fit_transform(data["Age"].values.reshape(-1,1))
data

#City_Category
encoder_city = LabelEncoder()
data["City_Category"] = encoder_city.fit_transform(data["City_Category"].values.reshape(-1,1))
data

#Stay_In_Current_City_Years
encoder_current_city = OrdinalEncoder()
data["Stay_In_Current_City_Years"] = encoder_current_city.fit_transform(data["Stay_In_Current_City_Years"].values.reshape(-1,1))
data

data.info()

data.describe()

data.shape

#Finding corelation
data_corr = data.corr()
#Less impact on wine quality Residual Sugar, Density, free and total sufur dioxide , ph(debatable if data is overfitted then only use this) so we are going to drop these columns
#data_new = data.drop(["residual sugar","density","free sulfur dioxide","total sulfur dioxide","pH"],axis=1) #axis=1 to remove data column wise
#Now we will split data for training
data_corr["Purchase"].sort_values(ascending=False)

"""###Positive correlation - Product_Category_3,City_Category,Gender,Product_Category_2
###Negative correlation - Product_Category_1

###Remove - Occupation, age, Stay_In_Current_City_Years, Marital_Status < 0.05
"""

data_new = data.drop(["Occupation","Age","Stay_In_Current_City_Years","Marital_Status"],axis=1)
data_new

#Feature scaling because in ML all features should have same scale to avoid bias
std_data = StandardScaler()
data_fit = std_data.fit_transform(data_new) #fit used to train model StandardScaler on the data and finds the scale  and transform applies the scale to the data
data_fit = pd.DataFrame(data_fit,columns=data_new.columns) #convert the np into dataframe
data_fit.head()

#Segregate feature and target
X = data_fit.drop("Purchase",axis=1)
y = data_fit["Purchase"]

X

y

#split data for training and testing
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

reg = LinearRegression()
reg.fit(X_train,y_train)
y_pred_lin = reg.predict(X_test)

print("R2 score:",r2_score(y_test,y_pred_lin))
print("MSE:",mean_squared_error(y_test,y_pred_lin))
print("MAE:",mean_absolute_error(y_test,y_pred_lin))
print("RMSE:",root_mean_squared_error(y_test,y_pred_lin))

import pandas as pd

# Reshape y_pred_reg_valid to have the same number of features as the original data used for fitting std_data
# Assuming std_data was fitted on data with 7 features
num_original_features = std_data.n_features_in_  # Get the number of features used during fitting
original_y_pred = std_data.inverse_transform(
    np.concatenate(
        [
            y_pred_lin.reshape(-1, 1),  # Reshape predictions to a single column
            np.zeros((y_pred_lin.shape[0], num_original_features - 1)),  # Pad with zeros for other features
        ],
        axis=1,
    )
)

# Extract the 'count' column, which should be the first column after inverse transform
df = pd.DataFrame({"y_pred_reg_valid": original_y_pred[:, 0]})
df.to_csv("prediction.csv", index=False)

"""#Batch Gradient descent to give a good model by giving good theta values or weight values"""

#to add x0=1 to all
X_l = add_dummy_feature(X_train)
X_l.shape

eta = 0.1
epochs = 1000
n = len(X_l)
np.random.seed(42)
theta = np.random.randn(6,1) # Changed to (10, 1) to match X_l's dimensions for matrix operations 10 rows and 1 column
#theta = [1]
#         2
#         3
#         4
#         5
#         6
#         7
#         8
#Reshape y_train to be a column vector
y_train_reshaped = y_train.values.reshape(-1, 1) #length of y ie 8 so 8 rows with 1 column #initially add values
losses_batch = []
for epoch in range(epochs):
    # Calculate the gradient. Note the order of operations is important for matrix multiplication.
    grad = (1/n) * X_l.T.dot((X_l.dot(theta) - y_train_reshaped)) #as per formula
    theta = theta - eta * grad # Update theta
    losses_batch.append(np.mean((theta)**2)) #mean squared error

plt.figure(figsize=(10, 6))
plt.plot(range(epochs), losses_batch)
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.title('Batch Gradient Descent')
plt.legend()
plt.show()

X_test_l = add_dummy_feature(X_test)

y_pred = X_test_l.dot(theta)
y_pred

import pandas as pd

# Reshape y_pred_reg_valid to have the same number of features as the original data used for fitting std_data
# Assuming std_data was fitted on data with 7 features
num_original_features = std_data.n_features_in_  # Get the number of features used during fitting
original_y_pred = std_data.inverse_transform(
    np.concatenate(
        [
            y_pred.reshape(-1, 1),  # Reshape predictions to a single column
            np.zeros((y_pred.shape[0], num_original_features - 1)),  # Pad with zeros for other features
        ],
        axis=1,
    )
)

# Extract the 'count' column, which should be the first column after inverse transform
df = pd.DataFrame({"y_pred_reg_valid": original_y_pred[:, 0]})
df.to_csv("predictions_batch.csv", index=False)

pd.DataFrame(X_test_l,columns=data_new.columns)

columns = data_new.columns
columns
for i in range(len(X_test_l)):
  plt.xlabel(columns[i])
  plt.ylabel("Purchase")
  plt.scatter(X_test_l[:,i],y_pred,color="blue",label="Predicted values through Batch Gradient Descent")

  plt.legend()
  plt.show()
  if columns[i] =="Product_Category_3":
    break

"""#Stochastic Gradient Descent"""

from sklearn.linear_model import SGDRegressor
sgd_reg = SGDRegressor(max_iter=1000, tol=1e-3, penalty=None, eta0=0.1)
sgd_reg.fit(X_train, y_train)
print(sgd_reg.intercept_, sgd_reg.coef_)
eta = 0.1
epochs = 1000
n = len(X_l)
np.random.seed(42)
theta = np.random.randn(6,1) # Changed to (10, 1) to match X_l's dimensions for matrix operations 10 rows and 1 column
#theta = [1]
#         2
#         3
#         4
#         5
#         6
#         7
#         8
#Reshape y_train to be a column vector
y_train_reshaped = y_train.values.reshape(-1, 1) #length of y ie 8 so 8 rows with 1 column #initially add values
losses_sgd = []
for epoch in range(epochs):
    # Calculate the gradient. Note the order of operations is important for matrix multiplication.
    grad = (1/n) * X_l.T.dot((X_l.dot(theta) - y_train_reshaped)) #as per formula
    theta = theta - eta * grad # Update theta
    losses_sgd.append((np.mean(theta**2 + np.random.randn() * 0.1)**2))  # Adding noise for SGD

# Plot Batch and SGD
plt.figure(figsize=(10, 6))
plt.plot(range(epochs), losses_sgd, alpha=0.6)
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.title('Stochastic Gradient Descent Comparison')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(range(epochs), losses_sgd, alpha=0.6, label="Stochastic Gradient Descent")
plt.plot(range(epochs), losses_batch,label="Batch Gradient Descent")
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.title('Gradient Descent Comparison')
plt.legend()
plt.show()

y_pred_stoc = sgd_reg.predict(X_test)
y_pred_stoc

import pandas as pd

# Reshape y_pred_reg_valid to have the same number of features as the original data used for fitting std_data
# Assuming std_data was fitted on data with 7 features
num_original_features = std_data.n_features_in_  # Get the number of features used during fitting
original_y_pred = std_data.inverse_transform(
    np.concatenate(
        [
            y_pred_stoc.reshape(-1, 1),  # Reshape predictions to a single column
            np.zeros((y_pred_stoc.shape[0], num_original_features - 1)),  # Pad with zeros for other features
        ],
        axis=1,
    )
)

# Extract the 'count' column, which should be the first column after inverse transform
df = pd.DataFrame({"y_pred_reg_valid": original_y_pred[:, 0]})
df.to_csv("predictions_stoc.csv", index=False)

"""#Polynomial Regression"""

from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree=1, include_bias=True)
X_poly = poly_reg.fit_transform(X_train)
lin_reg = LinearRegression()
lin_reg.fit(X_poly, y_train)
lin_reg.intercept_, lin_reg.coef_

X_poly_test = poly_reg.fit_transform(X_test)
lin_reg = LinearRegression()
lin_reg.fit(X_poly, y_train)
y_pred_poly = lin_reg.predict(X_poly_test)

import pandas as pd

# Get the number of features used during fitting
num_original_features = std_data.n_features_in_

# No need to reshape if y_pred_poly is already 1-dimensional
# y_poly_test_valid_reshaped = y_pred_poly[:, :num_original_features]

# Instead, create a DataFrame directly from y_pred_poly
original_y_pred = std_data.inverse_transform(
    np.concatenate(
        [
            y_pred_poly.reshape(-1, 1),  # Reshape predictions to a single column
            np.zeros((y_pred_poly.shape[0], num_original_features - 1)),  # Pad with zeros for other features
        ],
        axis=1,
    )
)

# Extract the predictions, which should be in the first column
# after inverse_transform
df = pd.DataFrame({"y_pred_reg_valid": original_y_pred[:, 0]})
df.to_csv("predictions_poly.csv", index=False)

"""# Using regularised linear regression to give good bias values"""

#Ridge Regression
from sklearn.linear_model import Ridge
alphas = np.logspace(-3, 1, 50)
ridge_coefs = []
for alp in alphas:
  ridge_reg = Ridge(alpha=alp, solver="cholesky", random_state=42)
  ridge_reg.fit(X_train, y_train)
  ridge_coefs.append(ridge_reg.coef_[0])
  y_pred_reg = ridge_reg.predict(X_test)

plt.figure(figsize=(10, 6))
plt.plot(alphas, ridge_coefs)
plt.xscale('log')
plt.xlabel('Regularization Parameter (alpha)')
plt.ylabel('Coefficients')
plt.title('Ridge Regularization Methods Comparison')
plt.legend()
plt.show()

from sklearn.linear_model import Ridge

alphas = np.logspace(-3, 1, 50)
for alp in alphas:
  ridge_reg = Ridge(alpha=alp, solver="cholesky", random_state=42)
  ridge_reg.fit(X_train, y_train)
  y_pred_reg = ridge_reg.predict(X_test)
y_pred_reg

import pandas as pd

# Reshape y_pred_reg_valid to have the same number of features as the original data used for fitting std_data
# Assuming std_data was fitted on data with 7 features
num_original_features = std_data.n_features_in_  # Get the number of features used during fitting
original_y_pred = std_data.inverse_transform(
    np.concatenate(
        [
            y_pred_reg.reshape(-1, 1),  # Reshape predictions to a single column
            np.zeros((y_pred_reg.shape[0], num_original_features - 1)),  # Pad with zeros for other features
        ],
        axis=1,
    )
)

# Extract the 'count' column, which should be the first column after inverse transform
df = pd.DataFrame({"y_pred_reg_valid": original_y_pred[:, 0]})
df.to_csv("predictions_ridge.csv", index=False)

#Lasso Regression
from sklearn.linear_model import Lasso
lasso_coefs = []
alphas = np.logspace(-3, 1, 50)
for alp in alphas:
  lasso_reg = Lasso(alpha=alp)
  lasso_reg.fit(X_train, y_train)
  lasso_coefs.append(lasso_reg.coef_)
  y_pred_lasso = lasso_reg.predict(X_test)

plt.figure(figsize=(10, 6))
plt.plot(alphas, lasso_coefs)
plt.xscale('log')
plt.xlabel('Regularization Parameter (alpha)')
plt.ylabel('Coefficients')
plt.title('Lasso Regularization Methods Comparison')
plt.legend()
plt.show()

#Lasso Regression
from sklearn.linear_model import Lasso
lasso_coefs = []
alphas = np.logspace(-3, 1, 50)
for alp in alphas:
  lasso_reg = Lasso(alpha=alp)
  lasso_reg.fit(X_train, y_train)
  y_pred_lasso_test = lasso_reg.predict(X_test)
y_pred_lasso_test

import pandas as pd

# Get the number of features used during fitting
num_original_features = std_data.n_features_in_

# No need to reshape if y_pred_poly is already 1-dimensional
# y_poly_test_valid_reshaped = y_pred_poly[:, :num_original_features]

# Instead, create a DataFrame directly from y_pred_poly
original_y_pred = std_data.inverse_transform(
    np.concatenate(
        [
            y_pred_lasso_test.reshape(-1, 1),  # Reshape predictions to a single column
            np.zeros((y_pred_lasso_test.shape[0], num_original_features - 1)),  # Pad with zeros for other features
        ],
        axis=1,
    )
)

# Extract the predictions, which should be in the first column
# after inverse_transform
df = pd.DataFrame({"y_pred_reg_valid": original_y_pred[:, 0]})
df.to_csv("predictions_lasso.csv", index=False)

#Elastic net regression
from sklearn.linear_model import ElasticNet
elastic_coefs = []
alphas = np.logspace(-3, 1, 50)
for alp in alphas:
  elastic_net = ElasticNet(alpha=alp, l1_ratio=0.5, random_state=42)
  elastic_net.fit(X_train, y_train)
  elastic_coefs.append(elastic_net.coef_)
  y_pred_elastic = elastic_net.predict(X_test)

plt.figure(figsize=(10, 6))
plt.plot(alphas, elastic_coefs)
plt.xscale('log')
plt.xlabel('Regularization Parameter (alpha)')
plt.ylabel('Coefficients')
plt.title('Elastic Regularization Methods Comparison')
plt.legend()
plt.show()

#Elastic net regression
from sklearn.linear_model import ElasticNet
elastic_coefs = []
alphas = np.logspace(-3, 1, 50)
for alp in alphas:
  elastic_net = ElasticNet(alpha=alp, l1_ratio=0.5, random_state=42)
  elastic_net.fit(X_train, y_train)
  y_pred_elastic_test = elastic_net.predict(X_test)
y_pred_elastic_test

import pandas as pd

# Reshape y_pred_reg_valid to have the same number of features as the original data used for fitting std_data
# Assuming std_data was fitted on data with 7 features
num_original_features = std_data.n_features_in_  # Get the number of features used during fitting
original_y_pred = std_data.inverse_transform(
    np.concatenate(
        [
            y_pred_elastic_test.reshape(-1, 1),  # Reshape predictions to a single column
            np.zeros((y_pred_elastic_test.shape[0], num_original_features - 1)),  # Pad with zeros for other features
        ],
        axis=1,
    )
)

# Extract the 'count' column, which should be the first column after inverse transform
df = pd.DataFrame({"y_pred_reg_valid": original_y_pred[:, 0]})
df.to_csv("predictions_elastic.csv", index=False)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

# Ridge, Lasso, Elastic Net example
alphas = np.logspace(-3, 1, 50)
ridge_coefs, lasso_coefs, elastic_coefs = [], [], []

for alpha in alphas:
    ridge = Ridge(alpha=alpha).fit(X_train, y_train)
    lasso = Lasso(alpha=alpha).fit(X_train, y_train)
    elastic_net = ElasticNet(alpha=alpha, l1_ratio=0.5).fit(X_train, y_train)
    ridge_coefs.append(ridge.coef_[0])
    lasso_coefs.append(lasso.coef_)
    elastic_coefs.append(elastic_net.coef_)

# Plot Ridge, Lasso, and Elastic Net
plt.figure(figsize=(10, 6))
plt.plot(alphas, ridge_coefs, label='Ridge Coefficients')
plt.plot(alphas, lasso_coefs, label='Lasso Coefficients')
plt.plot(alphas, elastic_coefs, label='Elastic Net Coefficients')
plt.xscale('log')
plt.xlabel('Regularization Parameter (alpha)')
plt.ylabel('Coefficients')
plt.title('Regularization Methods Comparison')
plt.legend()
plt.show()