# 💳 Credit Card Fraud Detection & Attack Prediction 🔍

![image](https://github.com/user-attachments/assets/7c60299e-a4af-4725-a5d8-ea2c3f3ce47f)


🚀 **Project Overview**  
This project leverages **Gaussian Mixture Model (GMM)** for fraud detection, helping financial institutions identify fraudulent transactions efficiently. It provides insights into attack types and preventive measures through a **web-based dashboard**.

---

## 🏆 Features  
✅ **Batch-Based Analysis**: Upload CSV files containing transaction history.  
✅ **Fraud Detection**: Uses **GMM** to detect anomalies.  
✅ **Attack Classification**: Identifies fraud types (Phishing, Skimming, etc.).  
✅ **Data Security**: Implements **AES Encryption** for sensitive fields.  
✅ **Web-Based Interface**: Displays flagged transactions with risk scores.  

---

## 🛠️ Technologies Used  
🔹 **Machine Learning**: Gaussian Mixture Model (GMM)  
🔹 **Backend**: Python, Flask, Flask-CORS  
🔹 **Frontend**: HTML, CSS, JavaScript  
🔹 **Database**: PostgreSQL / MySQL  
🔹 **Data Security**: AES Encryption  
🔹 **Data Processing**: Pandas, NumPy  
🔹 **Visualization**: Matplotlib, Seaborn  

---

## 🏗️ System Workflow  
1️⃣ Upload **CSV file** containing past transactions.  
2️⃣ **AES Encryption** secures card details.  
3️⃣ **GMM model** flags fraudulent transactions.  
4️⃣ Attack **classification module** identifies fraud type.  
5️⃣ User can **download reports** for further analysis.  

---

## 🚀 How to Run  

### 🌐 Go Live for Web Application  
Simply open `index.html` in your browser or use **Live Server Extension** in VS Code.  

### 🖥️ Backend Setup (Fraud Detection Model)  
Run these commands in the terminal:  

```bash
python -m venv fraudshield-env
source fraudshield-env/bin/activate
pip install flask flask-cors pymongo pandas scikit-learn numpy matplotlib joblib flask-jwt-extended python-dotenv
pip install category-encoders
pip install category-encoders pandas numpy scikit-learn flask flask-cors
python app.py
python app_wrapper.py
```

---

📌 Click on the localhost URL to access the web interface 
👉 The webpage is connected to a trained GMM model using AES encryption for security. 


## 📈 Future Enhancements

🚀 Real-time fraud detection instead of batch processing.  
🚀 User-level fraud alerts via notifications.  
🚀 API Integration for banks for seamless fraud detection.  
🚀 Advanced AI models (LSTMs, Autoencoders) for improved accuracy.  


### 💡 Contributing
🙌 Contributions are welcome! Feel free to fork this repo and submit PRs.
