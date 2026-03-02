# Selenium Formula Bot

An automated WhatsApp messaging bot built with Python and Selenium for the **Formula UTFPR** racing team. The bot reads a list of venues (farms/chácaras) scraped from Google Maps and sends personalized WhatsApp messages to each one, asking about accommodation availability for the team during the Formula SAE competition week.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [CSV File Format](#csv-file-format)
- [Usage](#usage)
- [Project Structure](#project-structure)

---

## Overview

The Formula UTFPR team needs accommodation for approximately **40 people** for one week in **Piracicaba, SP** during the Formula SAE competition (July 27 – August 3, 2025). This bot automates the tedious process of reaching out to dozens of local venues by:

1. Reading venue names and phone numbers from a CSV file.
2. Opening each contact's WhatsApp chat via `wa.me` links.
3. Automatically clicking through the WhatsApp Web prompts.
4. Waiting a randomised delay between messages to avoid spam detection.

---

## How It Works

```
mapsscraper.csv  →  main.py  →  WhatsApp Web (Edge)  →  Messages sent
```

1. **Load data** – `pandas` reads `mapsscraper.csv` and extracts the `Nome` (venue name) and `Telefone` (phone number) columns.
2. **Launch browser** – Selenium starts Microsoft Edge using the bundled `msedgedriver.exe`.
3. **Log in to WhatsApp Web** – The script navigates to `https://web.whatsapp.com/` and pauses so you can scan the QR code.
4. **Send messages** – For each row in the CSV the bot:
   - Builds a personalised message including the venue name and competition dates.
   - Opens `https://wa.me/<phone>?text=<message>`.
   - Clicks **"Iniciar conversa"** and then **"Usar o WhatsApp Web"** to open the pre-filled chat window.
   - Logs success or any errors to the console.
   - Waits a random delay of **10–20 seconds** before moving to the next contact.
5. **Finish** – The browser is closed after all contacts have been processed.

---

## Prerequisites

| Requirement | Version / Notes |
|---|---|
| Python | 3.8 or higher |
| Microsoft Edge | Must match the `msedgedriver.exe` version |
| Microsoft Edge WebDriver | Bundled as `msedgedriver.exe` – update if your Edge version differs |
| A WhatsApp account | Required to log in to WhatsApp Web |

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Harveker/Selenium-Formula-Bot.git
   cd Selenium-Formula-Bot
   ```

2. **Install Python dependencies**
   ```bash
   pip install pandas selenium
   ```

3. **Verify the Edge WebDriver**

   The repository includes `msedgedriver.exe` for Windows. Confirm that its version matches your installed Microsoft Edge version by running:
   ```bash
   msedgedriver.exe --version
   ```
   If they don't match, download the correct driver from [https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and replace the existing file.

---

## Configuration

Open `main.py` and update the two path constants near the top of the file to match your local environment:

```python
# Path to the CSV file containing venue data
google_drive_csv_url = "D:/Repositorio/python/Selenium-Formula-Bot/mapsscraper.csv"

# Path to the Edge WebDriver executable
edge_driver_path = "D:/Repositorio/python/Selenium-Formula-Bot/msedgedriver.exe"
```

Replace these with the **absolute paths** on your machine, for example:

```python
google_drive_csv_url = r"C:\Users\YourName\Selenium-Formula-Bot\mapsscraper.csv"
edge_driver_path     = r"C:\Users\YourName\Selenium-Formula-Bot\msedgedriver.exe"
```

---

## CSV File Format

The bot reads `mapsscraper.csv`, which was scraped from Google Maps. The two columns used by the script are:

| Column | Description | Example |
|---|---|---|
| `Nome` | Name of the venue | `Chácara Montreal Festas Piracicaba` |
| `Telefone` | Phone number with country code (no `+`) | `19997771370` |

Rows where `Telefone` is empty or `NaN` are automatically skipped with a log message.

The CSV may also contain other columns (address, rating, coordinates, etc.) that are ignored by the bot but can be useful for manual reference.

---

## Usage

1. **Run the script**
   ```bash
   python main.py
   ```

2. **Scan the QR code** – A Microsoft Edge window will open at `https://web.whatsapp.com/`. Scan the QR code with your phone to log in. The script will continue automatically once the page is loaded.

3. **Monitor the console** – Progress and any errors are printed to stdout:
   ```
   Mensagem enviada para Chácara Montreal Festas Piracicaba (19997771370)
   Aguardando 14 segundos antes de enviar a próxima mensagem...
   Número inválido ou ausente para Chácara Bella Dias. Pulando...
   ```

4. **Wait for completion** – The bot processes all rows and then closes the browser automatically.

> **Note:** Keep the browser window visible and do not interact with it while the bot is running.

---

## Project Structure

```
Selenium-Formula-Bot/
├── main.py            # Main bot script
├── mapsscraper.csv    # Venue data scraped from Google Maps
├── msedgedriver.exe   # Microsoft Edge WebDriver (Windows)
└── README.md          # This file
```
