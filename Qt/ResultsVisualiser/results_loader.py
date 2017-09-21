import pandas
import numpy as np

class ResultsLoader():
    def __init__(self):
        self.isAvailable = False

    def load(self, fname):
        self.df = pandas.read_table(fname, sep='\t')
        self.calc_cdf()
        self.isAvailable = True
    
    def get_vars(self):
        return self.df.columns[3:]
        
    def get_hs_list(self):
        hs = list(set(self.df.WaveHs))
        hs.sort()
        return ['%.2f' % x for x in hs]
    
    def get_wd_list(self):
        wd = list(set(self.df.WaveDirection))
        wd.sort()
        return ['%.1f' % x for x in wd]
        
    def get_tp_list(self, hs_list):
        if not hs_list:
            return []
        if isinstance(hs_list[0], str):
            hs_list = [float(x) for x in hs_list]
        tp = set()
        for hs in hs_list:
            tp.update(self.df[self.df.WaveHs == hs]['WaveTp'])
        tp = list(tp)
        tp.sort()
        return ['%.2f' % x for x in tp]
    
    def get_sample(self, var, hs, tp, wd):
        return self.df[(self.df.WaveHs == hs) & (self.df.WaveTp == tp) & 
                       (self.df.WaveDirection == wd)][var].sort_values()
    
    def calc_cdf(self):
        seeds = len(self.df[(self.df.WaveHs == self.df.WaveHs[0]) & 
                            (self.df.WaveTp == self.df.WaveTp[0]) & 
                            (self.df.WaveDirection == self.df.WaveDirection[0])])
        self.seeds = seeds
        self.cdf = np.linspace(0.5/seeds, (seeds-0.5)/seeds, seeds)
        self.llcdf = -np.log(-np.log(self.cdf))

    def check_data(self):
        """TBC
        perform some sanity checks, like number of seeds, check that
        all sea states have that number of seeds.
        output a message window in case cases are missing.
        """