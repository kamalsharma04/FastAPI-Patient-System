![Python](https://img.shields.io/badge/Python-3.13-blue)
![Jupyter](https://img.shields.io/badge/Notebook-Jupyter-orange)Game Sales and Rating Prediction
# Patient Management System API 🏥

A robust and efficient FastAPI-based Patient Management System. This API handles full CRUD (Create, Read, Update, Delete) operations and includes automated health logic.

## 🚀 Features
- **Full CRUD Support**: Manage patient records seamlessly.
- **Automated Calculations**: Real-time BMI and health verdict calculation using Pydantic `@computed_field`.
- **Data Validation**: Strict schema enforcement with Pydantic models.
- **Persistent Storage**: Data is saved in a human-readable `patients.json` format.

## 🛠️ Tech Stack
- **FastAPI**: Modern, high-performance web framework.
- **Pydantic**: Data validation and settings management.
- **Uvicorn**: ASGI server for running the application.

## 💻 Installation & Setup

1. **Activate Virtual Environment**:
   ```bash
   myenv\Scripts\activate