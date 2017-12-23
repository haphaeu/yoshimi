import math
import pandas
import numpy as np
from scipy import stats as ss
from bisect import bisect_left


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
                err.append("   Expected 'WaveHs', 'WaveTp' and 'WaveDirection', got {}".format(list(self.df.columns[:3])))
        except ValueError:
            err.append('Incorrect file headers.')
        
        # check for numeric entries only
        if not self.df.applymap(np.isreal).all().all():
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
                        return "Found sea states with different number of seeds."
        return []

    @staticmethod
    def fit(x, y, method, tail):
        """Linear fit using MLE, ME or least squares method."""
        if method == 'LstSqr':
            slope, cte = np.polyfit(x, y, deg=1)
            x1, x2 = min(x), max(x)
            y1, y2 = cte + x1*slope, cte + x2*slope
            return (x1, x2), (y1, y2)

        if tail == 'upper':
            gumbel = ss.gumbel_r
        else:
            gumbel = ss.gumbel_l
        
        if method == 'MLE':
            params = gumbel.fit(x)
        else:
            params = gumbel._fitstart(x)
        
        x = x.min(), x.max()
        if tail == 'upper':
            y = -np.log(-gumbel(*params).logcdf(x)).transpose()
        else:
            y = -np.log(-gumbel(*params).logsf(x)).transpose()

        return x, y
        # print('fit data: ', slope, cte, x1, x2, y1, y2)

    # #############################################################################################
    # #############################################################################################
    # These functions below are borrowed from Statistics/confidence_interval_bootstrap.py

    @staticmethod
    def confidence_interval(sample, fstats=np.sort, ci=0.95, repeat=1000, relative=True,
                            random_seed = 12343, fargs=[], fkwargs={}):
        """Returns the lower and upper confidence intervals of a statistic of a sample. The intervals
        can be relative or absolute, i.e:

            absolute ci = sample statistics + relative ci

        The statistics to be calculated for the sample is passed as a function that takes the sample
        as first argument. Additional positional arguments can be passed using fargs and fkwargs.

        The returned array has shape (2, len(fstats(sample))).

        The interval is calculated for a 100*ci % confidence level.

        Bootstrapping technique is used for the calculation of the intervals, using a sorted resampling
        with replacement.

        Arguments:
            sample      : array with the sample values
            fstats      : function used to calculate sample statistics
            ci          : confidence level of the interval
            repeat      : bootstrap size
            relative    : set to True for relative intervals, False for absolute intervals, i.e.,
                          absolute ci = sample statistics + relative ci
                          relative intervals can be seen as tolerances to sample statistics, while
                          absolute intervals are lower and upper bounds for the statistics.
            fargs       : optional. list with additional positional arguments for fstats.
            fkwargs     : optional. dictionary with additional key word arguments for fstats.
        """
        
        # To make this work within a class:
        resample = ResultsLoader.resample

        if not isinstance(sample, np.ndarray):
                sample = np.array(sample, dtype='float64')

        assert callable(fstats), "Error: fstats must be a function."

        m = fstats(sample)
        m_star = np.zeros(shape=(repeat, 1 if not hasattr(m, '__len__') else len(m)))
        np.random.seed(random_seed)
        for i in range(repeat):
            m_star[i] = fstats(resample(sample))  # re-sampling with replacement
        delta_star = m_star - m
        delta_star.sort(axis=0)
        ci_idx = np.array([math.floor((1.0 - ci)/2*repeat), math.ceil(repeat - (1.0 - ci)/2*repeat)])
        return delta_star[ci_idx] + (0 if relative else m)

    @staticmethod
    def resample(sample, size=False, replacement=True):
        """Re-sample of sample.
        size        : size of the output re-sampled array. Set to False to use size of input sample.
        replacement : if True, the items are put back in the sample after each draw, i.e, the re-
                      sampled output array might have repeated items from the input sample.
                      if False, drawn items are discarded, i.e, the output array will not repeat items
                      from the input sample.
                      Bootstrap technique must use replacement.

        This technique uses random resampling. A random seed is set to make sure that calls of this
        function with same arguments will return the same intervals. To change the random seed, change
        the global parameter _random_seed and re-set np.random.seed(seed). Alternatively to have
        ramdom outputs, set np.random.seed(None).

        """
        sample_size = len(sample)
        if not size:
            size = sample_size
        if replacement:
            return sample[np.random.randint(0, sample_size, size)]
        else:
            assert size <= sample_size, "Re-sampling without replacement - size must be <= sample_size"
            idx = np.arange(sample_size)
            np.random.shuffle(idx)
            return sample[idx[:size]]

    @staticmethod
    def fit_ci_gumbel(sample, ci=0.95, repeat=100, tail='upper', fit='MLE'):
        """Returns the best fit and confidence intervals for sample assuming Gumbel distribution.
        Returns are ready to plot using plot(*fit_points(sample))
        """
        
        # To make this work within a class
        confidence_interval = ResultsLoader.confidence_interval

        sz = len(sample)

        if tail == 'upper':
            gumbel = ss.gumbel_r
        else:
            gumbel = ss.gumbel_l
        if fit == 'ME':
            gumbel.ft = gumbel._fitstart
        else:
            gumbel.ft = gumbel.fit

        params_ci = confidence_interval(sample, gumbel.ft, ci=ci, repeat=repeat, relative=False)

        x = sample.min(), sample.max()
        if tail == 'upper':
            y = np.array([-np.log(-gumbel(*p).logcdf(x)) for p in params_ci]).transpose()
        else:
            # For a negative slope, we need to swap around the scale parameters
            _ = params_ci[0, 1]
            params_ci[0, 1] = params_ci[1, 1]
            params_ci[1, 1] = _
            y = np.array([-np.log(-gumbel(*p).logsf(x)) for p in params_ci]).transpose()
        return x, y

    # These functions above are borrowed from Statistics/confidence_interval_bootstrap.py
    # #############################################################################################
    # #############################################################################################

    @staticmethod
    def closest_index(mylist, number):
        """
        Assumes mylist is sorted. Returns the index of the closest value to number.

        If two numbers are equally close, return the largest index.

        This is a slight change of:
        https://stackoverflow.com/a/12141511/5069105
        """
        pos = bisect_left(mylist, number)
        if pos == 0:
            return 0
        if pos == len(mylist):
            return len(mylist)-1
        before = mylist[pos - 1]
        after = mylist[pos]
        if after - number <= number - before:
           return pos
        else:
           return pos-1

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