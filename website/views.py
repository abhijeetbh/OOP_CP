from flask import Blueprint, redirect, url_for
from flask import render_template
from flask import request
from flask import flash
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import pandas
import warnings
warnings.filterwarnings('ignore')


from win32comext.mapi.mapitags import PR_ATTACH_NUM

views=Blueprint('views',__name__)


@views.route('/index', methods=['GET','POST'])
def index():
    df = pandas.read_csv('outliers_removed.csv')

    x = df.drop('Outcome', axis=1)
    y = df['Outcome']

    smote = SMOTE(sampling_strategy={0: 2000, 1: 2000}, random_state=123)
    x, y = smote.fit_resample(x, y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

    rf = RandomForestClassifier()
    rf.fit(x_train, y_train)

    y_pred = rf.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy of the model is : ", accuracy * 100, '%')

    if request.method=='POST':
        preg=request.form.get('preg')
        glu=request.form.get('glu')
        bp=request.form.get('bp')
        ins=request.form.get('ins')
        bmi=request.form.get('bmi')
        age=request.form.get('age')

        preg=pandas.to_numeric(preg)
        glu=pandas.to_numeric(glu)
        bp=pandas.to_numeric(bp)
        ins=pandas.to_numeric(ins)
        bmi=pandas.to_numeric(bmi)
        age=pandas.to_numeric(age)

        if preg<0:
            flash('Pregnancies cannot be less than zero', 'error')
            return redirect(url_for('views.index'))
        if glu<=0:
            flash('Glucose cannot be less than or equal to zero','error')
            return redirect(url_for('views.index'))
        if bp<=0:
            flash('Blood Pressure cannot be less than or equal to zero','error')
            return redirect(url_for('views.index'))
        if ins<0:
            flash('Insulin cannot be less than 0', 'error')
            return redirect(url_for('views.index'))
        if bmi<=0:
            flash('BMI cannot be less than or equal to zero','error')
            return redirect(url_for('views.index'))
        if age<=0:
            flash('Age cannot be less than or equal to zero','error')
            return redirect(url_for('views.index'))

        user_data=[[preg,glu,bp,ins,bmi,age]]


        res=rf.predict(user_data)
        print(res)
        if res==1:
            flash('You might be diabetic, consult a professional immediately','error')
        if res==0:
            flash('You are not diabetic','succ')

    return render_template("index.html")