# Books to Scrape Project

This project scrapes book data from the [Books to Scrape](http://books.toscrape.com/) website. It retrieves information about books in each category, saves this data into CSV files, and downloads book images into a local directory.

## Features

- Scrapes book data (title, price, stock, rating, etc.) from multiple categories.
- Saves book data to CSV files.
- Downloads book cover images into a structured directory.
- Handles pagination for categories with multiple pages of books.

## Requirements

- Python 3.8+
- `pip` (Python package installer)
- Internet connection to access the website for scraping.

## Installation

Follow the steps below to set up the project on your Windows machine.

### 1. Clone the repository

First, clone my repository from GitHub:

```bash
git clone https://github.com/ahmadh-git/book.git
cd book

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install the requirements
pip install -r requirements.txt

# To finish or complete your virtual environment
run "deactivate"

# Output
Books will be output in the data file folder and images will be stored in the /data/img directory
