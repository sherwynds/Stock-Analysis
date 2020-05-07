# Stock-Analysis
A simple stock analysis framework built in Python

![image](https://user-images.githubusercontent.com/4008778/81018199-e45ed180-8e18-11ea-870b-34d3b5e68657.png)

## Installation Instructions:
Note: This has been tested on Windows 10 with Python 3.8
1. Clone/download the repository to the local disk
2. Edit constants.py to include your TIINGO API key
3. Install the dependencies using `pip install`
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


