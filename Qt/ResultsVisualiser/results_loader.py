import pandas

class ResultsLoader():
    def __init__(self, fname='results.txt'):
        self.load_results(fname)
    
    def load_results(self, fname):
        self.df = pandas.read_table(fname, sep='\t')
    
    def get_vars(self):
        return self.df.columns[3:]
        
    def get_hs_list(self):
        hs = list(set(self.df['WaveHs']))
        hs.sort()
        return ['%.2f' % x for x in hs]
    
    def get_wd_list(self):
        wd = list(set(self.df['WaveDirection']))
        wd.sort()
        return ['%.1f' % x for x in wd]
        
    def get_tp_list(self, hs_list):
        print(hs_list)
        if not hs_list:
            return []
        if isinstance(hs_list[0], (int, float)):
            hs_list = [float(x) for x in hs_list]
        tp = set()
        for hs in hs_list:
            tp.update(self.df[self.df['WaveHs'] == hs]['WaveTp'])
        tp = list(tp)
        tp.sort()
        return ['%.2f' % x for x in tp]
    
    def get_sample(self, var, hs, tp, wd):
        return df[(df.WaveHs == hs) & (df.WaveTp == tp) & 
                  (df.WaveDirection == wd)][var].sort_values()
    
    def check_data(self):
        """TBC
        perform some sanity checks, like number of seeds, check that
        all sea states have that number of seeds.
        output a message window in case cases are missing.
        """