class fragplotter():
    
    def __init__(self, ):
        
        self.args = get_args()
        self.fragment_analyzer_x = []
        self.fragment_analyzer_y = []
        self.minion_csv_x = []
        self.minion_csv_y = []
        self.minion_fq_x = []
        self.minion_fq_y = []
        self.minion_csv_values = []
        self.minion_fq_values = []

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

    def read_minion_fq(self,):
        
        import re
        import sys
        assert self.args.minion_fq.split('.')[-1] in ['fq','fastq'], 'Error: the fragment analyser csv does not have the filename extension ".csv"'
        p = Progress( bufcount(self.args.minion_fq)/(4*3), printint=1 )
        file_handle = open(self.args.minion_fq)
        while True:
            try:
                header = file_handle.readline()
                sequence = file_handle.readline()
                plus = file_handle.readline()
                qual = file_handle.readline()
            except EOFError:
                print 'end of file'
                break
            if re.search('Basecall_2D_2d',header):
                self.minion_fq_values.append(len(sequence))
                p.update()
            if header == '': break
        
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
        assert header == 'start_time,exit_status,mean_qscore_template,sequence_length_template,mean_qscore_complement,sequence_length_complement,mean_qscore_2d,sequence_length_2d,run_id'
        for line in file_handle:
            line = line.rstrip().split(',')
            #self.minion_csv_values.append((line[3],line[5],line[-2]))
            if line[-2]:self.minion_csv_values.append(int(line[-2]))

    def make_histograms(self, ):
        
        import operator
        
        for in_list,x_list,y_list in [(self.minion_csv_values,self.minion_csv_x,self.minion_csv_y),(self.minion_fq_values,self.minion_fq_x,self.minion_fq_y)]:
            
            hist = {}
            for  seq_length in in_list:
                try: hist[seq_length] += 1
                except KeyError: hist[seq_length] = 1
            last_length = 0
            for seq_length, count in sorted(hist.iteritems(),key=operator.itemgetter(0)):
                if seq_length != last_length+1:
                    for i in xrange(last_length,seq_length,1):
                        x_list.append(i)
                        y_list.append(0)
                x_list.append(seq_length)
                y_list.append(count)
                last_length = seq_length
    
    def nomarlize(self, ):
        for y_value_list in [self.fragment_analyzer_y,self.minion_csv_y,self.minion_csv_y]:
            tmp_total = float(sum(y_value_list))
            y_value_list = [value/tmp_total for value in y_value_list]
        
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

class Progress():
    """ a progress meter
    """
    
    import sys

    def __init__(self,total, verb='full', logfile=sys.stderr, unit='reads' ,mem=False, printint=0, new_line=False):
        import time
        self.total = total
        self.current = 0
        self.type = verb
        self.logfile = logfile
        self.ltime = time.time()
        self.lcurrent = self.current
        self.lpercentage = 0
        if verb == 'full': self.printint = 5
        elif verb == 'minimal':self.printint = 5
        self.unit = unit
        self.mem = mem
        if printint: self.printint = printint
        self.new_line=new_line

    def __enter__(self):
        if self.type == 'minimal': self.logfile.write('0%                 50%                 100%\n')
        #                                              ....................................................................................

    def update(self):
        import time
        self.current += 1
        self.percentage = int(round(100*float(self.current)/self.total))
        if self.percentage % self.printint == 0 and self.percentage != self.lpercentage:
            self.stf=int(round((self.total-self.current)/((self.current-self.lcurrent)/(time.time()-self.ltime))))
            if self.type == 'full' and self.logfile: self.logfile.write(
                '#Progress => '+str(self.percentage)+'%, '+
                str( round((self.current-self.lcurrent)/(time.time()-self.ltime),2) )+' '+self.unit+'/second, '+
                time.strftime("%A, %d %b %Y %H:%M:%S",time.localtime())+
                ', left: '+str(self.stf/60/60)+'h '+str(self.stf/60%60)+'min '+str(self.stf%60)+'s')
            if self.mem:
                import resource
                total_memory_used = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss + resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
                this_process_memory_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                if total_memory_used/1024/1024 > 1024: self.logfile.write(', using '+str(round(float(total_memory_used)/1024/1024/1024,2))+' ('+str(round(float(this_process_memory_used)/1024/1024/1024,2))+') GB.')
                elif total_memory_used/1024 > 1024:    self.logfile.write(', using '+str(round(float(total_memory_used)/1024/1024,2))+' ('+str(round(float(this_process_memory_used)/1024/1024,2))+') MB.')
                else:                                  self.logfile.write(', using '+str(round(float(total_memory_used)/1024,2))+' ('+str(round(float(this_process_memory_used)/1024,2))+') KB.')
            if self.new_line: self.logfile.write('\n')
            else: self.logfile.write('\r')
            if self.type == 'minimal': self.logfile.write('..')
            self.ltime = time.time()
            self.lcurrent = self.current
            self.lpercentage = self.percentage

    def __exit__(self, *args):
        if self.logfile: self.logfile.write('\n')

def bufcount(filename):
    """ returns the number of lines in a file
    """
    
    #
    # open the file and check if it's compressed or not
    #
    import gzip
    if filename.split('.')[-1] in ['gz','gzip']: f = gzip.open(filename)
    else: f = open(filename)
    
    #
    # set initial values
    #
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read # loop optimization
    
    #
    # do the actual counting and return the number of new line characters found
    #
    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
        f.close
    return lines