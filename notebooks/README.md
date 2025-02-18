###  Task 1 - Data Analysis and Preprocessing
## Overview
The goal of this task is to prepare and refine the dataset for effective fraud detection. Proper data preprocessing ensures high-quality input for machine learning models, leading to improved accuracy and reliability. This involves handling missing values, cleaning data, performing exploratory data analysis (EDA), merging datasets for geolocation analysis, and extracting key features. Additionally, normalization, scaling, and encoding categorical features will be applied to ensure consistency and efficiency in model training.

## Steps:

- **Handling Missing Values**: Imputing or removing missing data to maintain dataset integrity.
- **Data Cleaning**: Removing duplicates and correcting data types to ensure accuracy.
- **Exploratory Data Analysis (EDA)**: Performing univariate and bivariate analysis to identify patterns and relationships.
- **Geolocation Analysis**: Converting IP addresses into integer format and merging fraud transaction data with geolocation data.
- **Feature Engineering**: Extracting insights like transaction frequency, velocity, and time-based features (e.g., hour of the day, day of the week).
- **Normalization & Scaling**: Standardizing numerical features for better model performance.
- **Encoding Categorical Features**: Converting categorical data into numerical format for machine learning algorithms.


# Development Instructions
- Create a feature/task-1 Branch for development.
- Commit progress regularly with clear and detailed commit messages.
- Merge updates into the main branch via a Pull Request (PR).

# Task-2 Model Building and Training 

## Overview
In this phase, the objective is to develop a machine learning model capable of accurately identifying fraudulent activities. The process includes:
## Steps:

1. Data Preparation:
- **Feature and Target Separation**:
    - Separate the features (independent variables) from the target variable (dependent variable).
    - In the 'creditcard' dataset, the target variable is labeled as 'Class'.
    - In the 'Fraud_Data' dataset, the target variable is labeled as 'class'.

- **Train-Test Split**:
    - Divide the dataset into training and testing subsets to evaluate model performance.

2. Model Selection:
   - **To compare the performance of various models, consider the following algorithms**:
        - Logistic Regression
        - Decision Tree
        - Random Forest
        - Gradient Boosting
        - Multi-Layer Perceptron (MLP)
        - Convolutional Neural Network (CNN)
        - Recurrent Neural Network (RNN)
        - Long Short-Term Memory (LSTM)

    - **Model Training and Evaluation**:
        - Training:
            - Train each selected model on the training dataset.
        - Evaluation:
            - Assess model performance using metrics such as accuracy, precision, recall, F1 score, and ROC-AUC.


# Development Instructions
- Create a feature/task-2 Branch for development.
- Commit progress regularly with clear and detailed commit messages.
- Merge updates into the main branch via a Pull Request (PR).

# Task-3 Model Explainability
## Overview

Understanding how a model makes decisions is crucial, especially in sensitive areas like fraud detection. This task focuses on implementing tools and techniques to interpret and explain model predictions.
## Steps:
- **Versioning and Experiment Tracking**:
    - Utilize tools like MLflow to track experiments, log parameters, metrics, and version models.
    - MLflow provides a platform for managing the complete machine learning lifecycle, including experimentation, reproducibility, and deployment. 

    
# Development Instructions
- Create a feature/task-3 Branch for development.
- Commit progress regularly with clear and detailed commit messages.
- Merge updates into the main branch via a Pull Request (PR).


# Task-4 Model Deployment and API Development
## Overview
The goal of this task is to deploy the trained fraud detection model and develop an API for seamless integration with external systems.

## Steps:
1. Create the Flask Application
    - **Create a new project directory:**
    ```bash
    mkdir fraud_detection_api && cd flask.
- **Create a Python script serve_model.py to serve the model using Flask**
- **Create a requirements.txt file to list dependencies.**

2. API Development
- **Install Dependencies**
   - Create a requirements.txt file with the necessary dependencies:
      ```bash
      pip install -r requirements.txt

- **Define API Endpoints**
   - Create `serve_model
        - Load the trained fraud detection model.
        - Define API endpoints for inference and health checks.
        - Log requests and responses for monitoring.

3. Test the API
- **Run the Flask App Locally**

4. Dockerizing the Flask Application

- **Create a Dockerfile in the same directory** 
  ```bash

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000 to allow external access
EXPOSE 5000

# Run the API using Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "serve_model:app"]

5. Build and Run the Docker Container
- **Build the Docker Image**
  ```bash
  docker build -t fraud-detection-model .

# Development Instructions
- Create a feature/task-4 Branch for development.
- Commit progress regularly with clear and detailed commit messages.
- Merge updates into the main branch via a Pull Request (PR).

# Task-5 Build a Dashboard with Flask and Dash
## Overview
Create an interactive dashboard using Dash for visualizing fraud Insights from your data. The Flask backend will serve data from the datasets, while Dash will be used to visualize insights.

## steps
1. Setting Up the Project
- **Create a new directory for the dashboard:**
    ```bash
    mkdir fraud_detection && cd fraud_detection_dashboard.
- **Install Required Libraries**
- Create a requirements.txt file and add the following dependencies:
    ```bash
    pip install -r requirements.txt

2. Dash Frontend - Interactive Dashboard
- Create app.py to visualize fraud insights.

3.Running the Dashboard
1. **Start the Flask API:**

        ```bash
        python app.py

2. **Start the Dash dashboard:**
         ```bash
         python dashboard.py

3. **Open the dashboard in your browser:**

             ```bash
        http://127.0.0.1:8050/
             
# Development Instructions
- Create a feature/task-5 Branch for development.
- Commit progress regularly with clear and detailed commit messages.
- Merge updates into the main branch via a Pull Request (PR).


