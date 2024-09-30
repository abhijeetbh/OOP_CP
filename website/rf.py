import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import warnings
import joblib
warnings.filterwarnings('ignore')

df=pandas.read_csv('outliers_removed.csv')

x=df.drop('Outcome',axis=1)
y=df['Outcome']

smote=SMOTE(sampling_strategy={0:2000,1:2000},random_state=123)
x,y=smote.fit_resample(x,y)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1)


rf=RandomForestClassifier()
rf.fit(x_train,y_train)

y_pred=rf.predict(x_test)
accuracy=accuracy_score(y_test,y_pred)
print("Accuracy of the model is : ",accuracy*100,'%')