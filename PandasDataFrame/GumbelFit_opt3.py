# -*- coding: utf-8 -*-
"""
To be used in conjunction with:
    NR099910-004-10006 - Repeated lowering, OrcaFlex Gumbel Script
    NR099910-004-10001 - Lifting Analysis Methodology - Probabilistic Approach
===============================================================================================
Version 13
Corrected bug in WriteResults():
Exception: Excel worksheet name 'pennant line Max Effective Tension 3.50m' must be <= 31 chars.
14.03.2016
===============================================================================================
Version 12
Small change: confidence_Level passed as an argument to plotProbability().
rarossi, 29.02.2016
===============================================================================================
Version 11
Performance optimisation in gumbelFit() and summaryDataFrame().
Minor change required in createResultsPanel().
Basically using pandas.stuff by individual indexing is slow.
It is better to move things around in bunches and assigning by slicing.
Test case: > 4x faster

%timeit runfile('GumbelFit.py')
1 loops, best of 3: 20.2 s per loop

%timeit runfile('GumbelFit_opt.py')
1 loops, best of 3: 4.47 s per loop

by rarossi, 05.01.2016
===============================================================================================
Version 10
Changes:
- Both moment estimators and MLE distribution parameters are used, and results for both presented
  in Excel files and plot.
- Revised the Gumbel fit plot. Plots can be found in a separate subfolder. The different confidence
  levels analysed are shown in the plot, together with estimates
- For minimum samples containing zero values a warning is now given, and a Gumbel fitting is not
  performed. Instead, the sample empirical value for the considered confidence level is reported.
- Results files updated.

by rlohne, 12.11.2015
===============================================================================================
Version 9
Changes:
- Major change in format of output spreadsheets:
    Statistical results: name identifier replaced by 3 columns: Hs, Tp and WaveDir
    Summary of predicted min max: idem as above. Also added one column at the start with the
    confidence level and merged all confidence levels tabs into the same sheet. This is to have all
    results in the same page. This file also saved as a text file for convenience
- Roll back to allowing white spaces in names, since this is unavoidable due to Orcaflex loads
  names, e.g, 'Bend Moment'. The error was caused due to empty column in the end of results file
  resultant from a small bug in postCalcActions.py. postCalcActions.py corrected.
- Removal ambiguous flag UseMLE. Only UseMomentEstimators is kept. If set to False then MLE is used
- Add support for Abs variable, fitting then like Max variables.
- Fix identation keeping 4-spaces throughout the code and max line width of 100 characters.

by rarossi, 25.08.2015
===============================================================================================
Version 8

Changes from previous version:
Some cleanup in code
Restructured plotting
Changed the way result file is read. Previous version required that the Result txt-file be opened
and saved using Excel, as an error occured if not. Now this is fixed, but requires that object
names do not have any spaces in them. Use underscores etc.

Some small changes to make it Python 3 compatible. It has also been tested and found
working on Python 2.7.
===============================================================================================

@author: rlohne


"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as ss
import os
# from time import time


def readResultFile(InputFile):
    """Read input file, and return data frame with results, together with number of columns"""
    df = pd.read_table(InputFile)
    sample = pd.DataFrame(df)
    numRowsSample = len(sample)
    numColsSample = len(sample.columns)
    return sample, numRowsSample, numColsSample


def createResultsPanel(numRows, numCols, seedNo, confidence_Level, sample):
    """"Create empty data panel for results (matrix)"""
    ind = ['none']*(10+3*len(confidence_Level))
    ind[0:9] = 'Hs', 'Tp', 'WaveDir', 'StDev', 'Mean', 'Max', 'Min', 'beta ME', 'mu ME', 'beta MLE'
    ind[10] = 'mu MLE'
    count = 0
    for i in range(len(confidence_Level)):
        count = i + 11
        a = str(confidence_Level[i])
        ind[count] = 'g ME (' + a + ')'
    for i in range(len(confidence_Level)):
        count = i + 11 + len(confidence_Level)
        a = str(confidence_Level[i])
        ind[count] = 'g MLE(' + a + ')'
    for i in range(len(confidence_Level)):
        count = i + 11 + 2*len(confidence_Level)
        a = str(confidence_Level[i])
        ind[count] = 'sample (' + a + ')'
    seaStates = numRows/seedNo
    colnames = [_ for _ in range(int(seaStates))]
    # Create a panel that holds all data frames
    name = ['none']*(len(sample.columns)-3)
    for i in range(len(sample.columns)-3):
        name[i] = sample.columns[i+3]
    results = pd.Panel(items=name, major_axis=colnames, minor_axis=ind, dtype='O')

    #
    # Sketch to start thinking about converting this Panel into a MultiIndex'd DataFrame
    # First try to make the result as similar as possible to the Panel.
    # Alternativelly, the index could be replaced by the sea state tuple (Hs, Tp, WaveDir), but
    # doing so would mean a lot more work here...
    #
    mindex = pd.MultiIndex.from_product([name, ind], names=['loads', 'params'])
    res_df = pd.DataFrame(np.zeros(shape=(len(colnames), len(mindex))),
                          index=colnames, columns=mindex)
    #
    # Convertions:
    #
    # Using Panel                          Using DataFrame
    # results.major_axis              == res_df.index
    #                                    mindex = res_df.columns
    # results.minor_axis              == mindex.levels[1]  # !!!sorting order not kept!!! not used
    # results.items                   == mindex.levels[0]
    # results.iloc[row, column, :]    == res_df.iloc[column][mindex.levels[0][row]]
    # results.iloc[row, column]['Hs'] == res_df.iloc[column][mindex.levels[0][row]]['Hs']

    return res_df  # , colnames


