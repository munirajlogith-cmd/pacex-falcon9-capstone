"""Lab 8: classification models for landing success. Print results feed the slides."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from config import DATASET_PART_2, DATASET_PART_3

Y = pd.read_csv(DATASET_PART_2)["Class"].to_numpy()
X = pd.read_csv(DATASET_PART_3)
X = pd.DataFrame(StandardScaler().fit_transform(X), columns=X.columns)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
print("Test set size:", len(y_test))

models = {
    "Logistic Regression": (LogisticRegression(max_iter=1000),
                            {"C": [0.01, 0.1, 1], "penalty": ["l2"], "solver": ["lbfgs"]}),
    "SVM": (SVC(), {"kernel": ["linear", "rbf", "poly", "sigmoid"],
                    "C": np.logspace(-3, 3, 5), "gamma": np.logspace(-3, 3, 5)}),
    "Decision Tree": (DecisionTreeClassifier(random_state=12345),
                      {"criterion": ["gini", "entropy"], "splitter": ["best", "random"],
                       "max_depth": [2 * n for n in range(1, 10)],
                       "max_features": ["sqrt"], "min_samples_leaf": [1, 2, 4],
                       "min_samples_split": [2, 5, 10]}),
    "KNN": (KNeighborsClassifier(), {"n_neighbors": list(range(1, 11)),
                                     "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
                                     "p": [1, 2]}),
}

results, best_model, best_acc = {}, None, -1
for name, (est, grid) in models.items():
    gs = GridSearchCV(est, grid, cv=10).fit(X_train, y_train)
    acc = gs.score(X_test, y_test)
    results[name] = {"cv_accuracy": gs.best_score_, "test_accuracy": acc, "best_params": gs.best_params_}
    if acc > best_acc:
        best_model, best_acc = (name, gs), acc

summary = pd.DataFrame(results).T
print(summary)
summary.to_csv("model_results.csv")

name, gs = best_model
cm = confusion_matrix(y_test, gs.predict(X_test))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["did not land", "landed"], yticklabels=["did not land", "landed"])
plt.title(f"Confusion matrix - {name}")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("fig_confusion_matrix.png", dpi=150)
print("Best model:", name, "test accuracy:", round(best_acc, 4))
