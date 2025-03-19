from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import pandas as pd
import numpy as np
import json
import subprocess
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    """Serve the HTML page for uploading files"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FraudShield | Upload Transactions</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            /* Upload Form Styles */
            .form-container, .upload-container, .help-content {
              width: 100%;
              max-width: 800px;
              background-color: white;
              padding: 40px;
              border-radius: 10px;
              box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .upload-container {
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
              margin: 0 auto;
            }
            
            form {
              display: flex;
              flex-direction: column;
              align-items: center;
              width: 100%;
            }
            
            .form-group, .upload-container {
              width: 100%;
              margin-bottom: 20px;
            }
            
            .form-group label {
              display: block;
              margin-bottom: 10px;
              text-align: left;
            }
            
            .form-group input, #fileUpload {
              width: 100%;
              padding: 10px;
              border: 1px solid #ddd;
              border-radius: 5px;
              text-align: left;
            }
            
            .btn-primary {
              background-color: #3498db;
              color: white;
              border: none;
              padding: 12px 24px;
              border-radius: 5px;
              cursor: pointer;
              transition: background-color 0.3s ease;
              margin-top: 5px;
              width: 100%;
            }
            
            .btn-primary:hover {
              background-color: #2980b9;
            }
            
            /* Apply the same width, padding, and display properties to both buttons */
            .btn-secondary {
              background-color: var(--gray-color);
              color: white;
              border: none;
              padding: 12px 24px; /* Ensure equal padding */
              border-radius: 5px;
              cursor: pointer;
              transition: background-color 0.3s ease;
              text-decoration: none;
              text-align: center;
              margin-top: 5px;
              display: inline-block;
              width: 100%; /* Make both buttons full width or set a fixed width */
            }
            
            /* Optional: hover effect for both buttons */
            .btn-secondary:hover {
              background-color: #5a6268;
            }
            
            .form-footer, .file-help {
              margin-top: 15px;
              text-align: center;
              color: #666;
            }
            
            /* Alert styles */
            .alert-message {
              padding: 10px;
              margin-bottom: 15px;
              border-radius: 5px;
              text-align: center;
              display: none;
            }
            
            .alert-message.success {
              background-color: var(--success-color);
              color: white;
            }
            
            .alert-message.error {
              background-color: var(--danger-color);
              color: white;
            }
            
            /* Form check styling */
            .form-check {
              display: flex;
              align-items: center;
              width: 100%;
              margin-bottom: 20px;
              text-align: left;
            }
            
            .form-check input[type="checkbox"] {
              width: auto;
              margin-right: 10px;
            }
            
            .form-check label {
              margin-bottom: 0;
            }
            
            /* Upload progress styling */
            .upload-progress {
              width: 100%;
              text-align: center;
              padding: 20px;
              background-color: #f8f9fa;
              border-radius: 8px;
              margin-top: 20px;
            }
            
            .upload-progress h3 {
              color: var(--primary-color);
              margin-bottom: 15px;
            }
            
            .progress-bar {
              width: 100%;
              height: 20px;
              background-color: #e9ecef;
              border-radius: 10px;
              overflow: hidden;
              margin-bottom: 10px;
            }
            
            .progress-fill {
              height: 100%;
              background-color: var(--primary-color);
              width: 0;
              transition: width 0.5s ease;
            }
            
            /* Hidden class styling */
            .hidden {
              display: none;
            }
            
            /* Select styling - ensuring consistency */
            select {
              width: 100%;
              padding: 10px;
              border: 1px solid #ddd;
              border-radius: 5px;
              background-color: white;
            }
            
            /* Additional enhancement for the file input */
            input[type="file"] {
              padding: 8px;
              border: 1px solid #ddd;
              border-radius: 5px;
              background-color: white;
            }
            
            /* Ensure consistent styling for progress text */
            #progressText {
              color: var(--gray-color);
              font-size: 0.9rem;
            }

            /* Additional styles needed for the rest of the layout */
            :root {
                --primary-color: #3498db;
                --secondary-color: #2c3e50;
                --success-color: #2ecc71;
                --danger-color: #e74c3c;
                --warning-color: #f39c12;
                --gray-color: #7f8c8d;
            }
            
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
                color: #333;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            h1 {
                color: var(--secondary-color);
                margin-bottom: 30px;
            }
            
            /* Navigation */
            .main-nav {
                background-color: white;
                padding: 15px 20px;
                color: black;
            }
            
            .main-nav > div {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .nav-logo {
                display: flex;
                align-items: center;
                font-size: 1.5rem;
                font-weight: bold;
            }
            
            .nav-logo i {
                margin-right: 10px;
                color: var(--primary-color);
            }
            
            .nav-logo a {
                color: black;
                text-decoration: none;
            }
            
            .nav-buttons {
                display: flex;
            }
            
            .nav-button {
                color: black;
                text-decoration: none;
                padding: 8px 15px;
                margin-left: 5px;
                border-radius: 4px;
                transition: background-color 0.3s;
            }
            
            .nav-button:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            .nav-button.active {
                background-color: var(--primary-color);
            }
            
            /* Introduction section */
            .introduction {
                margin-bottom: 30px;
            }
            
            /* Footer */
            footer {
                background-color: var(--secondary-color);
                color: white;
                text-align: center;
                padding: 20px;
                margin-top: 50px;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .main-nav > div {
                    flex-direction: column;
                }
                
                .nav-buttons {
                    margin-top: 15px;
                }
                
                .nav-button {
                    padding: 8px 10px;
                    font-size: 0.9rem;
                }
            }
            
            /* Result styles */
            .result-summary {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                text-align: center;
            }
            
            .fraud-transaction {
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            
            .fraud-transaction h4 {
                color: var(--danger-color);
                margin-top: 0;
            }
            
            .transaction-details {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-bottom: 15px;
            }
            
            .fraud-reason, .prevention-methods {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 6px;
                margin-top: 10px;
            }
            
            .fraud-reason h5, .prevention-methods h5 {
                color: var(--secondary-color);
                margin-top: 0;
            }
        </style>
    </head>
    <body>
        <nav class="main-nav">
            <div>
                <div class="nav-logo">
                    <i class="fas fa-shield-alt"></i>
                    <a href="index.html">FraudShield</a>
                </div>
                <div class="nav-buttons">
                    <a href="index.html" class="nav-button">Home</a>
                    <a href="upload.html" class="nav-button active">Upload</a>
                    <a href="help.html" class="nav-button">Help</a>
                </div>
            </div>
        </nav>

        <div class="container">
            <section id="upload">
                <h1>Upload Transactions</h1>
                <div class="upload-container">
                    <div class="introduction">
                        <p>Upload your transaction data for fraud detection analysis. Our system will scan your file and identify potential fraudulent activities.</p>
                        <p>Upload Guidelines:</p>
                        <ul>
                            <li>Only CSV files are supported</li>
                            <li>Maximum file size: 10MB</li>
                            <li>Ensure your file includes transaction date, amount, and merchant information</li>
                            <li>Remove any sensitive personal data before uploading</li>
                        </ul>
                    </div>
                    
                    <form id="uploadForm">
                        <div class="form-group">
                            <label for="fileUpload">Upload CSV File</label>
                            <input type="file" id="fileUpload" accept=".csv" required>
                        </div>
                        
                        <div class="form-check">
                            <input type="checkbox" id="generateReport" checked>
                            <label for="generateReport">Generate detailed report after analysis</label>
                        </div>
                        
                        <button type="submit" class="btn-primary">
                            <i class="fas fa-search"></i> Upload & Detect Fraud
                        </button>
                    </form>
                    
                    <div class="upload-progress hidden" id="uploadProgress">
                        <h3>Analyzing Transactions</h3>
                        <div class="progress-bar">
                            <div class="progress-fill" id="progressFill"></div>
                        </div>
                        <p id="progressText">Uploading file...</p>
                    </div>
                </div>
            </section>
        </div>

        <footer>
            <p>&copy; 2025 FraudShield. All rights reserved.</p>
            <p>Contact: support@fraudshield.com</p>
        </footer>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Handle the upload form functionality
                const uploadForm = document.getElementById('uploadForm');
                const fileUpload = document.getElementById('fileUpload');
                const generateReport = document.getElementById('generateReport');
                const uploadProgress = document.getElementById('uploadProgress');
                const progressFill = document.getElementById('progressFill');
                const progressText = document.getElementById('progressText');
                
                if (uploadForm) {
                    uploadForm.addEventListener('submit', function(e) {
                        e.preventDefault();
                        
                        // Validate file selection
                        if (!fileUpload.files || fileUpload.files.length === 0) {
                            showAlert('Please select a CSV file to upload');
                            return;
                        }
                        
                        const file = fileUpload.files[0];
                        
                        // Validate file type
                        if (file.type !== 'text/csv' && !file.name.toLowerCase().endsWith('.csv')) {
                            showAlert('Please upload a valid CSV file');
                            return;
                        }
                        
                        // Validate file size (10MB limit)
                        const maxFileSize = 10 * 1024 * 1024; // 10MB
                        if (file.size > maxFileSize) {
                            showAlert('File size exceeds 10MB limit');
                            return;
                        }
                        
                        // Show progress bar
                        uploadForm.style.display = 'none';
                        uploadProgress.classList.remove('hidden');
                        
                        // Simulate progress
                        let progress = 0;
                        const progressInterval = setInterval(() => {
                            progress += 5;
                            progressFill.style.width = progress + '%';
                            
                            if (progress < 30) {
                                progressText.textContent = 'Uploading file...';
                            } else if (progress < 60) {
                                progressText.textContent = 'Analyzing transactions...';
                            } else if (progress < 90) {
                                progressText.textContent = 'Detecting fraud patterns...';
                            } else {
                                progressText.textContent = 'Generating report...';
                            }
                            
                            if (progress >= 100) {
                                clearInterval(progressInterval);
                                
                                // Prepare data to send to backend
                                const formData = new FormData();
                                formData.append('file', file);
                                formData.append('generateReport', generateReport.checked);
                                
                                // Send to backend
                                fetch('/process-csv', {
                                    method: 'POST',
                                    body: formData
                                })
                                .then(response => {
                                    if (!response.ok) {
                                        throw new Error('Server returned an error');
                                    }
                                    return response.json();
                                })
                                .then(data => {
                                    if (data.error) {
                                        throw new Error(data.error);
                                    }
                                    
                                    // Show success message
                                    showAlert('File processed successfully!', 'success');
                                    
                                    // Display results
                                    let resultsHTML = `
                                        <div class="result-summary">
                                            <h3>Analysis Complete</h3>
                                            <p>Found ${data.fraudCount} fraudulent transactions out of ${data.totalCount} total transactions.</p>
                                        </div>
                                    `;
                                    
                                    if (data.fraudCount > 0) {
                                        resultsHTML += '<h3>Fraudulent Transactions</h3>';
                                        
                                        data.fraudTransactions.forEach((item, index) => {
                                            resultsHTML += `
                                                <div class="fraud-transaction">
                                                    <h4>Fraudulent Transaction #${index + 1}</h4>
                                                    <div class="transaction-details">
                                                        <p><strong>Transaction ID:</strong> ${item.transaction_id || 'N/A'}</p>
                                                        <p><strong>Card Number:</strong> ${item.card_number || 'N/A'}</p>
                                                        <p><strong>Amount:</strong> $${item.amount || 'N/A'}</p>
                                                        <p><strong>Date:</strong> ${item.date || 'N/A'}</p>
                                                        <p><strong>Merchant:</strong> ${item.merchant || 'N/A'}</p>
                                                        <p><strong>Fraud Type:</strong> ${item.fraud_type || 'N/A'}</p>
                                                    </div>
                                                    <div class="fraud-reason">
                                                        <h5>Why This Is Flagged as Fraud:</h5>
                                                        <p>${item.reason}</p>
                                                    </div>
                                                    <div class="prevention-methods">
                                                        <h5>Prevention Methods:</h5>
                                                        <ul>
                                                            ${item.prevention.map(method => `<li>${method}</li>`).join('')}
                                                        </ul>
                                                    </div>
                                                </div>
                                            `;
                                        });
                                    } else {
                                        resultsHTML += '<p>No fraudulent transactions detected.</p>';
                                    }
                                    
                                    // Add a button to upload another file
                                    resultsHTML += `
                                        <button id="uploadAnother" class="btn-primary">
                                            <i class="fas fa-upload"></i> Upload Another File
                                        </button>
                                    `;
                                    
                                    // Update the container with the results
                                    const container = document.querySelector('.upload-container');
                                    if (container) {
                                        container.innerHTML = resultsHTML;
                                        
                                        // Add event listener to the "Upload Another" button
                                        const uploadAnotherBtn = document.getElementById('uploadAnother');
                                        if (uploadAnotherBtn) {
                                            uploadAnotherBtn.addEventListener('click', function() {
                                                // Reset form and show it again
                                                fileUpload.value = '';
                                                container.innerHTML = '';
                                                
                                                // Re-add the original elements
                                                container.appendChild(document.createElement('div')).className = 'introduction';
                                                container.querySelector('.introduction').innerHTML = `
                                                    <p>Upload your transaction data for fraud detection analysis. Our system will scan your file and identify potential fraudulent activities.</p>
                                                    <p>Upload Guidelines:</p>
                                                    <ul>
                                                        <li>Only CSV files are supported</li>
                                                        <li>Maximum file size: 10MB</li>
                                                        <li>Ensure your file includes transaction date, amount, and merchant information</li>
                                                        <li>Remove any sensitive personal data before uploading</li>
                                                    </ul>
                                                `;
                                                
                                                // Add the upload form back
                                                container.appendChild(uploadForm);
                                                uploadForm.style.display = 'flex';
                                                
                                                // Reset progress bar
                                                progressFill.style.width = '0%';
                                                uploadProgress.classList.add('hidden');
                                            });
                                        }
                                    }
                                })
                                .catch(error => {
                                    // Hide loading indicator and show error
                                    uploadProgress.classList.add('hidden');
                                    uploadForm.style.display = 'flex';
                                    showAlert('Error: ' + error.message);
                                });
                            }
                        }, 100);
                    });
                }
                
                // Utility function to show alerts
                function showAlert(message, type = 'error') {
                    // Find the nearest container for feedback
                    const alertContainer = document.querySelector('.form-container, .upload-container, .container');
                    if (alertContainer) {
                        // Create or find existing alert element
                        let alertElement = alertContainer.querySelector('.alert-message');
                        if (!alertElement) {
                            alertElement = document.createElement('div');
                            alertElement.className = 'alert-message';
                            alertContainer.insertBefore(alertElement, alertContainer.firstChild);
                        }

                        // Set alert content and style
                        alertElement.textContent = message;
                        alertElement.className = `alert-message ${type === 'success' ? 'success' : 'error'}`;
                        alertElement.style.display = 'block';

                        // Hide alert after 5 seconds
                        setTimeout(() => {
                            alertElement.style.display = 'none';
                        }, 5000);
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/process-csv', methods=['POST'])
def process_csv():
    try:
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        # If user doesn't select file, browser might submit an empty part without filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Save the file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Create a Python script to analyze the data
        analysis_script = """