def gumbelFit(confidence_Level, sample, results, seedNo, colnames):
    """Fill in results, Calculate statistics"""
    evalv = ['none']*(seedNo)
    # Define Euler constant used for Gumbel statistics
    gamma = 0.5772  # Euler constant
    noCL = len(confidence_Level)
    for row in range(len(sample.columns)-3):
        c = 0
        tmp_data = [0]*(11+3*noCL)  # need to update this 14 here !!!
        for column in range(len(results.index)):
            evalv = sample.iloc[c:c+seedNo, row+3].tolist()
            sortEvalv = sorted(evalv)
            c = (column+1)*seedNo
            tmp_data[0] = sample.iloc[column*seedNo, 0]  # Hs
            tmp_data[1] = sample.iloc[column*seedNo, 1]  # Tp
            tmp_data[2] = sample.iloc[column*seedNo, 2]  # WaveDir
            tmp_data[3] = np.std(evalv)
            tmp_data[4] = np.average(evalv)
            tmp_data[5] = np.max(evalv)
            tmp_data[6] = np.min(evalv)

            # Check if column name contains 'Min'.
            # If true, sample is assumed to be minima, and left skewed distribution is used
            if 'Min' in sample.columns[row+3]:
                muMLE, betaMLE = ss.gumbel_l.fit(evalv)
                betaMoment = tmp_data[3]*(np.sqrt(6))/np.pi
                muMoment = tmp_data[4]+gamma*betaMoment
                tmp_data[7] = betaMoment  # beta ME
                tmp_data[8] = muMoment  # mu ME
                tmp_data[9] = betaMLE  # beta MLE
                tmp_data[10] = muMLE  # mu MLE
                count = 0
                for i in range(len(confidence_Level)):
                    count = i + 11
                    if 0 not in evalv:
                        tmp_data[count] = ss.gumbel_l.ppf((1-confidence_Level[i]),
                                                            muMoment, betaMoment)
                        tmp_data[count+noCL] = ss.gumbel_l.ppf((1-confidence_Level[i]),
                                                                 muMLE, betaMLE)
                    else:
                        tmp_data[count] = 'use sample value'
                        tmp_data[count+noCL] = 'use sample value'
                    sampleIndex = seedNo-(confidence_Level[i])*seedNo
                    enoughSeeds = seedNo >= round(1/(1-confidence_Level[i]), 4)
                    if enoughSeeds:
                        tmp_data[count+2*noCL] = sortEvalv[int(sampleIndex)-1]
                    else:
                        tmp_data[count+2*noCL] = 'need to run more seeds for this confidence level'
            elif 'Max' in sample.columns[row+3] or 'Abs' in sample.columns[row+3]:
                # Else, sample is maxima or max absolute, right skewed distribution is to be used.
                muMLE, betaMLE = ss.gumbel_r.fit(evalv)
                betaMoment = tmp_data[3]*(np.sqrt(6))/np.pi
                muMoment = tmp_data[4]-gamma*betaMoment
                tmp_data[7] = betaMoment  # beta ME
                tmp_data[8] = muMoment  # mu ME
                tmp_data[9] = betaMLE  # beta MLE
                tmp_data[10] = muMLE  # mu MLE
                count = 0
                for i in range(len(confidence_Level)):
                    count = i + 11
                    if 0 not in evalv:
                        tmp_data[count] = ss.gumbel_r.ppf((confidence_Level[i]),
                                                            muMoment, betaMoment)
                        tmp_data[count+noCL] = ss.gumbel_r.ppf((confidence_Level[i]),
                                                                 muMLE, betaMLE)
                    else:
                        tmp_data[count] = 'use sample value'
                        tmp_data[count+noCL] = 'use sample value'
                    sampleIndex = confidence_Level[i]*seedNo
                    enoughSeeds = seedNo >= round(1/(1-confidence_Level[i]), 4)
                    if enoughSeeds:
                        tmp_data[count+2*noCL] = sortEvalv[int(sampleIndex)-1]
                    else:
                        tmp_data[count+2*noCL] = 'need to run more seeds for this confidence level'
            else:
                tmp_data[7] = 'Error! Name must contain Max, Min or Abs.'
            # finally feed tmp_data into the results dataframe
            # this is done for performance, since item assignment by index in pandas
            # panels is VERY slow...
            results.iloc[column][results.columns.levels[0][row]] = tmp_data
    return results


