# Import Libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix

# Load Dataset (You can find datasets on Kaggle)
data = pd.read_csv('spam.csv', encoding='latin-1')
data = data[['v1', 'v2']]
data.columns = ['label', 'message']

# Preprocessing
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# Feature Extraction using Bag of Words (BoW)
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['message'])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, data['label'], test_size=0.2, random_state=42)

# Model Training
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Confusion Matrix
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))
