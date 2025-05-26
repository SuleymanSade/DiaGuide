# About the Project
## Inspiration
Diabetes affects a significant portion of the USA, with an estimated prevalence of 11%. This condition might impact people's lifestyle, and understanding one's personal risk might be a powerful indicator of the habits related to diet and activity. It also helps with directing high-risk people to hospitals, resulting in lowering further damage.

## What it does
* First, it asks the user to input certain information about themselves, such as age, physical health, etc.
* Then it feeds these parameters to a linear regression model that I built using historical diabetes data.
* Finally showcases the result at the end.

## ⚙️ Tools & Stack

### 🀄 Language(s)
- **Python**

---

### 💻 Frontend

**🔨 Tools & Libraries:**  
- [Streamlit]([https://streamlit.io/](https://diaguide.streamlit.app/))

**❓ Why I chose it:**  
I needed a simple library to create the layout — and I needed it fast 🏃‍♂️💨. As someone without much front-end experience, Streamlit helped me a lot. It’s beginner-friendly and has great documentation 📖 and tutorials. It was the perfect tool to create a data-heavy app with minimal UI design.

**🛠️ How I used it:**  
It was the cornerstone of my UI. Everything — from layout to interactivity — was built using 🐍 Python.  
No HTML, no CSS — just clean Python code.

---

### 🤖 Machine Learning

**🔨 Tools & Libraries:**  
- `scikit-learn`

**🔎 Model Type(s):**  
- Logistic Regression  
- Random Forest  
- Gradient Boosting

**🧹 Data Cleaning Libraries:**  
- `pandas`  
- `numpy`

**💪 Performance / Evaluation:**  
I trained 3 different models and evaluated them using ROC curves — this checks model performance on the test set, where:
- `1.0 = perfect`
- `0.5 = same as random guessing`

| Model              | ROC Score | Speed / Notes                         |
|--------------------|-----------|---------------------------------------|
| Logistic Regression| **0.81**  | ⚡ Very fast                           |
| Gradient Boosting  | 0.82      | ⏳ Okay speed                          |
| Random Forest      | 0.77      | 🐢 Significantly slowed server response|

**🏆 Result:**  
I chose **Logistic Regression** — the small accuracy difference wasn’t worth the slower response time of Gradient Boosting or Random Forest.

---

### 📊 Dataset

**🌐 Source:**  
[Kaggle - Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset/data)

**🔢 Features Used:**  
- BMI  
- Age  
- Blood Pressure  
- (and more)

**🤔 Why this dataset:**  
✅ Clean  
🏷️ Labeled  
🧠 Interpretable  

**📝 Additional Notes:**  
I excluded two columns — **education level** and **income** — because they were more personal and only increased accuracy by ~1%, which wasn’t significant.

---

### 🌐 Hosting & Deployment

**🚀 Where I deployed:**  
- [Streamlit Cloud](https://streamlit.io/cloud)

**🧑‍💻 GitHub Repository:**  
- [`SuleymanSade/DiaGuide`](https://github.com/SuleymanSade/DiaGuide)

**🌐 Live App:**  
- [DiaGuide App](https://your-app-link.streamlit.app) <!-- Replace with your real URL if you want -->

**🛠️ How I did it:**
1. Listed all required libraries in `requirements.txt`
2. Configured `git lfs` to handle large model files (>100MB)
3. Created the GitHub repo and pushed the code
4. Set up Streamlit Cloud for deployment

**❓ Why I used Streamlit Cloud:**  
It was free-to-use and super simple to set up. Plus, it syncs with GitHub — so any future code updates automatically refresh the app.



## Challenges we ran into
* Initially, it was a struggle to figure out the system to show questions one by one, but then with the use of functions and custom keys, I was able to resolve the issue.
* Another issue was with the speed of the web app. I initially used random forest as my model, but it significantly slowed down the web app and made it harder to answer questions, and even caused it to crash. However, after switching to logistic regression and experimenting with it, both the accuracy and the speed had increased.
* Uploading these files was a struggle due to large file sizes, but we were able to launch it thanks to Git LFS

## Accomplishments that we're proud of
* I am proud of getting a ROC value of 0.81, while fixing my previous speed issues was a huge success.
* I am happy with being able to publish a fully functional web app that provides decent results to the user.

## What we learned
* This is my first time using Streamlit to build a web app, and I learned a lot about how to create different properties and the basics of how they work. This was also my first time using Python for the front-end of a web app.
* I learned how to better evaluate different models and improved my knowledge of them.

## What's next for DiaGuide
* I want to implement GridSearch on the models so that I get the best parameters to run with, and maybe even try other tools to train models for better results.
* I also want to implement a system that keeps track of user data in a SQL database, including a second questionnaire that asks users about their daily blood pressure and similar values, and warns them about significant changes over time.
* I am also planning to ask more questions to predict other commonly seen conditions and train more models with their data.

You can easily access the project in: <https://diaguide.streamlit.app/>
The demo for the web app: <https://youtu.be/fp0EZWSssPQ>
Also check out Devpost project: <https://devpost.com/software/diaguide>