import pandas as pd
import numpy as np
import json
import os
import sys
import traceback

# Wrap everything in try/except to catch and report errors
try:
    # Set the file path from command line argument
    csv_path = sys.argv[1]
    output_path = sys.argv[2]

    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Uncomment the following if you want to use your GMM module directly
    # Set up path to import your GMM module if needed
    # sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # try:
    #     import GMM.GMM as gmm_module
    #     # If GMM module has functions we can call directly:
    #     # fraudulent_indices = gmm_module.detect_fraud(df)
    # except ImportError:
    #     print("Warning: Could not import GMM module. Using fallback analysis.")
    
    # Process the data (this would be replaced by your GMM model)
    fraud_transactions = []
    
    # Clean column names - remove any ObjectId entries and standardize keys
    clean_df = pd.DataFrame()
    for col in df.columns:
        # Skip columns that contain ObjectId
        if 'ObjectId' in str(col):
            continue
        # Clean the column name and add to clean_df
        clean_name = col.strip()
        clean_df[clean_name] = df[col]
    
    # Replace df with our cleaned dataframe
    df = clean_df

    # Identify suspicious transactions
    for idx, row in df.iterrows():
        fraud_score = 0
        fraud_reasons = []
        
        # Convert values to appropriate types safely
        try:
            amount = float(row.get('Transaction Amount', 0))
        except (ValueError, TypeError):
            amount = 0
            
        # Get transaction source safely
        transaction_source = str(row.get('Transaction Source', '')).strip()
        
        # Get transaction notes safely
        transaction_notes = str(row.get('Transaction Notes', '')).strip()
        
        # Get fraud flag safely
        try:
            fraud_flag = int(row.get('Fraud Flag or Label', 0))
        except (ValueError, TypeError):
            fraud_flag = 0
        
        # Apply fraud detection rules
        if amount > 5000:
            fraud_score += 0.5
            fraud_reasons.append("High transaction amount ($" + str(amount) + " due to possibly account takeover.)")
        
        if transaction_source.lower() == 'online':
            fraud_score += 0.3
            fraud_reasons.append("Possibly due to Card Cloning")
        
        if 'suspicious' in transaction_notes.lower():
            fraud_score += 0.8
            fraud_reasons.append("Possibly caused due to phishing attack.")
        
        # Check if the transaction is marked as fraud in the dataset
        if fraud_flag == 1:
            fraud_score = 1.0
            fraud_reasons.append("Fraud Detected due to possibly skimming.")
        
        # If fraud score exceeds threshold, mark as fraud
        if fraud_score >= 0.5:
            fraud_type = "General Fraud"
            
            # Determine fraud type (example logic)
            if transaction_source.lower() == 'online':
                fraud_type = "Card Not Present"
            elif amount > 10000:
                fraud_type = "High-Value Fraud"
            
            # Get transaction details safely
            card_number = str(row.get('Card Number', 'Unknown'))
            # Mask all but the last 4 digits of the card number for security
            if len(card_number) > 4:
                card_number = '*' * (len(card_number) - 4) + card_number[-4:]
                
            transaction_data = {
                'transaction_id': str(row.get('Transaction ID', f"TX{idx}")),
                'card_number': card_number,
                'amount': amount,
                'date': str(row.get('Transaction Date and Time', 'Unknown')),
                'merchant': str(row.get('Merchant Name', 'Unknown')),
                'fraud_type': fraud_type,
                'reason': " & ".join(fraud_reasons) if fraud_reasons else "Suspicious pattern detected",
                'prevention': [
                    'Verify cardholder identity with additional authentication',
                    'Contact cardholder to confirm transaction',
                    'Temporarily block card until verification',
                    'Monitor account for additional suspicious activity'
                ]
            }
            fraud_transactions.append(transaction_data)

    # Write results to output file
    with open(output_path, 'w') as f:
        json.dump({
            'total_count': len(df),
            'fraud_count': len(fraud_transactions),
            'fraud_transactions': fraud_transactions
        }, f)
        
