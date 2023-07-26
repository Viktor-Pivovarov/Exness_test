# Overview

Scripts designed to fetch and record stock quote data for given symbols. It interfaces with the iex cloud API to retrieve live stock data, which it then stores in a local SQLite database.

The application also includes features for exporting the data into CSV files, as well as generating time-series plots for visual data analysis.


1. script_input.py and unittest_stock_quote.py are for points 1-8 of the assignment

2. script_worker.py, build-docker.sh, requirenments.txt and docker-compose.yaml are for point 9 of the assignment

3. exe foulder is for point 10 of the assignment

## Requirements

1. python3
2. matplotlib
3. pandas
4. requests
5. pyinstaller
6. docker
7. docker-compose

## Run scripts

1. script_input.py
Check API Token and then run script and enter in input nessesary symbol or symbols. 
The script will return data in a CSV file and a graph of selected symbols.

```bash
python3 script_input.py
```

2. script_worker.py
Check API Token and then set environmental variables:
   - SYMBOLS= enter your symbol(s)
   - EXPORT_CSV=true\false
   - EXPORT_PLOT=true\false

The script will run in a loop until it is turned off. The execution time can be changed in line 145 of the code.

```bash
SYMBOLS="AA,AAA" DRAW_GRAPH=true EXPORT_CSV=true python3 script_worker.py
```

## Build docker image

1. Set execution time of script.

2. Run
```bash
./build_docker.sh
```
3. Set variables in docker-compose.yaml

4. Run
```bash
docker-compose up
```

## Build exe file

1. Package the script and all its dependencies
```bash
pyinstaller --onefile script_worker.py
```

2. Set variables and run file
```bash
set SYMBOLS=AA,AAA
set DRAW_GRAPH=true
set EXPORT_CSV=true
script_worker.exe
```