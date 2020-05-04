# Stock-Analysis
A Stock Analysis Framework

## Installation Instructions:
Note: This has been tested on Windows 10 with Python 3.8
1. Clone/download the repository to the local disk
2. Edit constants.py to include your TIINGO API key
3. Use the command line to navigate to the Stock-Analysis folder, and activate the virtual environment with `.\env\Scripts\activate` on Windows
4. Run the script with `python main.py`

## Usage Instructions:
1. Enter a valid stock symbol in the 'Symbol' box, and optionally a valid name in the 'Name' box
2. Enter valid start/end dates (cannot be the same day, end date must be later than start date)
3. Press 'Generate Graph'
4. Use the Matplotlib toolbars to navigate each plot

## Python Dependencies:
* matplotlib
* numpy
* pandas
* pandas-datareader
* pyqt5


