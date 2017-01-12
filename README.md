# fragplot
Python script to plot fragment sizes from two csv files (minIon and fragmentanalyzer).

## To install run:
```
    git clone https://github.com/elhb/fragplot.git
    cd fragplot
    python setup.py install
```

## Usage:
```
usage: fragplot [-h] [-csv <file>] [-fq <file>] [-fcsv <file>] -o <file>
                [-s <int>] [-e <int>]

Note that you must supply either one "--minion_csv" or one "--minion_fq" as
well as a "--out_file" for the program to work!

optional arguments:
  -h, --help            show this help message and exit
  -csv <file>, --minion_csv <file>
                        minion csv filename
  -fq <file>, --minion_fq <file> THE FASTQ FILE STUFF DOES NOT WORK YET DON'T USE THEM!!!!
                        minion fastq filename
  -fcsv <file>, --fragge_csv <file>
                        fragmentanalyzer csv
  -o <file>, --out_file <file>
                        output .pdf or .png filename
  -s <int>, --range_start <int>
                        start of the range to plot in the pdf
  -e <int>, --range_end <int>
                        end of the range to plot in the pdf
```

## To run on the included Example data:
```
    fragplot --minion_csv example_data/minion.csv --fragge_csv=example_data/electropherogram.csv -o example_data/example_output_2.png -s 100 -e 10000
```