def plotProbability(results, sample, colnames, seedNo, confidence_Level,
                    Objectplot, PlotWd, PlotHs, PlotT):
    """"Make diagnosis plots"""
    if not os.path.isdir('Plots'):
        os.mkdir('Plots')
    evalv = ['none']*(seedNo)
    loads_names = results.columns.levels[0]
    for row in range(len(loads_names)):
        c = 0
        for column in range(len(results.items)):
            evalv = sample.iloc[c:c+seedNo, row+3].tolist()
            sortEvalv = sorted(evalv)
            c = (column+1)*seedNo

            if (loads_names[row] in Objectplot and sample.iloc[c-seedNo, 2] in PlotWd and
                         sample.iloc[c-seedNo, 0] in PlotHs and sample.iloc[c-seedNo, 1] in PlotT):
                fig = plt.figure(num=None, figsize=(12, 12), dpi=240, facecolor='w', edgecolor='k')
                savepng = True
                if savepng: figpng = plt.figure(num=None, figsize=(165/25.4, 90/25.4), dpi=96,
                                                 facecolor='w', edgecolor='k')

                betaME = results.iloc[column][loads_names[row]]['beta ME']
                muME = results.iloc[column][loads_names[row]]['mu ME']

                betaMLE = results.iloc[column][loads_names[row]]['beta MLE']
                muMLE = results.iloc[column][loads_names[row]]['mu MLE']

                # First supblot is histogram of observations and pdf of the fitted distribution
                ax = fig.add_subplot(211)
                n, bins, patches = ax.hist(evalv, 10, histtype='bar',
                                           normed="1", cumulative=False)
                plt.setp(patches, 'facecolor', 'g', 'alpha', 0.5)
                name = sample.columns[row+3]
                ax.set_xlabel(name)
                a = min(evalv)-0.05*min(evalv)
                b = max(evalv)+0.05*min(evalv)
                pdfsample = np.linspace(a, b, 1000)
                if 'Min' in sample.columns[row+3]:
                    yME = ss.gumbel_l.pdf(pdfsample, muME, betaME)  # Create Gumbel PDF
                    yMLE = ss.gumbel_l.pdf(pdfsample, muMLE, betaMLE)
                elif 'Max' in sample.columns[row+3] or 'Abs' in sample.columns[row+3]:
                    yME = ss.gumbel_r.pdf( pdfsample, muME, betaME)
                    yMLE = ss.gumbel_r.pdf( pdfsample, muMLE, betaMLE)
                ax.plot(pdfsample, yME, 'r', pdfsample, yMLE, 'b')
                ax.legend(('Gumbel - ME', 'Gumbel - MLE'), bbox_to_anchor=(0.01, 0.99),
                          loc=2, borderaxespad=0.)

                # Second subplot is the Gumbel plot (log log) showing fitted distribution
                # as a straight line, and observations as scatter points
                ae = fig.add_subplot(212)
                if savepng: aepng = figpng.add_subplot(111)

                sampleRange = np.array(range(1, seedNo+1))
                factor = float(1)/float((seedNo+1))
                sampleCDF = np.multiply(sampleRange, factor)
                if 'Min' in sample.columns[row+3]:
                    loglogValueME = [ss.gumbel_l.ppf(1-conf, muME, betaME)
                                     for conf in confidence_Level]
                    loglogValueMLE = [ss.gumbel_l.ppf(1-conf, muMLE, betaMLE)
                                      for conf in confidence_Level]
                    a = sorted(evalv)
                    a.append(loglogValueME[-1])
                    b = sorted(evalv)
                    b.append(loglogValueMLE[-1])
                    loglog_cdfME = -np.log(-ss.gumbel_l.logsf(a, muME, betaME))
                    loglog_cdfMLE = -np.log(-ss.gumbel_l.logsf(b, muMLE, betaMLE))
                    ae.scatter(sorted(evalv), -np.log(-np.log(1-sampleCDF)),
                               marker='*', color='k')
                    ae.plot(a, loglog_cdfME,  'r')
                    ae.plot(b, loglog_cdfMLE,  'b')
                    ae.set_ylabel('Cumulative probability')
                    ylim = [-np.log(-np.log(1-confidence_Level[0]))-1,
                                            max(-np.log(-np.log(confidence_Level[-1]))+1,
                                                -np.log(-np.log(1-sampleCDF[-1]))+1)]
                    ae.set_ylim(ylim[0], ylim[1])
                    loglogConf = [-np.log(-np.log(conf)) for conf in confidence_Level]
                    xlim = [min(sorted(evalv)[0], min(loglogValueME), min(loglogValueMLE)),
                                sorted(evalv)[-1]]
                    ae.set_xlim(xlim[0], xlim[1])
                    if savepng:
                        aepng.scatter(sorted(evalv), -np.log(-np.log(1-sampleCDF)),
                                      marker='*', color='k')
                        aepng.plot(a, loglog_cdfME,  'r')
                        aepng.plot(b, loglog_cdfMLE,  'b')
                        aepng.set_ylabel('Cumulative probability')
                        aepng.set_ylim(ylim[0], ylim[1])
                        aepng.set_xlim(xlim[0], xlim[1])

                    for i in range(len(confidence_Level)):
                        ae.plot([xlim[0], xlim[1]], [loglogConf[i], loglogConf[i]],
                                'k--', alpha=0.2)
                        ae.annotate(str(round(confidence_Level[i], 4)), xy=(xlim[1],
                                    loglogConf[i]), xytext=(xlim[1], loglogConf[i]))
                        ae.plot([loglogValueME[i], loglogValueME[i]], [ylim[0], loglogConf[i]],
                                'r--')
                        ae.annotate(str(round(loglogValueME[i], 2)),
                                    xy=(loglogValueME[i], ylim[0]),
                                    xytext=(loglogValueME[i], ylim[0]-2),
                                    arrowprops=dict(arrowstyle="->", color='red'))
                        ae.plot([loglogValueMLE[i], loglogValueMLE[i]], [ylim[0], loglogConf[i]],
                                'b--')
                        ae.annotate(str(round(loglogValueMLE[i], 2)),
                                    xy=(loglogValueMLE[i], ylim[0]),
                                    xytext=(loglogValueMLE[i], ylim[0]-1),
                                    arrowprops=dict(arrowstyle="->", color='blue'))

                        if savepng:
                            aepng.plot([xlim[0], xlim[1]], [loglogConf[i], loglogConf[i]], 'k--',
                                       alpha=0.2)
                            aepng.annotate(str(round(confidence_Level[i], 4)),
                                           xy=(xlim[1], loglogConf[i]),
                                           xytext=(xlim[1], loglogConf[i]))
                            aepng.plot([loglogValueME[i], loglogValueME[i]],
                                       [ylim[0], loglogConf[i]], 'r--')
                            aepng.annotate(str(round(loglogValueME[i], 2)),
                                           xy=(loglogValueME[i], ylim[0]),
                                           xytext=(loglogValueME[i], ylim[0]-2),
                                           arrowprops=dict(arrowstyle="->", color='red'))
                            aepng.plot([loglogValueMLE[i], loglogValueMLE[i]],
                                       [ylim[0], loglogConf[i]], 'b--')
                            aepng.annotate(str(round(loglogValueMLE[i], 2)),
                                           xy=(loglogValueMLE[i], ylim[0]),
                                           xytext=(loglogValueMLE[i], ylim[0]-1),
                                           arrowprops=dict(arrowstyle="->", color='blue'))

                        rank = seedNo-(confidence_Level[i])*seedNo
                        enoughSeeds = seedNo >= round(1/(1-confidence_Level[i]), 4)
                        if enoughSeeds:
                            x = sortEvalv[int(rank)-1]
                            y = -np.log(-np.log(1-sampleCDF[int(rank)-1]))
                            ae.annotate('p'+str(confidence_Level[i])+' = '+str(round(x, 2)),
                                        xy=(x, y), xytext=(x, y+1.0),
                                        arrowprops=dict(arrowstyle="->", color='black'))
                            if savepng:
                                aepng.annotate('p'+str(confidence_Level[i])+' = '+str(round(x, 2)),
                                               xy=(x, y), xytext=(x, y+1.0),
                                               arrowprops=dict(arrowstyle="->", color='black'))

                elif 'Max' in sample.columns[row+3] or 'Abs' in sample.columns[row+3]:
                    loglogValueME = [ss.gumbel_r.ppf(conf, muME, betaME)
                                     for conf in confidence_Level]
                    loglogValueMLE = [ss.gumbel_r.ppf(conf, muMLE, betaMLE)
                                      for conf in confidence_Level]
                    a = sorted(evalv)
                    a.append(loglogValueME[-1])
                    b = sorted(evalv)
                    b.append(loglogValueMLE[-1])
                    loglog_cdfME = -np.log(-ss.gumbel_r.logcdf(a, muME, betaME))
                    loglog_cdfMLE = -np.log(-ss.gumbel_r.logcdf(b, muMLE, betaMLE))
                    ae.scatter(sorted(evalv), -np.log(-np.log(sampleCDF)),  marker='*', color='k')
                    ae.plot(a, loglog_cdfME,  'r')
                    ae.plot(b, loglog_cdfMLE,  'b')
                    ae.set_ylabel('Cumulative probability')
                    ylim = [-np.log(-np.log(1-confidence_Level[0]))-1,
                                            max(-np.log(-np.log(confidence_Level[-1]))+1,
                                                -np.log(-np.log(1-sampleCDF[-1]))+1)]
                    ae.set_ylim(ylim[0], ylim[1])
                    loglogConf = [-np.log(-np.log(conf)) for conf in confidence_Level]
                    xlim = [sorted(evalv)[0], max(sorted(evalv)[-1], max(loglogValueME),
                            max(loglogValueMLE))]
                    ae.set_xlim(xlim[0], xlim[1])

                    if savepng:
                        aepng.scatter(sorted(evalv), -np.log(-np.log(sampleCDF)),
                                      marker='*', color='k')
                        aepng.plot(a, loglog_cdfME,  'r')
                        aepng.plot(b, loglog_cdfMLE,  'b')
                        aepng.set_ylabel('Cumulative probability')
                        aepng.set_ylim(ylim[0], ylim[1])
                        aepng.set_xlim(xlim[0], xlim[1])

                    for i in range(len(confidence_Level)):
                        ae.plot([xlim[0], xlim[1]], [loglogConf[i], loglogConf[i]],
                                'k--', alpha=0.2)
                        ae.annotate(str(round(confidence_Level[i], 4)),
                                    xy=(xlim[1], loglogConf[i]),
                                    xytext=(xlim[1], loglogConf[i]))
                        ae.plot([loglogValueME[i], loglogValueME[i]],
                                [ylim[0], loglogConf[i]], 'r--')
                        ae.annotate(str(round(loglogValueME[i], 2)),
                                    xy=(loglogValueME[i], ylim[0]),
                                    xytext=(loglogValueME[i], ylim[0]-2),
                                    arrowprops=dict(arrowstyle="->", color='red'))
                        ae.plot([loglogValueMLE[i], loglogValueMLE[i]], [-2, loglogConf[i]], 'b--')
                        ae.annotate(str(round(loglogValueMLE[i], 2)),
                                    xy=(loglogValueMLE[i], ylim[0]),
                                    xytext=(loglogValueMLE[i], ylim[0]-1),
                                    arrowprops=dict(arrowstyle="->", color='blue'))

                        if savepng:
                            aepng.plot([xlim[0], xlim[1]], [loglogConf[i], loglogConf[i]],
                                       'k--', alpha=0.2)
                            aepng.annotate(str(round(confidence_Level[i], 4)),
                                           xy=(xlim[1], loglogConf[i]),
                                           xytext=(xlim[1], loglogConf[i]))
                            aepng.plot([loglogValueME[i], loglogValueME[i]],
                                       [ylim[0], loglogConf[i]], 'r--')
                            aepng.annotate(str(round(loglogValueME[i], 2)),
                                           xy=(loglogValueME[i], ylim[0]),
                                           xytext=(loglogValueME[i], ylim[0]-2),
                                           arrowprops=dict(arrowstyle="->", color='red'))
                            aepng.plot([loglogValueMLE[i], loglogValueMLE[i]],
                                       [-2, loglogConf[i]], 'b--')
                            aepng.annotate(str(round(loglogValueMLE[i], 2)),
                                           xy=(loglogValueMLE[i], ylim[0]),
                                           xytext=(loglogValueMLE[i], ylim[0]-1),
                                           arrowprops=dict(arrowstyle="->", color='blue'))

                        rank = confidence_Level[i]*seedNo
                        enoughSeeds = seedNo >= round(1/(1-confidence_Level[i]), 4)
                        if enoughSeeds:
                            x = sortEvalv[int(rank)-1]
                            y = -np.log(-np.log(sampleCDF[int(rank)-1]))
                            ae.annotate('p'+str(confidence_Level[i])+' = '+str(round(x, 2)),
                                        xy=(x, y), xytext=(x, y-1.0),
                                        arrowprops=dict(arrowstyle="->", color='black'))
                            if savepng:
                                aepng.annotate('p'+str(confidence_Level[i])+' = '+str(round(x, 2)),
                                               xy=(x, y), xytext=(x, y-1.0),
                                               arrowprops=dict(arrowstyle="->", color='black'))

                name = '%s Hs %.2f Tp %d wdir %d' % (sample.columns[row+3],
                                                     sample.iloc[c-seedNo, 0],
                                                     sample.iloc[c-seedNo, 1],
                                                     sample.iloc[c-seedNo, 2])
                fig.tight_layout(pad=0, w_pad=0, h_pad=0)
                if savepng: figpng.tight_layout(pad=0, w_pad=0, h_pad=0)
                os.chdir('Plots')
                fig.savefig('Gumbel-plot '+name+'.pdf', bbox_inches='tight')
                plt.close(fig)
                if savepng:
                    figpng.savefig('Gumbel-plot '+name+'.png', bbox_inches='tight')
                    plt.close(figpng)
                os.chdir('..')


