'''
Created on Nov 27, 2016

@author: Mohamed Zahran
'''
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.interpolate import spline

#plt.ion()
import numpy as np
from math import log

import sys 
sys.path.append('../')
#sys.path.append('/Users/mohame11/anaconda/lib/python2.7/site-packages/')
from MyEnums import *

class MyPlot():

    def __init__(self, tag, path, metric, figs, minAlpha=0, maxAlpha=1e10):
        self.tag = tag
        self.path = path
        self.metric = metric        
        self.mapping = {}
        self.x = []
        self.figs = figs
        self.minAlpha = minAlpha
        self.maxAlpha = maxAlpha
        
        self.parse()       
    
    def parse(self):
        r = open(self.path, 'r')
        for line in r:
            parts = line.split(':')
            params = parts[0].split(',')
            results = parts[-1].replace(')','').replace('(','').split(',')
            
            config = ', '.join(params[1:])
            alpha = float(params[0].split('=')[-1])
            if(alpha < self.minAlpha):
                continue
            if(alpha > self.maxAlpha):
                continue
            
            if(alpha not in self.x):
                self.x.append(alpha)
                
            if(self.metric == METRIC.CHI_SQUARE):  
                res = float(results[-1].split('=')[-1])  
                              
            elif(self.metric == METRIC.FISHER):  
                res = float(results[-1].split('=')[-1].replace(']',''))
                                            
            elif(self.metric == METRIC.RECALL):
                res = float(results[-3].split('=')[-1].replace('[',''))
                
            elif(self.metric == METRIC.PRECISION):
                res = float(results[-2])
                
            elif(self.metric == METRIC.FSCORE):
                res = float(results[-1].split('=')[-1].replace(']',''))
                
            elif(self.metric == METRIC.ACCURACY):
                tp=float(results[0].split('=')[-1])
                fp=float(results[1].split('=')[-1])
                fn=float(results[2].split('=')[-1])
                tn=float(results[3].split('=')[-1])
                res = (tp+tn)/(tp+tn+fp+fn)
                
            elif(self.metric == METRIC.TRUE_NEGATIVE_RATE):
                tp=float(results[0].split('=')[-1])
                fp=float(results[1].split('=')[-1])
                fn=float(results[2].split('=')[-1])
                tn=float(results[3].split('=')[-1])
                res = tn/(tn+fp)
            
            elif(self.metric == METRIC.FALSE_POSITIVE_RATE):
                tp=float(results[0].split('=')[-1])
                fp=float(results[1].split('=')[-1])
                fn=float(results[2].split('=')[-1])
                tn=float(results[3].split('=')[-1])
                res = fp/(tn+fp)
                
            elif(self.metric == METRIC.BAYESIAN):
                res = float(results[-1].replace(']',''))
                res = 1 - res
            
            elif(self.metric == METRIC.AUC):
                tp=float(results[0].split('=')[-1])
                fp=float(results[1].split('=')[-1])
            
            #if(res == np.NaN):
            #    print 'NaN exists !'
            #    res = 0.0
                
            if(config not in self.mapping):                
                self.mapping[config] = {alpha:res}
            else:
                self.mapping[config][alpha] = res
        
        
        r.close()
    
    def plot(self):       
        plt.rc('legend',**{'fontsize':13})
        for i in range(len(self.figs)):
            plt.figure(i)
            plt.xlabel('Alpha')
            plt.ylabel(str(self.metric))
            plt.xticks([log(x,10) for x in self.x])  
            
            #plt.legend(loc='upper right')   
                             
            #plt.title(self.figs[i])                      
            figConfigSet = {}               
            for cf in self.mapping:
                if(self.figs[i] in cf):
                    if('TScountAdj=True' in cf):
                        continue
                    figConfigSet[cf] = []
                
            for x in self.x:    
                for cf in figConfigSet:                    
                    figConfigSet[cf].append(self.mapping[cf][x])
            
            lgx = [log(x,10) for x in self.x]
            flg = True
            for cf in figConfigSet:                                                          
