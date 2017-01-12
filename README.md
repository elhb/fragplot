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
                [-s <int>] [-e <int>] [-b <int>]

NOTE:
You must supply either one "--minion_csv" or one "--minion_fq" as well as a "--out_file" for the program to work!
ALSO:
Only the sequences in the fastq that has the term "Basecall_2D_2d" in the header will be used.

optional arguments:
  -h, --help            show this help message and exit
  -csv <file>, --minion_csv <file>
                        minion csv filename
  -fq <file>, --minion_fq <file>
                        minion fastq filename
  -fcsv <file>, --fragge_csv <file>
                        fragmentanalyzer csv
  -o <file>, --out_file <file>
                        output .pdf or .png filename
  -s <int>, --range_start <int>
                        start of the range to plot in the pdf
  -e <int>, --range_end <int>
                        end of the range to plot in the pdf
  -b <int>, --bin_size <int>
                        size in base pairs for the bins in the minion
                        histograms, each point in the line represents the
                        middle point of the bin, ie if bin size is 10 (the
                        default value) the frequenzy off all reads with length
                        0-10 vill be plotted as y-value for x=5, likewise if
                        bin_size is 100, freq of reads with lengths 0-100bp
                        will get x=50.
```

## To run on the included Example data:
```
    fragplot --minion_csv example_data/minion.csv --fragge_csv=example_data/electropherogram.csv -o example_data/example_output_2.png -s 100 -e 10000
```