def summaryDataFrame(results, confidence_Level):
    """"Create summary data frame containing Gumbel estimates"""

    # Swap params and loads at the columns' hierarchy
    res_swap = results.swaplevel(i=0, j=1, axis=1)

    # create ME, MLE and sample dataFrames and add to a summary_resultsel
    index = ['Confidence level', 'Hs', 'Tp', 'WaveDir']
    # python >= 3.5 - cool!:
    # for k, nm in enumerate([['ME', *['g ME (%s)' % str(c) for c in confidence_Level]],
    #                         ['MLE', *['g MLE(%s)' % str(c) for c in confidence_Level]],
    #                         ['sample', *['sample (%s)' % str(c) for c in confidence_Level]]]):
    # python <= 3.4 - bleh!:
    for k, nm in enumerate([
                              [item for sublist in
                                  [['ME'], ['g ME (%s)' % str(c) for c in confidence_Level]]
                                  for item in sublist],
                              [item for sublist in
                                  [['MLE'], ['g MLE(%s)' % str(c) for c in confidence_Level]]
                                  for item in sublist],
                              [item for sublist in
                                  [['sample'], ['sample (%s)' % str(c) for c in confidence_Level]]
                                  for item in sublist]
                           ]):
        for i, c in enumerate(confidence_Level):
            df = res_swap[nm[i+1]]   # ############## STOPPED HERE #####
            df['Confidence level'] = [c]*len(df)
            df['Hs'] = results.iloc[0, :, 0]
            df['Tp'] = results.iloc[0, :, 1]
            df['WaveDir'] = results.iloc[0, :, 2]
            if i == 0:                                               # In the 1st i-iteraction
                df0 = df.set_index(index).reset_index()              # create a DataFrame with the
            else:                                                    # 1st conf. level. Then update
                df0 = df0.append(df.set_index(index).reset_index())  # this df in the next iters.
        if k == 0:                            # In the first k-iteraction, create a Panel with
            summary = pd.Panel({nm[0]: df0})  # the 'ME' DataFrame. Then in the next iteractions,
        else:                                 # update this panel with the 'MLE' and finally
            summary[nm[0]] = df0              # with the 'sample' DataFrames.
    summary['ME and sample'] = summary['ME']    # Add to panel the 'XX and sample' DataFrames,
    summary['MLE and sample'] = summary['MLE']  # starting with a bare copy of the existing DFs,
    for method in ['ME', 'MLE']:                # and then replacing occurrences of
        for varname in results.items:           # 'use sample value' by the sample value.
            idx = summary[method][varname] == 'use sample value'
            summary[method+' and sample'][varname][idx] = summary['sample'][varname][idx]
    return summary


