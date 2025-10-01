# Spotify Playlist Data Pipeline & Analysis

## Overview

This project automates the process of extracting, transforming, and analyzing track data from a public Spotify playlist. The Python script (`data_extraction_from_api.py`) connects to the Spotify API, fetches data for a specified playlist (e.g., "best songs 2023"), extracts key details like track name, artist, album, and popularity, and saves the clean data into a CSV file. The accompanying Jupyter Notebook (`analysis.ipynb`) then uses this data to perform an initial analysis, identifying key statistics like average popularity and the most frequent artists.

## Technologies Used

  * **Python 3.10**
  * **Pandas:** For data manipulation and analysis.
  * **Requests:** For making HTTP requests to the Spotify API.
  * **Spotify Web API:** As the primary data source.

## Features

  * **Authentication:** Securely authenticates with the Spotify API using Client ID and Client Secret via the Client Credentials Flow.
  * **Data Extraction:** Searches for a playlist by name and extracts detailed information for all tracks within it.
  * **Data Storage:** Cleans and processes the extracted data, saving the results into a structured CSV file (`extracted_track_data.csv`).
  * **Data Analysis:** The notebook performs an initial exploratory data analysis to find:
      * The average popularity score of the playlist.
      * The most popular track.
      * The most frequently featured artists.

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
