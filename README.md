# PlantGuard-AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Computer Vision](https://img.shields.io/badge/Computer_Vision-Plant_Disease_Detection-2E8B57?style=flat)

AI-based plant disease detection using both Deep Learning and Classical Machine Learning pipelines, developed for comparative analysis, experimentation, and real-time deployment through a Streamlit application.

</div>

---

# Overview

PlantGuard-AI is a computer vision project focused on automated plant disease classification from leaf images.  
The project combines two independent approaches:

- a transfer learning pipeline based on **EfficientNetV2B0**
- a feature-based Classical ML pipeline using **ResNet50 + PCA + Ensemble Learning**

Rather than focusing only on prediction accuracy, the project was designed to explore how different learning paradigms behave under the same classification problem. This includes model performance, feature representation, confidence behavior, and deployment practicality.

The repository also includes an interactive Streamlit application that allows users to upload plant leaf images and receive real-time predictions with disease information, severity estimation, and treatment recommendations.

---

# Motivation

Plant disease detection is a common application of computer vision in agriculture, but many implementations focus exclusively on a single deep learning model.

This project takes a broader approach by comparing:

- end-to-end deep learning
- feature extraction with traditional machine learning

The goal was to better understand the trade-offs between both approaches while building a complete and deployable AI workflow instead of an isolated notebook experiment.

The project also served as a practical study in:
- transfer learning
- feature engineering
- dimensionality reduction
- ensemble learning
- model evaluation
- AI application deployment

---

# System Architecture

## Deep Learning Pipeline

The deep learning branch uses transfer learning with EfficientNetV2B0 trained on augmented leaf image data.

### Workflow

```text
Input Image
   ↓
Data Augmentation
   ↓
EfficientNetV2B0
   ↓
Dense Classification Layers
   ↓
Disease Prediction
```

### Core Components

- EfficientNetV2B0 backbone
- Transfer Learning
- Data Augmentation
- Fine-Tuning
- Softmax Classification

This pipeline achieved the strongest overall classification performance during evaluation, particularly for visually similar disease categories.

---

## Classical Machine Learning Pipeline

The second pipeline follows a feature-based workflow where deep visual features are extracted first and then passed into traditional ML classifiers.

### Workflow

```text
Input Image
   ↓
ResNet50 Feature Extraction
   ↓
Feature Scaling
   ↓
PCA Dimensionality Reduction
   ↓
ML Classifiers
   ↓
Voting Ensemble
```

### Models Used

- Logistic Regression
- Support Vector Machine (SVM)
- Random Forest
- K-Nearest Neighbors (KNN)
- Voting Ensemble

This branch was included to evaluate how well classical ML methods perform when supported by high-quality extracted visual features.

---

# Comparative Analysis

One of the central parts of the project was comparing both pipelines under the same dataset and evaluation conditions.

| Aspect | Deep Learning Pipeline | Classical ML Pipeline |
|---|---|---|
| Learning Strategy | End-to-End Representation Learning | Feature-Based Learning |
| Backbone | EfficientNetV2B0 | ResNet50 Feature Extraction |
| Dimensionality Reduction | Not Required | PCA |
| Classifiers | Dense Neural Layers | LR, SVM, RF, KNN |
| Interpretability | Moderate | Higher |
| Training Complexity | Higher | Moderate |
| Generalization | Stronger | Moderate |
| Prediction Stability | High | Variable |
| Best Overall Accuracy | 98.8% | 92.3% |

### Key Observations

- EfficientNetV2 generalized better across visually overlapping diseases.
- The ensemble pipeline produced competitive results on structured extracted features.
- PCA reduced redundancy and improved ML training efficiency.
- Transfer learning significantly reduced training time while improving convergence stability.

The comparison itself became one of the most valuable outcomes of the project because it highlighted practical differences between modern deep learning workflows and traditional ML pipelines.

---

# Streamlit Application

The repository includes a complete Streamlit-based interface for real-time inference and experimentation.

### Features

- Upload plant leaf images
- Select prediction pipeline
- Compare DL and ML outputs
- Display confidence scores
- Disease descriptions
- Severity estimation
- Treatment recommendations
-The application provides a unified inference layer where both models can be executed and compared in real-time through a single GUI.

The interface was designed to move beyond a minimal prototype and provide a cleaner deployment experience suitable for demonstrations and research presentations.

---

# Dataset

The models were trained and evaluated using the /kaggle/input/datasets/vipoooool/new-plant-diseases-dataset, a widely used benchmark dataset for plant disease classification tasks.

### Dataset Summary

| Category | Value |
|---|---|
| Plant Species | 14 |
| Disease Classes | 38 |
| Data Type | RGB Leaf Images |
| Task Type | Multi-Class Classification |

### Supported Plant Categories

- Tomato
- Potato
- Apple
- Corn
- Grape
- Peach
- Pepper
- Strawberry

---

# Results

## Performance Summary

> Replace placeholder values below with final evaluation metrics.

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| EfficientNetV2B0 | 98.8% | 98.9% | 98.9% | 98.8% |
| Voting Ensemble | 92.3% | 92.6% | 92.3% | 92.3% |
| SVM | 92.9% | 93.2% | 92.3% | 92% |
| Random Forest | 87.4% | 87.9% | 87.4% | 87.3% |

### Evaluation Notes

The EfficientNetV2 pipeline consistently achieved the best overall performance, especially on disease classes with subtle texture differences and complex visual patterns.

The classical ML ensemble remained competitive in several categories, particularly after feature extraction and PCA optimization, though prediction consistency varied more across difficult classes.

---

# Project Structure

```bash
PlantGuard-AI/
|
├── streamlit_app.py
│   
│
├── models/
│   ├── final_model.keras
│   ├── ensemble.pkl
│   └── class_names.json
│
├── notebooks.ipynb
│  
│
├── assets/
│   ├── gui.png
│   └── confusion_matrix.png
│
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/PlantGuard-AI.git
cd PlantGuard-AI
```

---

## Create Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Streamlit Application

```bash
streamlit run app/streamlit_app.py
```

---

# Research Contribution

This project contributes a comparative implementation of:

- transfer learning for agricultural disease classification
- feature-based Classical ML workflows using deep extracted representations
- ensemble learning for plant disease prediction
- deployable AI inference through Streamlit

The repository was developed not only as a classification system, but also as an applied study of how different learning paradigms behave within the same computer vision problem.

---

# What I Learned

Working on both pipelines provided practical insight into the differences between:
- representation learning
- handcrafted ML workflows
- transfer learning strategies
- ensemble behavior
- deployment-oriented AI engineering

One of the most important observations was that strong feature extraction can still make classical ML surprisingly competitive, even when compared against modern CNN architectures.

The project also reinforced that building a usable AI system involves more than model training alone — deployment, interface design, and evaluation workflow matter just as much.

---

## Future Work

This project may be extended into a research paper focusing on comparative analysis between deep learning and classical machine learning approaches for plant disease detection.

---

# Author

Aya Mahmoud Alhareidi  
Computer Science / Artificial Intelligence Student

Focused on Computer Vision, Machine Learning, and applied AI systems with an interest in practical deployment and research-oriented development.

---