def writeResults(results, summaryResults, StatResultsFile, SummaryFile, seaStates):
    """Write results to Excel and text file"""
    # results.to_excel(StatResultsFile, index=False)
    # excel tab name max length is 31 characters
    results_short = results.rename(items=lambda s: s[:31])
    results_short.to_excel(StatResultsFile, index=False)
    summaryResults.to_excel(SummaryFile, index=False)
    return None


def main(InputFile, confidence_Level, seedNo, StatResultsFile, SummaryFile, Plot, Objectplot,
         PlotWd, PlotHs, PlotT):
    """"========================MAIN=============================="""
    # #t00 = time()
    # Read result file
    # #print('Reading input')
    sample, numRowsSample, numColsSample = readResultFile(InputFile)
    # Create panel for all results
    # #t0 = time()
    results, colnames = createResultsPanel(numRowsSample, numColsSample, seedNo,
                                           confidence_Level, sample)
    # #t_cr = time() - t0
    # Do Gumbel fit
    # #print('Gumbel fit')
    # #t0 = time()
    results = gumbelFit(confidence_Level, sample, results, seedNo, colnames)
    # #t_gf = time()-t0
    # Creates a summary file giving predicted max/min for each load case and object analysed
    # #print('Summarising and writing results to file')
    # #t0 = time()
    SummaryResults = summaryDataFrame(results, confidence_Level)
    # #t_sm = time()-t0

    # Creates a result file giving all statistical results for Gumbel fit
    seaStates = int(numRowsSample/seedNo)
    # #t0 = time()
    writeResults(results, SummaryResults, StatResultsFile, SummaryFile, seaStates)
    # # t_wr = time()-t0
    # Plot if required
    if Plot:
        print('Plotting')
        plotProbability(results, sample, colnames, seedNo, confidence_Level,
                        Objectplot, PlotWd, PlotHs, PlotT)
    # #print('Done')
    # #ttot = time()-t00
    # #print('tot\tgumbel\tsummary\twrite\tcreate')
    # #print('%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t' % (ttot, t_gf, t_sm, t_wr, t_cr))
    return results, SummaryResults


