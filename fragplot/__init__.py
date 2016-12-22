class fragplotter():
    
    def __init__(self, fragment_analyzer_csv, min_ion_csv):
        
        self.fragment_analyzer_csv = fragment_analyzer_csv
        self.min_ion_csv = min_ion_csv
    
    def run(self, ):
        
        self.read_csvs()
        self.make_histogram()
        self.nomarlize()
        self.plot()
    
    def read_csvs(self, ):
        
        import os
        
        assert os.path.isfile(self.fragment_analyzer_csv), 'Error: the fragment analyser csv does not excist'
        assert os.path.isfile(self.min_ion_csv), 'Error: the minIon csv does not excist'
        
        assert self.fragment_analyzer_csv.split('.')[-1] == 'csv', 'Error: the fragment analyser csv does not have the filename extension ".csv"'
        assert self.min_ion_csv.split('.')[-1] == 'csv', 'Error: the minIon csv does not have the filename extension ".csv"'
        
        file_handle = open(self.fragment_analyzer_csv)
        self.fragment_analyzer_x = []
        self.fragment_analyzer_y = []
        header = file_handle.readline().split(',')
        assert header[0] == 'Size (bp)'
        for line in file_handle:
            line = line.rstrip().split(',')
            self.fragment_analyzer_x.append(float(line[0]))
            self.fragment_analyzer_y.append(float(line[1]))

        file_handle = open(self.min_ion_csv)
        header = file_handle.readline().rstrip()
        self.min_ion_values = []
        assert header == 'start_time,exit_status,mean_qscore_template,sequence_length_template,mean_qscore_complement,sequence_length_complement,mean_qscore_2d,sequence_length_2d,run_id'
        for line in file_handle:
            line = line.rstrip().split(',')
            #self.min_ion_values.append((line[3],line[5],line[-2]))
            if line[-2]:self.min_ion_values.append(int(line[-2]))

    def make_histogram(self, ):
        
        hist = {}
        self.min_ion_x = []
        self.min_ion_y = []
        
        for  seq_length in self.min_ion_values:
            try: hist[seq_length] += 1
            except KeyError: hist[seq_length] = 1
            
        import operator        
        last_length = 0
        for seq_length, count in sorted(hist.iteritems(),key=operator.itemgetter(0)):
            if seq_length != last_length+1:
                for i in xrange(last_length,seq_length,1):
                    self.min_ion_x.append(i)
                    self.min_ion_y.append(0)
            self.min_ion_x.append(seq_length)
            self.min_ion_y.append(count)
            last_length = seq_length
    
    def nomarlize(self, ):
        tmp_total = float(sum(self.fragment_analyzer_y))
        self.fragment_analyzer_y = [value/tmp_total for value in self.fragment_analyzer_y]
        tmp_total = float(sum(self.min_ion_y))
        self.min_ion_y = [value/tmp_total for value in self.min_ion_y]
    
    def plot(self, ):
        
        import matplotlib.pyplot as plt
        fig, ax_mi = plt.subplots()
        ax_fa = ax_mi.twinx()
        line, = ax_mi.plot(self.min_ion_x, self.min_ion_y, color='r')
        line, = ax_fa.plot(self.fragment_analyzer_x, self.fragment_analyzer_y, color='b')
        ax_mi.set_xlabel('Fragemnt size Base(Pair)s')
        ax_fa.set_ylabel('Frequenzy Frag.Analyzer')
        ax_mi.set_ylabel('Frequenzy MinIon')
        plt.title('Fragment size frequencies')
        plt.show()