#                 if(flg):                                                                                                           
#                     lines = plt.plot(lgx, figConfigSet[cf], '--r', label=cf)
#                     flg = False
#                 else:
#                     lines = plt.plot(lgx, figConfigSet[cf], 'b', label=cf)
                
                lines = plt.plot(lgx, figConfigSet[cf], label=cf)
                plt.setp(lines, linewidth=2.0)  
                plt.legend(bbox_to_anchor=(0., 1.00, 1.00, .101), loc=3, ncol=1, mode="expand", borderaxespad=0.)
                #lines = plt.plot(lgx, figConfigSet[cf], label=cf)                                                            
                
        plt.show()
    
       
    @staticmethod
    def fusePlots(allPlots, optAlpa='' , useLog=True, my_yaxis_label='', title='', savedFigFileName = 'foo.pdf'):
        title = title.replace('cumulative p-value','').replace('ranking p-value','').replace(',','')
        plt.rc('legend',**{'fontsize':10})        
        fig = plt.figure(0)
        #fig = plt.figure(0, figsize=(12, 8))
        plt.ylabel(my_yaxis_label)
        if(useLog):
            plt.xticks([log(x,10) for x in allPlots[0].x], rotation='vertical')
            plt.xlabel('log10(alpha_i)')
        else:
            plt.xticks([x for x in allPlots[0].x], rotation='vertical')
            plt.xlabel(r"${\alpha_i}$")  
        
        #plt.tick_params(axis='both', which='major', labelsize=10)
        for p in allPlots:
            figConfigSet = {}               
            for cf in p.mapping:                
                if(p.figs[0] in cf):
                    if('TScountAdj=True' in cf or 'HOLMS' in cf):
                        continue
                    figConfigSet[cf] = []
            
              
            for x in p.x:    
                for cf in figConfigSet:                    
                    figConfigSet[cf].append(p.mapping[cf][x])
            
            if(useLog):
                xvalues = [log(x,10) for x in p.x]
            else:
                xvalues = [x for x in  p.x]     
                
            
            for cf in figConfigSet:   
                #lines = plt.plot(xvalues, figConfigSet[cf], '--r', label='Tribeflow')
                #lines = plt.plot(xvalues, figConfigSet[cf], 'b', label='Ngram LM')
                
                '''
                xnew = np.linspace(min(xvalues), max(xvalues), 1000) # the last param represents number of points to make between T.min and T.max
                smoothed = spline(xvalues, figConfigSet[cf], xnew)
                for it in range(len(smoothed)):
                    if(smoothed[it] > 1.0):
                        smoothed[it] = 1.0
                    if(smoothed[it] < 0):
                        smoothed[it] = 0.0
                lines = plt.plot(xnew, smoothed, label=p.tag)
                '''
                
                lines = plt.plot(xvalues, figConfigSet[cf], label=p.tag)
                
                
        
        #add a line at y=0.05 (Alpha2)
        #lines = plt.plot(xvalues, [0.05 for x in xvalues], ':g', label='Significance level threshold at 5%')
        
        #add a line at 0.95 for the simulated data (false discovery rate)
        #lines = plt.plot(xvalues, [0.95 for x in xvalues], '-o', label='False Discovery Rate')
        
        #0.169 +/- 0.0560267793113
        if(optAlpa != ''):
            a = float(optAlpa)
            if(useLog):
                a = log(a,10)
            lines = plt.plot([a, a], [-0.1, 1.1], '--', label='Chosen Alpha*')
            
                  
        plt.setp(lines, linewidth=2.0)
          
        plt.legend(bbox_to_anchor=(0., 1.00, 1.00, .101), loc=3, ncol=2, mode="expand", borderaxespad=0., prop={'size':9}) #legend font size
        
        axes = plt.gca()
        #axes.set_xlim([-10,0.01])
        
        #control the value ranges of yaxis
        axes.set_ylim([-0.1,1.1])
        
        #control values ranges to show in the yaxis
        plt.yticks(list(np.arange(-0.1, 1.1, 0.1)))
        
        #caption
        if(title != ''):
            fig.suptitle(title, fontsize=12, fontweight='bold', horizontalalignment='center', y=.89)
            #fig.text(.3, .9, title, fontsize=10)
            #fig.text(.1, .1, r'an equation: $E=mc^2$', fontsize=15)

        plt.grid()                                                                       
        plt.savefig(savedFigFileName, bbox_inches='tight')
        plt.show()
        
            