if __name__ == '__main__':
    # --------------------USER INPUT----------------------------#
    # Define number of seeds run for each load case
    seedNo = 10

    # Define confidence level
    confidence_Level = [0.9, 0.99]

    # Define if you want histogram and corresponding Gumbel fit plot for each load case
    # True = yes, False = no
    Plot = True
    # Also, specify which object you want plots for (Fill in object name (column header from
    # Input file)), and for which sea states you want plotting for
    Objectplot = ['CraneWire Max Tension', 'CraneWire Min Tension',
                  'sling1 Max Tension', 'sling1 Min Tension',
                  'sling2 Max Tension', 'sling2 Min Tension',
                  'sling3 Max Tension', 'sling3 Min Tension',
                  'sling4 Max Tension', 'sling4 Min Tension']
    PlotWd = [165, 180, 195]
    PlotHs = [2.3, 3.5]
    PlotT = [7, 8, 14]

    # Specify input file that contains data
    InputFile = 'Results.txt'

    # Specify file name for summary results
    SummaryFile = 'Summary of predicted max_min_opt.xlsx'

    # Specify file name for statistical results
    StatResultsFile = 'Statistical results_opt.xlsx'

    # #-----------------END USER INPUT------------------------#

    Results, SummaryResults = main(InputFile, confidence_Level, seedNo, StatResultsFile,
                                   SummaryFile, Plot, Objectplot, PlotWd, PlotHs, PlotT)
