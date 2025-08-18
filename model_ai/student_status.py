import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

BASE_DIR = Path(__file__).resolve().parents[1]
csv_path = BASE_DIR /'model_ai' /'data' / 'student-mat.csv'
out_dir = BASE_DIR /'model_ai' / 'model'
out_dir.mkdir(parents=True, exist_ok=True)
model_path = out_dir / 'student_scores.pkl'

df = pd.read_csv(csv_path ,sep=';')

df['Label'] = (df['G3'] < 8).astype(int)

X = df[['G2']].values
y = df['Label'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1337, stratify=y
)

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression(max_iter=1000, solver='lbfgs'))
])
pipe.fit(X_train, y_train)

y_proba = pipe.predict_proba(X_test)[:, 1]
y_pred  = (y_proba >= 0.5).astype(int)

acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

joblib.dump(pipe, model_path)
print(f'Model saved to: {model_path}')
print(f'Accuracy: {acc:.3f} | ROC AUC: {auc:.3f}')
