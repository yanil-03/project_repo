import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import db_utils, joblib

df = db_utils.load_sample_data()

df = df.drop(columns= ['CandidateID', 'Name', 'Age', 'Location'])
# print(df.head()
lb_education = LabelEncoder()
lb_internships = LabelEncoder()
# lb = LabelEncoder()
# df['Location'] = lb.fit_transform(df['Location'])
df['Education'] = lb_education.fit_transform(df['Education'])
df['SuggestedInternship'] = lb_internships.fit_transform(df['SuggestedInternship'])

X = df.drop(columns = ['SuggestedInternship'])
y = df['SuggestedInternship']
print(X.head())
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Best Parameters: {'n_estimators': 300, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_depth': 20, 'bootstrap': True}
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy : ", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))


joblib.dump(lb_education, "lb_education.pkl")
joblib.dump(lb_internships, "lb_internships.pkl")
joblib.dump(model, "model.pkl")
print("PKL files exported!")