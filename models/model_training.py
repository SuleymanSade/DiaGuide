import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import matplotlib.pyplot as plt
from sklearn.svm import SVC

DATA_PATH = 'data/diabetes_binary_health_indicators_BRFSS2015.csv'


def get_data(path=DATA_PATH):
    print("Loading data...")
    try:
        df = pd.read_csv(DATA_PATH)
        df = df.drop(columns=["Income", "Education"])
        print("Data loaded successfully.")
        return df
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

def data_prep(df):
    print("Preparing data...")

    if df is None:
        print("No data to prepare.")
        return None, None, None, None, None
    
    # Convert columns to appropriate data types
    if 'Diabetes_binary' in df.columns:       df['Diabetes_binary'] = df['Diabetes_binary'].astype('category')
    if 'Smoker' in df.columns:                df['Smoker'] = df['Smoker'].astype('category')
    if 'HearthDiseaseorAttack' in df.columns: df['HearthDiseaseorAttack'] = df['HearthDiseaseorAttack'].astype('category')
    if 'HighBP' in df.columns:                df['HighBP'] = df['HighBP'].astype('category')
    if 'HighChol' in df.columns:              df['HighChol'] = df['HighChol'].astype('category')
    if 'CholCheck' in df.columns:             df['CholCheck'] = df['CholCheck'].astype('category')
    if 'Stroke' in df.columns:                df['Stroke'] = df['Stroke'].astype('category')
    if 'Fruits' in df.columns:                df['Fruits'] = df['Fruits'].astype('category')
    if 'Veggies' in df.columns:               df['Veggies'] = df['Veggies'].astype('category')
    if 'Sex' in df.columns:                   df['Sex'] = df['Sex'].astype('category')
    if 'HvyAlcoholConsump' in df.columns:     df['HvyAlcoholConsump'] = df['HvyAlcoholConsump'].astype('category')
    if 'AnyHealthcare' in df.columns:         df['AnyHealthcare'] = df['AnyHealthcare'].astype('category')
    if 'NoDocbcCost' in df.columns:           df['NoDocbcCost'] = df['NoDocbcCost'].astype('category')
    if 'DiffWalk' in df.columns:              df['DiffWalk'] = df['DiffWalk'].astype('category')
    
    try:
        
        x = df.drop(columns=['Diabetes_binary'])
        y = df['Diabetes_binary']
        
        num_features = x.select_dtypes(include=['int64', 'float64']).columns
        cat_features = x.select_dtypes(include=['category']).columns
        
        print(f"Numerical features: {num_features}")
        print(f"Categorical features: {cat_features}")
        
        num_transform = StandardScaler()
        cat_transform = OneHotEncoder(handle_unknown='ignore')
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', num_transform, num_features),
                ('cat', cat_transform, cat_features)
            ]
        )
        
        x = preprocessor.fit_transform(x)
        
        print("Data preparation complete.")
        
        return x, y, num_features, cat_features, preprocessor
    except Exception as e:
        print(f"An error occurred during data preparation: {e}")
        print("Data preparation failed.")
    return None, None, None, None, None
    
    
def train_model(x, y, model_type='random_forest'):
    if x is None or y is None:
        print("No data to train the model.")
        return None
    
    # use RANDOM FOREST CLASSIFIER
    try:
        print("Training model...")
        if model_type == 'random_forest':
            model = RandomForestClassifier(random_state=42)
        elif model_type == 'logistic_regression':
            model = LogisticRegression(random_state=42)
        elif model_type == 'svm':
            model = SVC(probability=True, random_state=42)
        elif model_type == 'gradient_boosting':
            model = GradientBoostingClassifier(random_state=42)
        else:
            raise ValueError("Unsupported model type. Please choose 'random_forest', 'logistic_regression', 'svm', or 'gradient_boosting'.")
        # Uncomment the following line to use GridSearchCV for hyperparameter tuning
        # param_grid = {'n_estimators': [50, 100, 200], 'max_depth':[5, 10, None]}
        
        model.fit(x, y)
        print("Model training complete.")
        
        return model
    except Exception as e:
        print(f"An error occurred during model training: {e}")
        print("Model training failed.")
    return None, None, None

def evaluate_model(model, x_test, y_test, name="Random Forest"):
    print("Evaluating model...")
    if model is None or x_test is None or y_test is None:
        print("No model or test data to evaluate.")
        return
    
    try:
        y_pred = model.predict(x_test)
        y_pred_proba = model.predict_proba(x_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc_roc = roc_auc_score(y_test, y_pred_proba)

        print(f"Model: {name}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        print(f"AUC-ROC: {auc_roc:.4f}")

        # Plot ROC Curve
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {auc_roc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.legend(loc="lower right")
        plt.show()
    except Exception as e:
        print(f"An error occurred during model evaluation: {e}")

def save_model(model, preprocessor, filename='diabetes_model.pkl'):
    if model is None:
        print("No model to save.")
        return
    try:
        with open(filename, 'wb') as f:
            pickle.dump((model, preprocessor), f)
        print(f"Model saved to {filename}.")
    except Exception as e:
        print(f"An error occurred while saving the model: {e}")

def main():
    print("Starting model training...")
    
    df = get_data(DATA_PATH)
    if df is None:
        return
    
    x, y, num_features, cat_features, preprocessor = data_prep(df)
    
    if x is None or y is None:
        return
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
    
    # model = train_model(x_train, y_train)
    
    # evaluate_model(model, x_test, y_test)
    
    # save_model(model, preprocessor)
    
    lr_model = train_model(x_train, y_train, 'logistic_regression')
    evaluate_model(lr_model, x_test, y_test, "Logistic Regression")
    save_model(lr_model, preprocessor, "logistic_regression_model.pkl")

    rf_model = train_model(x_train, y_train, 'random_forest')
    evaluate_model(rf_model, x_test, y_test, "Random Forest")
    save_model(rf_model, preprocessor, "random_forest_model.pkl")

    gb_model = train_model(x_train, y_train, 'gradient_boosting')
    evaluate_model(gb_model, x_test, y_test, "Gradient Boosting")
    save_model(gb_model, preprocessor, "gradient_boosting_model.pkl")

    # SVM was commented out due to taking too long to train
    # svm_model = train_model(x_train, y_train, 'svm')
    # evaluate_model(svm_model, x_test, y_test, "SVM")
    # save_model(svm_model, preprocessor, "svm_model.pkl")
    
    print("Model training complete.")

main()

# print(get_data(DATA_PATH).info())
# print(get_data(DATA_PATH).describe())
# print(get_data(DATA_PATH).head())
# print(get_data(DATA_PATH).columns)