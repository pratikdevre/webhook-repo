
# GitHub Webhook Tracker

This project listens to GitHub events like push, pull request, and merge via webhooks,
stores them in MongoDB Atlas, and displays them on a simple frontend.

---


## 🚀 How to Run This Project (For Recruiters)

### 1. Extract the ZIP File

Unzip the file to a folder like `webhook-tracker`.

---

### 2. Install Python Packages

Make sure Python is installed. Then open a terminal inside the folder and run:

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install flask pymongo flask-cors
```

---

### 3. Add MongoDB Connection

1. Open `config.py`
2. Replace the `MONGO_URI` value with your MongoDB Atlas connection string:

```python
MONGO_URI = "your_mongodb_uri_here"
```

---

### 4. Start the Flask Server

```bash
python app.py
```

Should run at: `http://127.0.0.1:5000`

---

### 5. (Optional) Test with Webhooks

To test real GitHub webhooks:

1. Start ngrok:
   ```bash
   ngrok http 5000
   ```

2. Copy the HTTPS URL and add it to your GitHub repo's webhooks:
   - Payload URL: `https://<your-ngrok>.ngrok-free.app/webhook`
   - Content type: `application/json`
   - Events: `push` and `pull request`

---

### 6. View the Frontend

Open this file in your browser:

```
templates/index.html
```

You’ll see real-time GitHub events listed.

---

### ✅ Done

Push or PR from GitHub and see the events show up live.

This project was built as part of the TechStaX Developer Assessment.
