class fragplotter():
    
    def __init__(self, ):
        
        self.args = get_args()
        self.fragment_analyzer_x = []
        self.fragment_analyzer_y = []
        self.minion_csv_x = []
        self.minion_csv_y = []
        self.minion_fq_x = []
        self.minion_fq_y = []

    def run(self, ):
        
        self.read_infiles()
        self.make_histograms()
        self.nomarlize()
        self.plot()
    
    def read_infiles(self, ):
        
        import os
        import sys
        
        if not self.args.minion_csv and not self.args.minion_fq:
            sys.stderr.write('Error: you have to supply at least one minion infile, use the --help option for more info.\n')
            sys.exit()
        
        if self.args.fragge_csv and os.path.isfile(self.args.fragge_csv):
            self.read_fragge_csv()
        else:
            sys.stderr.write('WARNING: the fragment analyser csv does not excist ('+str(self.args.fragge_csv)+') will not plot any data from this file.\n')
            
        if self.args.minion_csv and os.path.isfile(self.args.minion_csv):
            self.read_minion_csv()
        else:
            sys.stderr.write('WARNING: the minIon csv does not excist ('+str(self.args.minion_csv)+') will not plot any data from this file.\n')
            
        if self.args.minion_fq and os.path.isfile(self.args.minion_fq):
            self.read_minion_fq()
        else:
            sys.stderr.write('WARNING: the minIon fastq does not excist ('+str(self.args.minion_fq)+') will not plot any data from this file.\n')

        
    def read_fragge_csv(self,):
        assert self.args.fragge_csv.split('.')[-1] == 'csv', 'Error: the fragment analyser csv does not have the filename extension ".csv"'
        file_handle = open(self.args.fragge_csv)
        header = file_handle.readline().split(',')
        assert header[0] == 'Size (bp)'
        for line in file_handle:
            line = line.rstrip().split(',')
            self.fragment_analyzer_x.append(float(line[0]))
            self.fragment_analyzer_y.append(float(line[1]))
        
    def read_minion_csv(self,):
        assert self.args.minion_csv.split('.')[-1] == 'csv', 'Error: the minIon csv does not have the filename extension ".csv"'
        file_handle = open(self.args.minion_csv)
        header = file_handle.readline().rstrip()
        self.min_ion_values = []
        assert header == 'start_time,exit_status,mean_qscore_template,sequence_length_template,mean_qscore_complement,sequence_length_complement,mean_qscore_2d,sequence_length_2d,run_id'
        for line in file_handle:
            line = line.rstrip().split(',')
            #self.min_ion_values.append((line[3],line[5],line[-2]))
            if line[-2]:self.min_ion_values.append(int(line[-2]))

    def make_histograms(self, ):
        
        hist = {}
        
        for  seq_length in self.min_ion_values:
            try: hist[seq_length] += 1
            except KeyError: hist[seq_length] = 1
            
        import operator        
        last_length = 0
        for seq_length, count in sorted(hist.iteritems(),key=operator.itemgetter(0)):
            if seq_length != last_length+1:
                for i in xrange(last_length,seq_length,1):
                    self.minion_csv_x.append(i)
                    self.minion_csv_y.append(0)
            self.minion_csv_x.append(seq_length)
            self.minion_csv_y.append(count)
            last_length = seq_length
    
    def nomarlize(self, ):
        tmp_total = float(sum(self.fragment_analyzer_y))
        self.fragment_analyzer_y = [value/tmp_total for value in self.fragment_analyzer_y]
        tmp_total = float(sum(self.minion_csv_y))
        self.min_ion_y = [value/tmp_total for value in self.minion_csv_y]
    
    def plot(self, ):
        
        import matplotlib.pyplot as plt
        fig, ax_mi = plt.subplots()
        ax_fa = ax_mi.twinx()
        line, = ax_mi.plot(self.minion_csv_x, self.minion_csv_y, color='r')
        line, = ax_mi.plot(self.minion_fq_x, self.minion_fq_y, color='g')
        line, = ax_fa.plot(self.fragment_analyzer_x, self.fragment_analyzer_y, color='b')
        ax_mi.set_xlabel('Fragemnt size Base(Pair)s')
        ax_fa.set_ylabel('Frequenzy Frag.Analyzer')
        ax_mi.set_ylabel('Frequenzy MinIon')
        plt.title('Fragment size frequencies')
        if self.args.range_start or self.args.range_end:
            start = 0
            end = max(self.minion_csv_x+self.minion_fq_x+self.fragment_analyzer_x)
            if self.args.range_start: start = self.args.range_start
            if self.args.range_end: end = self.args.range_end
            ax_mi.set_xlim(start, end)
            ax_fa.set_xlim(start, end)
        #plt.show()
        plt.savefig(self.args.out_file)
        
def get_args():
    import sys
    import argparse
    if len( sys.argv) ==1: sys.argv.append('--help')
    parser = argparse.ArgumentParser(description='Note that you must supply either one "--minion_csv" or one "--minion_fq" as well as a "--out_file" for the program to work!')
    parser.add_argument('-csv',"--minion_csv", help="minion csv filename",metavar='<file>')
    parser.add_argument('-fq',"--minion_fq", help="minion fastq filename",metavar='<file>')
    parser.add_argument('-fcsv',"--fragge_csv", help="fragmentanalyzer csv",metavar='<file>')
    parser.add_argument('-o',"--out_file", help="output .pdf or .png filename",required=True,metavar='<file>')
    parser.add_argument('-s',"--range_start",type=int, help="start of the range to plot in the pdf",metavar='<int>')
    parser.add_argument('-e',"--range_end",type=int, help="end of the range to plot in the pdf",metavar='<int>')
    args = parser.parse_args()
    return args