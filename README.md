# ♻️ EcoSorter: AI-Based Waste Segregation & Carbon Footprint Analyser

Welcome to **EcoSorter**, an interactive, AI-powered web application built to tackle the global waste crisis! This tool automatically classifies trash and calculates your carbon footprint savings in real-time.

Wrapped in an engaging, cyberpunk-themed user interface, EcoSorter makes recycling and waste management both accessible and visually striking.

## ✨ Key Features
* **Real-Time AI Classification:** Uses a custom-trained TensorFlow/Keras model to instantly identify waste via camera input.
* **Smart Categorization:** Automatically sorts items into Recyclable, Biodegradable, or Hazardous categories.
* **Carbon Footprint Tracking:** Calculates and displays a running total of estimated CO2 emissions saved (e.g., 0.5 kg CO2e saved per recyclable item).
* **Cyberpunk UI:** Built with Streamlit for a highly interactive and futuristic user experience.

## 📁 Repository Structure
* `app.py` — The main Python script that runs the Streamlit web app and the UI.
* `keras_model.h5` — The trained AI model that actually classifies the waste.
* `labels.txt` — The text file mapping the AI's output to the correct waste categories.
* `requirements.txt` — The list of required Python libraries needed to run the app.

## 🛠️ Tech Stack
* **Python 3**
* **Streamlit** (Frontend / UI)
* **TensorFlow / Keras** (Machine Learning)
* **Pillow (PIL)** (Image Processing)

## 🚀 How to Run the App (For Judges)

Follow these simple steps to run EcoSorter on your local machine.

### 1. Prerequisites
Make sure you have Python installed on your computer.

### 2. Install Dependencies
Open your terminal or command prompt, navigate to the folder containing this project, and run the following command to install the required libraries:

```bash
pip install -r requirements.txt
```

### 3. Launch the Application
Once the installation is complete, start the Streamlit server by running:

```bash
streamlit run app.py
```

Note: The system will automatically attempt to launch the dashboard in your default browser at http://127.0.0.1:5000.

4. System Access
The OS uses a self-registering database. Simply enter any Operator ID and Access Code to create a profile and unlock the dashboard.

The app will automatically open in your default web browser. Grant camera permissions when prompted to start sorting waste and saving carbon!

---
*Built for the Hackathon - Let's build a greener future together!*