except Exception as e:
    # Print the full traceback for debugging
    traceback.print_exc()
    # Write error to output file so it can be displayed to the user
    with open(output_path, 'w') as f:
        json.dump({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, f)
    # Exit with error code
    sys.exit(1)
        """
        
        # Create a temporary file for the analysis script
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
            f.write(analysis_script.encode('utf-8'))
            analysis_script_path = f.name
        
        # Create a temporary file for the output
        output_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        output_path = output_file.name
        output_file.close()
        
        # Run the analysis script
        command = f"python {analysis_script_path} {filepath} {output_path}"
        process = subprocess.run(command, shell=True, capture_output=True)
        
        # Read the output
        with open(output_path, 'r') as f:
            results = json.load(f)
        
        # Check if there was an error in the analysis script
        if 'error' in results:
            error_message = f"Analysis error: {results['error']}\n\nDetails: {results.get('traceback', 'No traceback available')}"
            # Clean up temporary files
            os.remove(filepath)
            os.remove(analysis_script_path)
            os.remove(output_path)
            return jsonify({'error': error_message}), 500
        
        # Clean up temporary files
        os.remove(filepath)
        os.remove(analysis_script_path)
        os.remove(output_path)
        
        return jsonify({
            'success': True,
            'totalCount': results['total_count'],
            'fraudCount': results['fraud_count'],
            'fraudTransactions': results['fraud_transactions']
        })
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)