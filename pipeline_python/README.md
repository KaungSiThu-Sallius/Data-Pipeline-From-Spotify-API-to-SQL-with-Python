# Automated Spotify Data Pipeline
## Overview

This project is a fully automated, end-to-end **ETL (Extract, Transform, Load)** pipeline that fetches data from the **Spotify API**, processes it, and loads it into a local **SQLite** database.  
The entire process is tested and scheduled to run daily using a **CI/CD workflow** with **GitHub Actions**.

The pipeline performs the following key steps:

1. **Extract:** Connects to the Spotify API and retrieves all tracks from a specified playlist (e.g., *"best songs 2023"*).  
2. **Transform:** Cleans the raw data using **Pandas**, validates data types, removes duplicates, and performs feature engineering to create a `popularity_tier` for each track.  
3. **Load:** Stores the final, analysis-ready dataset into a structured **SQLite** database.  

---

## Key Features

- **Automated ETL Process:** A single, modular Python script (`pipeline.py`) handles the entire data workflow.  
- **CI/CD Automation:** The pipeline is automatically executed daily using **GitHub Actions**, ensuring the data is always up-to-date.  
- **Unit Testing:** The data transformation logic is validated by a suite of unit tests written with **pytest**, ensuring code reliability and correctness.  
- **Secure Credential Management:** API keys and secrets are handled securely using **GitHub Secrets** in the automated workflow and a `.env` file for local development.  
- **Feature Engineering:** The script enriches the raw data by creating new, insightful features like a categorical `popularity_tier`.  

---

## Technologies Used

- **Python 3.10**  
- **Libraries:** Pandas, Requests, NumPy  
- **Database:** SQLite  
- **Testing:** pytest  
- **Automation:** GitHub Actions  

---

## Project Structure

```plaintext
├── pipeline_python/  
    ├── .github/workflows/    
    ├── tests/               
    │   ├── __init__.py
    │   └── test_pipeline.py
    ├── .gitignore           
    ├── pipeline.py          
    ├── README.md             
    └── requirements.txt      
```

## How to Run

1.  **Clone the repository.**
2.  **Set up your environment:**
      * Create a `.env` file in the root directory.
      * Add your Spotify credentials to the `.env` file:
        ```
        CLIENT_ID="your_client_id_here"
        CLIENT_SECRET="your_client_secret_here"
        ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the data extraction script:**
    ```bash
    python data_extraction.py
    ```
5.  **Explore the analysis:** Open and run the `analysis.ipynb` notebook in a Jupyter environment to see the results.

---

## Blog Post

I wrote a detailed article explaining the process of building this pipeline. You can read it on Medium:

[Building My First Data Pipeline: From Spotify API to SQL with Python](https://medium.com/@kaungsithu.sallius/building-my-first-data-pipeline-from-spotify-api-to-sql-with-python-fff78ca0376e)
