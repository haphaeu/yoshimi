import pandas
import numpy as np

class ResultsLoader():
    def __init__(self):
        self.isAvailable = False

    def load(self, fname):
        self.df = pandas.read_table(fname, sep='\t')
        errors = self.check_data()
        if errors:
            self.isAvailable = False
            print('Error checking input data')
            for err in errors:
                print(err)
            return errors
        self.calc_cdf()
        self.isAvailable = True
        return False

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

    @staticmethod
    def fit(x, y):
        """Linear fit using least squares method."""
        slope, cte = np.polyfit(x, y, deg=1)
        x1, x2 = min(x), max(x)
        y1, y2 = cte + x1*slope, cte + x2*slope
        # print('fit data: ', slope, cte, x1, x2, y1, y2)
        return (x1, x2), (y1, y2)

    def check_data(self):
        """
        Perform some sanity checks, like number of seeds, check that
        all sea states have that number of seeds.
        output a message window in case cases are missing.
        """
        err = []
        
        # check number of columns
        ncols = len(self.df.columns)
        if ncols < 4:
            err.append('Incorrect number of columns.')
            err.append('   Expected at least 4 columns, got %d' % ncols)
        
        # check first three column
        try:
            if not all(self.df.columns[:3] == ['WaveHs', 'WaveTp', 'WaveDirection']):
                err.append("Incorrect headers in file.")
                err.append("   Expected 'WaveHs', 'WaveTp' and 'WaveDirection', got ", list(self.df.columns[:3]))
        except ValueError:
            err.append('Incorrect file headers.')
        
        # check for numeric entries only
        if not all(self.df.applymap(np.isreal)):
            err.append("Found non-numeric data in table.")
        
        # check if all sea states have the same number of seeds
        try:
            out = self.check_seeds()
            if out:
                err.append(out)
        except:
            err.append("Error getting number of seeds.")

        return err

    def check_seeds(self):
        seeds = len(self.df[(self.df.WaveHs == self.df.WaveHs[0]) & 
                            (self.df.WaveTp == self.df.WaveTp[0]) & 
                            (self.df.WaveDirection == self.df.WaveDirection[0])])
        for hs in self.get_hs_list():
            hs = float(hs)
            for tp in self.get_tp_list([hs]):
                tp = float(tp)
                for wd in self.get_wd_list():
                    wd = float(wd)
                    iseeds = len(self.df[(self.df.WaveHs == hs) & 
                                (self.df.WaveTp == tp) & 
                                (self.df.WaveDirection == wd)])
                    if not iseeds == seeds:
                        return ["Found sea states with different number of seeds."]
        return []

    # Deprecated
    def __fit__(self):
        """Linear fit of all sea states in the data.
        Fits are saved in an instance dataframe
        DEPRECATED - fits are done by request, see static method fit().
        """
        idx = ['WaveHs', 'WaveTp', 'WaveDirection']
        vars = self.get_vars()
        cols = ['slope', 'constant', 'x1', 'x2']
        mcols = pandas.MultiIndex.from_product([vars, cols])
        bigdata=[]
        for hs in self.get_hs_list():
            for tp in self.get_tp_list([hs]):
                for wd in self.get_wd_list():
                    hs, tp, wd = float(hs), float(tp), float(wd)
                    data = [hs, tp, wd]
                    for var in vars:
                        sample = self.get_sample(var, hs, tp, wd)
                        coefs = np.polyfit(sample, self.llcdf, 1)
                        data.extend(coefs)
                        data.append(min(sample))
                        data.append(max(sample))
                    bigdata.append(data)
        df = pandas.DataFrame(data=bigdata)
        df.columns = [*idx, *df.columns[3:]]
        df = df.set_index(idx)
        df.columns = mcols
        self.df_fit = df.reset_index()