def tribflow9(pv):
    resultsPath = '/Users/mohame11/Documents/newResults/'
    title = 'Tribeflow: B=9, '
    if(pv == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
        minAlpha = 1e-20
        maxAlpha = 1
        useLog = True
        optAlpha = 1.93103637695e-14#currentAlpha= 1.93103637695e-14  metric= 0.949128546326
        #alpha=1.93103637695e-14, TECHNIQUE.MAJORITY_VOTING, HYP.EMPIRICAL, TScountAdj=False: OT=71, OF=144319, NT=535, NF=1419172, stats=[(1.3050167616092931, 0.041379281249816546)]
        tr9_likes = resultsPath+'tribeflow9/'+'pins_repins_tribeflow9_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITHOUT_RANKING'
        tr9_likes_bayesian = resultsPath+'tribeflow9/'+'pins_repins_tribeflow9_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITHOUT_RANKING'
        tr9_sim = resultsPath+'tribeflow9/'+'pins_repins_tribeflow9_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
        tr9_injSim = resultsPath+'tribeflow9/'+'pins_repins_tribeflow9_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    
    elif(pv == PVALUE.WITH_RANKING):
        title += 'ranking p-value'
        minAlpha = 0.001
        maxAlpha = 1
        useLog = False
        optAlpha = 0.663492063492 #currentAlpha= 0.663492063492  metric= 0.950273711071
        #alpha=0.663492063492, TECHNIQUE.MAJORITY_VOTING, HYP.EMPIRICAL, TScountAdj=False: OT=29, OF=39714, NT=577, NF=1523777, stats=[(1.9284126303765161, 0.0016460749449736768)]
        tr9_likes = resultsPath+'tribeflow9/'+'pins_repins_tribeflow9_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITH_RANKING'
        tr9_likes_bayesian = resultsPath+'tribeflow9/'+'pins_repins_tribeflow9_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITH_RANKING'
        tr9_sim = resultsPath+'tribeflow9/'+'pins_repins_tribeflow9_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
        tr9_injSim = resultsPath+'tribeflow9/'+'pins_repins_tribeflow9_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
    
    
    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', tr9_likes_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', tr9_likes, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', tr9_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('tr9_injSim', tr9_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1, p2, p3], '', useLog=useLog, my_yaxis_label = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'tr9_'+str(pv).replace('.','_')+'.pdf')   

def tribflow9_lastfm(pv):
    resultsPath = '/Users/mohame11/Documents/newResults_lastfm/'
    title = 'Tribeflow: B=9, '
    if(pv == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
        minAlpha = 1e-20
        maxAlpha = 1
        useLog = True
        optAlpha = 1.1828125e-17 #currentAlpha= 1.1828125e-17  metric= 0.950564710239
        
        #tr9_likes = resultsPath+'tribeflow9/'+'lastfm_tribeflow9_noWin_log_simInj_METRIC.FISHER_PVALUE.WITHOUT_RANKING'
        #tr9_likes_bayesian = resultsPath+'tribeflow9/'+'lastfm_tribeflow9_noWin_log_simInj_METRIC.BAYESIAN_PVALUE.WITHOUT_RANKING'
        
        tr9_likes = '/Users/mohame11/Documents/newResults_lastfm/pvalues_tribeflow_injection2/METRIC.FISHER_PVALUE.WITHOUT_RANKING'
        tr9_likes_bayesian = '/Users/mohame11/Documents/newResults_lastfm/pvalues_tribeflow_injection2/METRIC.BAYESIAN_PVALUE.WITHOUT_RANKING'
        
        tr9_sim = resultsPath+'tribeflow9/'+'lastfm_tribeflow9_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
        
    
    elif(pv == PVALUE.WITH_RANKING):
        title += 'ranking p-value'
        minAlpha = 0.001
        maxAlpha = 1
        useLog = False
        optAlpha = 0.95015625 #currentAlpha= 0.95015625  metric= 0.950101832994
        
        tr9_likes = resultsPath+'tribeflow9/'+'lastfm_tribeflow9_noWin_log_simInj_METRIC.FISHER_PVALUE.WITH_RANKING'
        tr9_likes_bayesian = resultsPath+'tribeflow9/'+'lastfm_tribeflow9_noWin_log_simInj_METRIC.BAYESIAN_PVALUE.WITH_RANKING'
        
        #tr9_likes = '/Users/mohame11/Documents/newResults_lastfm/pvalues_tribeflow_injection2/METRIC.FISHER_PVALUE.WITH_RANKING'
        #tr9_likes_bayesian = '/Users/mohame11/Documents/newResults_lastfm/pvalues_tribeflow_injection2/METRIC.BAYESIAN_PVALUE.WITH_RANKING'
        
        tr9_sim = resultsPath+'tribeflow9/'+'lastfm_tribeflow9_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
        
    
    
    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', tr9_likes_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', tr9_likes, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', tr9_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('tr9_injSim', tr9_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1, p2, p3], '', useLog=useLog, my_yaxis_label = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'tr9_lastfm_'+str(pv).replace('.','_')+'.pdf')   

def tribflow3(pv):
    resultsPath = '/Users/mohame11/Documents/newResults/'
    title = 'Tribeflow: B=3, '
    if(pv == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
        minAlpha = 1e-20
        maxAlpha = 1
        useLog = True
        optAlpha = 1.6328125e-06 #currentAlpha= 1.6328125e-06  metric= 0.949703225457
        tr3_bayesian = resultsPath+'tribeflow3/'+'pins_repins_tribeflow3_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITHOUT_RANKING'
        tr3_likes = resultsPath+'tribeflow3/'+'pins_repins_tribeflow3_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITHOUT_RANKING'
        tr3_sim = resultsPath+'tribeflow3/'+'pins_repins_tribeflow3_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
        tr3_injSim = resultsPath+'tribeflow3/'+'pins_repins_tribeflow3_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    
    elif(pv == PVALUE.WITH_RANKING):
        title += 'ranking p-value'
        minAlpha = 0.001
        maxAlpha = 1
        useLog = False
        optAlpha = 0.66875 #currentAlpha= 0.66875  metric= 0.949882445972
        tr3_bayesian = resultsPath+'tribeflow3/'+'pins_repins_tribeflow3_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITH_RANKING'
        tr3_likes = resultsPath+'tribeflow3/'+'pins_repins_tribeflow3_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITH_RANKING'
        tr3_sim = resultsPath+'tribeflow3/'+'pins_repins_tribeflow3_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
        tr3_injSim = resultsPath+'tribeflow3/'+'pins_repins_tribeflow3_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
    
    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', tr3_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', tr3_likes, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', tr3_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('tr9_injSim', tr9_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1, p2, p3], '', useLog=useLog, my_yaxis_label ='Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'tr3_'+str(pv).replace('.','_')+'.pdf')   
        
def ngram3(pv):
    resultsPath = '/Users/mohame11/Documents/newResults/'
    title = 'Ngram LM: B=3, '
    if(pv == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
        minAlpha = 1e-6
        maxAlpha = 1
        useLog = True
        optAlpha = 0.01474609375 #currentAlpha= 0.01474609375  metric= 0.950344687785
        ngram3_likes = resultsPath+'ngram3/'+'pins_repins_ngram3_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITHOUT_RANKING'
        ngram3_bayesian = resultsPath+'ngram3/'+'pins_repins_ngram3_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITHOUT_RANKING'
        ngram3_sim = resultsPath+'ngram3/'+'pins_repins_ngram3_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
        ngram3_injSim = resultsPath+'ngram3/'+'pins_repins_ngram3_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    
    else:
        title += 'ranking p-value'
        minAlpha = 0.001
        maxAlpha = 1
        useLog = False
        optAlpha = 0.7265625 #currentAlpha= 0.7265625  metric= 0.949231892086
        ngram3_likes = resultsPath+'ngram3/'+'pins_repins_ngram3_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITH_RANKING'
        ngram3_bayesian = resultsPath+'ngram3/'+'pins_repins_ngram3_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITH_RANKING'
        ngram3_sim = resultsPath+'ngram3/'+'pins_repins_ngram3_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
        ngram3_injSim = resultsPath+'ngram3/'+'pins_repins_ngram3_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
    

    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', ngram3_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', ngram3_likes, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', ngram3_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('ngram3_injSim', ngram3_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1, p2, p3], '', useLog=useLog, my_yaxis_label = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'ngram3_'+str(pv).replace('.','_')+'.pdf')

def ngram9(pv):
    resultsPath = '/Users/mohame11/Documents/newResults/'
    title = 'Ngram LM: B=9, '
    if(pv == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
        minAlpha = 1e-5
        maxAlpha = 1
        useLog = True
        optAlpha = 0.0152734375 #currentAlpha= 0.0152734375  metric= 0.94963912974
        #alpha=0.0152734375, TECHNIQUE.MAJORITY_VOTING, HYP.EMPIRICAL, TScountAdj=False: OT=195, OF=385700, NT=2781, NF=5823001, stats=[(1.058597461738265, 0.44731697960223149)]
        ngram9_bayesian = resultsPath+'ngram9/'+'pins_repins_ngram9_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITHOUT_RANKING'
        ngram9_likes = resultsPath+'ngram9/'+'pins_repins_ngram9_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITHOUT_RANKING'
        ngram9_sim = resultsPath+'ngram9/'+'pins_repins_ngram9_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
        ngram9_injSim = resultsPath+'ngram9/'+'pins_repins_ngram9_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    
    else:
        title += 'ranking p-value'
        minAlpha = 0.001
        maxAlpha = 1
        useLog = False
        optAlpha = 0.725 #currentAlpha= 0.725  metric= 0.949647407388
        #alpha=0.725, TECHNIQUE.MAJORITY_VOTING, HYP.EMPIRICAL, TScountAdj=False: OT=102, OF=204304, NT=2874, NF=6004397, stats=[(1.0430519459233127, 0.64389006895189893)]
        ngram9_bayesian = resultsPath+'ngram9/'+'pins_repins_ngram9_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITH_RANKING'
        ngram9_likes = resultsPath+'ngram9/'+'pins_repins_ngram9_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITH_RANKING'
        ngram9_sim = resultsPath+'ngram9/'+'pins_repins_ngram9_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
        ngram9_injSim = resultsPath+'ngram9/'+'pins_repins_ngram9_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
    

    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', ngram9_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', ngram9_likes, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', ngram9_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('ngram3_injSim', ngram3_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1, p2, p3], '', useLog=useLog, my_yaxis_label = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'ngram9_'+str(pv).replace('.','_')+'.pdf')
    
def rnnlm3(pv):
    resultsPath = '/Users/mohame11/Documents/newResults/'
    title = 'RNN LM: B=3, '
    if(pv == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
        minAlpha = 1e-5
        maxAlpha = 1
        useLog = True
        optAlpha = 0.050078125#currentAlpha= 0.050078125  metric= 0.95029157259 '0.01 +/- 0' #'0.01 +/- 6.93889390391e-18'
        rnn3_likes = resultsPath+'rnnlm3/'+'pins_repins_rnnlm3_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITHOUT_RANKING'
        rnn3_bayesian = resultsPath+'rnnlm3/'+'pins_repins_rnnlm3_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITHOUT_RANKING'
        rnn3_sim = resultsPath+'rnnlm3/'+'pins_repins_rnnlm3_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
        rnn3_injSim = resultsPath+'rnnlm3/'+'pins_repins_rnnlm3_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    
    
    else:
        title += 'ranking p-value' 
        minAlpha = 0.001
        maxAlpha = 1
        useLog= False
        optAlpha = 0.84375 #currentAlpha= 0.84375  metric= 0.948298457199'0.653 +/- 0' #'0.653 +/- 0.0607536007163'
        rnn3_likes = resultsPath+'rnnlm3/'+'pins_repins_rnnlm3_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITH_RANKING'
        rnn3_bayesian = resultsPath+'rnnlm3/'+'pins_repins_rnnlm3_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITH_RANKING'
        rnn3_sim = resultsPath+'rnnlm3/'+'pins_repins_rnnlm3_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
        rnn3_injSim = resultsPath+'rnnlm3/'+'pins_repins_rnnlm3_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
    
    
    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', rnn3_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', rnn3_likes, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', rnn3_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('rnn3_injSim', rnn3_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1,p2,p3], '', useLog=useLog, my_yaxis_label = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'rnn3_'+str(pv).replace('.','_')+'.pdf')

def rnnlm9(pv):
    resultsPath = '/Users/mohame11/Documents/newResults/'
    title = 'RNN LM: B=9, '
    if(pv == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
        minAlpha = 1e-5
        maxAlpha = 1
        useLog = True
        optAlpha = 0.051484375 #currentAlpha= 0.051484375  metric= 0.949489375515
        #alpha=0.051484375, TECHNIQUE.MAJORITY_VOTING, HYP.EMPIRICAL, TScountAdj=False: OT=194, OF=381470, NT=2782, NF=5827231, stats=[(1.0652375067224999, 0.40078734063955179)]
        rnn9_bayesian = resultsPath+'rnnlm9/'+'pins_repins_rnnlm9_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITHOUT_RANKING'
        rnn9_likes = resultsPath+'rnnlm9/'+'pins_repins_rnnlm9_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITHOUT_RANKING'
        rnn9_sim = resultsPath+'rnnlm9/'+'pins_repins_rnnlm9_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
        rnn9_injSim = resultsPath+'rnnlm9/'+'pins_repins_rnnlm9_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    
    
    else:
        title += 'ranking p-value' 
        minAlpha = 0.001
        maxAlpha = 1
        useLog= False
        optAlpha = 0.84375 #currentAlpha= 0.84375  metric= 0.949382091047
        #alpha=0.84375, TECHNIQUE.MAJORITY_VOTING, HYP.EMPIRICAL, TScountAdj=False: OT=190, OF=364882, NT=2786, NF=5843819, stats=[(1.092236801093418, 0.2420666488452653)]
        rnn9_bayesian = resultsPath+'rnnlm9/'+'pins_repins_rnnlm9_noWin_log_allLikes_METRIC.BAYESIAN_PVALUE.WITH_RANKING'
        rnn9_likes = resultsPath+'rnnlm9/'+'pins_repins_rnnlm9_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITH_RANKING'
        rnn9_sim = resultsPath+'rnnlm9/'+'pins_repins_rnnlm9_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
        rnn9_injSim = resultsPath+'rnnlm9/'+'pins_repins_rnnlm9_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
    
    
    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', rnn9_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', rnn9_likes, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', rnn9_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('rnn3_injSim', rnn3_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1,p2,p3], '', useLog=useLog, my_yaxis_label = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'rnn9_'+str(pv).replace('.','_')+'.pdf')
       
def bagOfAction9(pv):
    resultsPath = '/Users/mohame11/Documents/newResults/'
    title = 'Bag of actions'
    if(pv == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
        minAlpha = 0
        maxAlpha = 1
        useLog = True
        optAlpha = 0.0504296875 #currentAlpha= 0.0504296875  metric= 0.950514517272
        bag_likes = resultsPath+'bagOfActions/'+'pins_repins_bag_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITHOUT_RANKING'
        bag_sim = resultsPath+'bagOfActions/'+'pins_repins_bag_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
        bag_injSim = resultsPath+'bagOfActions/'+'pins_repins_bag_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    
    
    elif(pv == PVALUE.WITH_RANKING):
        title += 'ranking p-value' 
        minAlpha = 0.001
        maxAlpha = 1
        useLog= False
        optAlpha = 0.7984375 #currentAlpha= 0.7984375  metric= 0.950514517272
        bag_likes = resultsPath+'bagOfActions/'+'pins_repins_bag_noWin_log_allLikes_METRIC.FISHER_PVALUE.WITH_RANKING'
        bag_sim = resultsPath+'bagOfActions/'+'pins_repins_bag_noWin_log_simData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
        bag_injSim = resultsPath+'bagOfActions/'+'pins_repins_bag_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_PVALUE.WITH_RANKING'
    
    else: #standAlone
        title += ''
        minAlpha = 0
        maxAlpha = 1
        useLog = False
        optAlpha = 0.0494244384766 #currentAlpha= 0.0494244384766  metric= 0.950462015992
        bag_likes = resultsPath+'bagOfActions/'+'standAlone_bagOfActions_allLikes10'
        bag_likes_bayesian = resultsPath+'bagOfActions/'+'standAlone_bagOfActions_allLikes10_bayesian'
        bag_sim = resultsPath+'bagOfActions/'+'standAlone_bagOfActions_simulatedData_10'
        #bag_injSim = resultsPath+'bagOfActions/'+'standAlone_bagOfActions_simulatedData_10'
    
    
    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', bag_likes_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', bag_likes, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', bag_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('rnn3_injSim', rnn3_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1,p2,p3], '', useLog=useLog, my_yaxis_label = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'bagOfActions9_'+str(pv).replace('.','_')+'.pdf')

def bagOfAction3(pv):
    resultsPath = '/Users/mohame11/Documents/newResults/'
    title = 'Bag of actions: B=3, '
    
    title += ''
    minAlpha = 0
    maxAlpha = 1
    useLog = False
    optAlpha = 0.0483161491527 ##currentAlpha= 0.0483161491527  metric= 0.949222693317
    bag_fisher = resultsPath+'bagOfActions/'+'standAlone_bagOfActions_allLikes4'
    bag_bayesian = resultsPath+'bagOfActions/'+'standAlone_bagOfActions_allLikes4_bayesian'
    bag_sim = resultsPath+'bagOfActions/'+'standAlone_bagOfActions_simulatedData_4'
    
    
    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', bag_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', bag_fisher, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', bag_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('rnn3_injSim', rnn3_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1,p2,p3], '', useLog=useLog, my_yaxis_label = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'bagOfActions3_'+str(pv).replace('.','_')+'.pdf')

def bagOfAction_lastfm(pv):
    resultsPath = '/Users/mohame11/Documents/newResults_lastfm/'
    title = 'Bag of actions: B=9, '
    
    title += ''
    minAlpha = 0
    maxAlpha = 1
    useLog = False
    optAlpha = 0.048671875 #currentAlpha= 0.048671875  metric= 0.95047
    
    bag_fisher = resultsPath+'bagOfActions/'+'bag10_fisher'
    bag_bayesian = resultsPath+'bagOfActions/'+'bag10_bayesian'
    
    #bag_fisher = resultsPath+'bagOfActions/'+'bag10_fisher_smallOutliers'
    #bag_bayesian = resultsPath+'bagOfActions/'+'bag10_bayesian_smallOutliers'
    
    bag_sim = resultsPath+'bagOfActions/'+'bag10_sim'
    
    
    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', bag_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', bag_fisher, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', bag_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('rnn3_injSim', rnn3_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1,p2,p3], '', useLog=useLog, my_yaxis_label = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR', title=title, savedFigFileName = 'bagOfActions_lastfm_'+str(pv).replace('.','_')+'.pdf')




def plotAUCexperiment(PLOT_TITLE='', NAME='', PV ='', MIN_ALPHA='', MAX_ALPHA='', OPT_ALPHA =''):
    resultsPath = '/Users/mohame11/Documents/myFiles/Career/Work/Purdue/PhD_courses/projects/outlierDetection/Results/newResults/'
    title = PLOT_TITLE
    minAlpha = MIN_ALPHA
    maxAlpha = MAX_ALPHA
    optAlpha = OPT_ALPHA
    if(PV == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
    else:
        title += 'ranking p-value' 
        
    plot_bayesian = resultsPath+NAME+'/'+'pins_repins_'+NAME+'_noWin_log_allLikes_METRIC.BAYESIAN_'+str(PV)
    r = open(plot_bayesian, 'r')
    x = []
    y = []
    fig = plt.figure(0)
    for line in r:
        parts = line.split(':')
        params = parts[0].split(',')
        results = parts[-1].replace(')','').replace('(','').split(',')
        
        config = ', '.join(params[1:])
        alpha = float(params[0].split('=')[-1])
        if(alpha < minAlpha):
            continue
        if(alpha > maxAlpha):
            continue
        
        tp=float(results[0].split('=')[-1])
        fp=float(results[1].split('=')[-1])
        x.append(fp)
        y.append(tp)
        
    lines = plt.plot(x, y, label=PLOT_TITLE) 
    plt.setp(lines, linewidth=2.0)
          
    plt.legend(bbox_to_anchor=(0., 1.00, 1.00, .101), loc=3, ncol=2, mode="expand", borderaxespad=0., prop={'size':9}) #legend font size
    
    axes = plt.gca()
   
    #control the value ranges of yaxis
    #axes.set_ylim([-0.1,1.1])
    
    #control values ranges to show in the yaxis
    #plt.yticks(list(np.arange(-0.1, 1.1, 0.1)))
    
    #caption
    if(title != ''):
        fig.suptitle(title, fontsize=12, fontweight='bold', horizontalalignment='center', y=.89)
        #fig.text(.3, .9, title, fontsize=10)
        #fig.text(.1, .1, r'an equation: $E=mc^2$', fontsize=15)

    plt.grid()               
    savedFigFileName = NAME+'_'+str(PV).replace('.','_')+'AUC.pdf'                                                        
    plt.savefig(savedFigFileName, bbox_inches='tight')
    plt.show() 
    
    

def plotExperiment(PLOT_TITLE='', NAME='', PV ='', MIN_ALPHA='', MAX_ALPHA='', OPT_ALPHA ='', USELOG='', YAXIS_LABEL=''):
    resultsPath = '/Users/mohame11/Documents/myFiles/Career/Work/Purdue/PhD_courses/projects/outlierDetection/Results/newResults/'
    title = PLOT_TITLE
    minAlpha = MIN_ALPHA
    maxAlpha = MAX_ALPHA
    useLog = USELOG
    optAlpha = OPT_ALPHA
    if(PV == PVALUE.WITHOUT_RANKING):
        title += 'cumulative p-value'
    else:
        title += 'ranking p-value' 
    
    plot_bayesian = resultsPath+NAME+'/'+'pins_repins_'+NAME+'_noWin_log_allLikes_METRIC.BAYESIAN_'+str(PV)
    plot_likes = resultsPath+NAME+'/'+'pins_repins_'+NAME+'_noWin_log_allLikes_METRIC.FISHER_'+str(PV)
    plot_sim = resultsPath+NAME+'/'+'pins_repins_'+NAME+'_noWin_log_simData_METRIC.REC_PREC_FSCORE_'+str(PV)
    plot_injSim = resultsPath+NAME+'/'+'pins_repins_'+NAME+'_noWin_log_simInjectedData_METRIC.REC_PREC_FSCORE_'+str(PV)
    
    
    p1 = MyPlot('Bayesian\'s test p-value: likes trajectories', plot_bayesian, METRIC.BAYESIAN, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p2 = MyPlot('Fisher\'s test p-value: likes trajectories', plot_likes, METRIC.FISHER, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    p3 = MyPlot('False Discovery Rate (FDR): Simulated data', plot_sim, METRIC.FALSE_POSITIVE_RATE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    #p3 = MyPlot('rnn3_injSim', rnn3_injSim, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)], minAlpha, maxAlpha)
    MyPlot.fusePlots([p1,p2,p3], '', useLog=useLog, my_yaxis_label = YAXIS_LABEL, title=title, savedFigFileName = NAME+'_'+str(PV).replace('.','_')+'.pdf')
    

def main():
    mpl.rcParams.update({'font.size': 11})
    
    #plotExperiment(PLOT_TITLE = 'Tribeflow: B=3, ', NAME = 'tribeflow3', PV = PVALUE.WITHOUT_RANKING, MIN_ALPHA = 1e-20, MAX_ALPHA = 1, OPT_ALPHA = 1.6328125e-06, USELOG = True,YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    #plotExperiment(PLOT_TITLE = 'Tribeflow: B=3, ', NAME = 'tribeflow3', PV = PVALUE.WITH_RANKING,    MIN_ALPHA = 0.001, MAX_ALPHA = 1, OPT_ALPHA = 0.66875, USELOG = False, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    
    #plotExperiment(PLOT_TITLE = 'Ngram LM: B=3, ', NAME = 'ngram3', PV = PVALUE.WITHOUT_RANKING, MIN_ALPHA = 1e-6, MAX_ALPHA = 1, OPT_ALPHA = 0.01474609375, USELOG = True, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    #plotExperiment(PLOT_TITLE = 'Ngram LM: B=3, ', NAME = 'ngram3', PV = PVALUE.WITH_RANKING,    MIN_ALPHA = 0.001, MAX_ALPHA = 1, OPT_ALPHA = 0.7265625, USELOG = False, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    
    #plotExperiment(PLOT_TITLE = 'RNN LM: B=3, ', NAME = 'rnnlm3', PV = PVALUE.WITHOUT_RANKING, MIN_ALPHA = 1e-5, MAX_ALPHA = 1, OPT_ALPHA = 0.050078125, USELOG = True, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    #plotExperiment(PLOT_TITLE = 'RNN LM: B=3, ', NAME = 'rnnlm3', PV = PVALUE.WITH_RANKING,    MIN_ALPHA = 0.001, MAX_ALPHA = 1, OPT_ALPHA = 0.84375, USELOG = False, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    
    
    
    #plotExperiment(PLOT_TITLE = 'Tribeflow: B=9, ', NAME = 'tribeflow9', PV = PVALUE.WITHOUT_RANKING, MIN_ALPHA = 1e-20, MAX_ALPHA = 1, OPT_ALPHA = 1.93103637695e-14, USELOG = True, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    #plotExperiment(PLOT_TITLE = 'Tribeflow: B=9, ', NAME = 'tribeflow9', PV = PVALUE.WITH_RANKING,    MIN_ALPHA = 0.001, MAX_ALPHA = 1, OPT_ALPHA = 0.663492063492, USELOG = False, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    
    #plotExperiment(PLOT_TITLE = 'Tribeflow: B=9, ', NAME = 'tribeflow9', PV = PVALUE.WITH_RANKING,    MIN_ALPHA = 0.001, MAX_ALPHA = 1, OPT_ALPHA = 0.663492063492, USELOG = False, USED_METRICS=METRIC.AUC, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    plotAUCexperiment(PLOT_TITLE = 'Tribeflow: B=9, ', NAME = 'tribeflow9', PV = PVALUE.WITH_RANKING,    MIN_ALPHA = 0.001, MAX_ALPHA = 1, OPT_ALPHA = 0.663492063492)
    
    #plotExperiment(PLOT_TITLE = 'Ngram LM: B=9, ', NAME = 'ngram9', PV = PVALUE.WITHOUT_RANKING, MIN_ALPHA = 1e-5, MAX_ALPHA = 1, OPT_ALPHA = 0.0152734375, USELOG = True, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    #plotExperiment(PLOT_TITLE = 'Ngram LM: B=9, ', NAME = 'ngram9', PV = PVALUE.WITH_RANKING,    MIN_ALPHA = 0.001, MAX_ALPHA = 1, OPT_ALPHA = 0.725, USELOG = False, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    
    #plotExperiment(PLOT_TITLE = 'RNN LM: B=9, ', NAME = 'rnnlm9', PV = PVALUE.WITHOUT_RANKING, MIN_ALPHA = 1e-5, MAX_ALPHA = 1, OPT_ALPHA = 0.051484375, USELOG = True, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    #plotExperiment(PLOT_TITLE = 'RNN LM: B=9, ', NAME = 'rnnlm9', PV = PVALUE.WITH_RANKING,    MIN_ALPHA = 0.001, MAX_ALPHA = 1, OPT_ALPHA = 0.84375, USELOG = False, YAXIS_LABEL = 'Bayesian\'s test p-value / Fisher\'s test p-value  / FDR')
    
    '''
    tribflow3(PVALUE.WITHOUT_RANKING)
    tribflow3(PVALUE.WITH_RANKING)
    ngram3(PVALUE.WITHOUT_RANKING)
    ngram3(PVALUE.WITH_RANKING)
    rnnlm3(PVALUE.WITHOUT_RANKING)
    rnnlm3(PVALUE.WITH_RANKING)
    
    bagOfAction3('alone') #currentAlpha= 0.0483161491527  metric= 0.949222693317
    '''
    
    '''
    tribflow9(PVALUE.WITHOUT_RANKING)
    tribflow9(PVALUE.WITH_RANKING)
    ngram9(PVALUE.WITHOUT_RANKING)
    ngram9(PVALUE.WITH_RANKING)
    rnnlm9(PVALUE.WITHOUT_RANKING)
    rnnlm9(PVALUE.WITH_RANKING)
    '''
    #bagOfAction9('alone')
    


    
    
    ####################################
    
    
    #tribflow9_lastfm(PVALUE.WITH_RANKING)
    #tribflow9_lastfm(PVALUE.WITHOUT_RANKING)
    #bagOfAction_lastfm('alone')
    
   
    



    '''
    ########################################################################
    unixdata_win10_path = '/Users/mohame11/Documents/myFiles/Career/Work/Purdue/PhD_courses/projects/outlierDetection/UNIX_user_data/win10/'
    unixdata_win4_path =  '/Users/mohame11/Documents/myFiles/Career/Work/Purdue/PhD_courses/projects/outlierDetection/UNIX_user_data/win4/'
    
    #win10
    tribeflow_win10_simInj = unixdata_win10_path + 'tribeflow/' + 'unixdata_tribeflow_win10_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    ngram_win10_simInj = unixdata_win10_path + 'ngram/' + 'unixdata_9gram_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    
    #p9 =  MyPlot('tribeflow_win10_simInj', tribeflow_win10_simInj, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)])
    #p10 = MyPlot('ngram_win10_simInj', ngram_win10_simInj, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)])  
    #MyPlot.fusePlots([p9 , p10], useLog=True, my_yaxis_label = 'F1 score', savedFigFileName = 'unixdata_simInj_win10.pdf')

    #win4
    tribeflow_win4_simInj = unixdata_win4_path + 'tribeflow/' + 'unixdata_tribeflow4_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    ngram_win4_simInj = unixdata_win4_path + 'ngram/' + 'unixdata_ngram3_METRIC.REC_PREC_FSCORE_PVALUE.WITHOUT_RANKING'
    
    #p11 =  MyPlot('tribeflow_win4_simInj', tribeflow_win4_simInj, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)])
    #p12 = MyPlot('ngram_win4_simInj', ngram_win4_simInj, METRIC.FSCORE, [str(TECHNIQUE.MAJORITY_VOTING)])  
    #MyPlot.fusePlots([p11 , p12], useLog=True, my_yaxis_label = 'F1 score', savedFigFileName = 'unixdata_simInj_win4.pdf')
    '''
    

    print('Done !')
      
    
main()
