# Fake Money Detection System

This repository contains the code for a fake banknote detection system. It utilizes machine learning to classify banknote images as either real or fake based on features extracted using image processing techniques. The system includes a training script, a logic module for feature extraction and prediction, and a graphical user interface (GUI) for easy interaction.
##Keywords

* **Fake Banknote Detection**
* **Machine Learning**
* **Computer Vision**
* 
## Overview

The project consists of the following main components:

* **`modeling.ipynb`**: A Jupyter Notebook containing the steps for training the machine learning model.
* **`logic.py`**: A Python module that implements the core logic for image processing (Sobel edge detection, feature extraction) and prediction using the trained model.
* **`GUI.py`**: A Python script that provides a user-friendly graphical interface for uploading banknote images and getting real-time predictions.
* **`model.joblib`**: (This file will be generated after running `modeling.ipynb`) The serialized trained machine learning model.
* **`gui/detective.png`**: (Optional) A logo image used in the GUI.
* **`data_banknote_authentication.txt`**: (Assumed) The dataset used for training the model.

## Getting Started

To run this project, you will need to have Python 3 installed on your system, along with the necessary libraries.

### Prerequisites

* **Python 3**
* **Libraries (install using pip):**
    ```bash
    pip install pandas scikit-learn numpy opencv-python scikit-image joblib matplotlib pillow
    ```

### Developers

* Abdulrahman Mohamed
* Abdulrahman Nasser
* Amr Khaled El Sayed
* Abdulrahman Fawzi

## License

this project can be used for anyone
