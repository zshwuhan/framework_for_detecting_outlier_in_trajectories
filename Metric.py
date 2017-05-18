'''
Created on Nov 23, 2016

@author: zahran
'''
from MyEnums import *
from scipy.stats import chisquare, fisher_exact
from scipy.stats.contingency import expected_freq, chi2_contingency
import numpy as np

class Metric:
    def __init__(self):
        self.type = None
        pass
    def update(self, decisions, goldMarkers):
        pass
    
    

class Chisq(Metric):    
    def __init__(self):  
        self.type = METRIC.CHI_SQUARE          
        self.OT = 0 #OT: Decision=outlier and friendship=True.
        self.OF = 0 
        self.NT = 0
        self.NF = 0 #NF: Decision=Normal  and friendship=False      
        self.expectedOT = 0
        self.expectedOF = 0
        self.expectedNT = 0
        self.expectedNF = 0
        self.stats = None
    
    def getSummary(self):
        myStr = 'OT='+str(self.OT)+', OF='+str(self.OF)+', NT='+str(self.NT)+', NF='+str(self.NF)+', stats='+str(self.stats)
        return myStr
        
    def update(self, decisions, goldMarkers):
        for i in range(len(decisions)):        
            if(decisions[i] == DECISION.OUTLIER and goldMarkers[i] == GOLDMARKER.TRUE):
                self.OT += 1        
            elif(decisions[i] == DECISION.OUTLIER and goldMarkers[i] == GOLDMARKER.FALSE):
                self.OF += 1
            elif(decisions[i] == DECISION.NORMAL and goldMarkers[i] == GOLDMARKER.TRUE):
                self.NT += 1
            elif(decisions[i] == DECISION.NORMAL and goldMarkers[i] == GOLDMARKER.FALSE):
                self.NF += 1
        
        ''' 
        row0 = self.OT + self.OF # no. of outliers
        row1 = self.NT + self.NF
        col0 = self.OT + self.NT
        col1 = self.OF + self.NF
        grandTotal = row0+row1
                
        self.expectedOT = float(row0*col0)/float(grandTotal)
        self.expectedOF = float(row0*col1)/float(grandTotal)
        self.expectedNT = float(row1*col0)/float(grandTotal)
        self.expectedNF = float(row1*col1)/float(grandTotal)
        
        self.stats = chisquare([self.OT, self.OF, self.NT, self.NF], f_exp=[self.expectedOT, self.expectedOF, self.expectedNT, self.expectedNF], ddof=2)
        #ci = chi2_contingency([self.OT, self.OF, self.NT, self.NF])
        
        #print(self.stats, oddsratio, pvalue)
        #print('myExpected:'+str([self.expectedOT, self.expectedOF, self.expectedNT, self.expectedNF]))
        #ep = expected_freq([self.OT, self.OF, self.NT, self.NF])
        #cm = np.array_equal(ep, np.array([self.expectedOT, self.expectedOF, self.expectedNT, self.expectedNF]))
        #print(cm)
        #if(not cm):       
        #    print('\nERROR in exp cnt\n')
        #print('\n')
        '''
                
    def calculateStats(self):
        row0 = self.OT + self.OF # no. of outliers
        row1 = self.NT + self.NF
        col0 = self.OT + self.NT
        col1 = self.OF + self.NF
        grandTotal = row0+row1
                
        self.expectedOT = float(row0*col0)/float(grandTotal)
        self.expectedOF = float(row0*col1)/float(grandTotal)
        self.expectedNT = float(row1*col0)/float(grandTotal)
        self.expectedNF = float(row1*col1)/float(grandTotal)
        
        self.stats = chisquare([self.OT, self.OF, self.NT, self.NF], f_exp=[self.expectedOT, self.expectedOF, self.expectedNT, self.expectedNF], ddof=2)
        
        
        

class Fisher(Metric):    
    def __init__(self):  
        self.type = METRIC.FISHER          
        self.OT = 0 #OT: Decision=outlier and friendship=True.
        self.OF = 0 
        self.NT = 0
        self.NF = 0 #NF: Decision=Normal  and friendship=False             
        self.stats = None
    
    def getSummary(self):
        myStr = 'OT='+str(self.OT)+', OF='+str(self.OF)+', NT='+str(self.NT)+', NF='+str(self.NF)+', stats='+str(self.stats)
        return myStr
        
    def update(self, decisions, goldMarkers):
        for i in range(len(decisions)):        
            if(decisions[i] == DECISION.OUTLIER and goldMarkers[i] == GOLDMARKER.TRUE):
                self.OT += 1        
            elif(decisions[i] == DECISION.OUTLIER and goldMarkers[i] == GOLDMARKER.FALSE):
                self.OF += 1
            elif(decisions[i] == DECISION.NORMAL and goldMarkers[i] == GOLDMARKER.TRUE):
                self.NT += 1
            elif(decisions[i] == DECISION.NORMAL and goldMarkers[i] == GOLDMARKER.FALSE):
                self.NF += 1
            
        
        #self.stats = [fisher_exact([[self.OT, self.OF], [self.NT, self.NF]])]
    
    def calculateStats(self):
        self.stats = [fisher_exact([[self.OT, self.OF], [self.NT, self.NF]])]
        
        
        
class rpf(Metric): #recall_precision_fscore
    def __init__(self): 
        self.type = METRIC.REC_PREC_FSCORE
        self.OT = 0 #OT: Decision=outlier and friendship=True. (tp)
        self.OF = 0 #fp
        self.NT = 0 #fn
        self.NF = 0 #NF: Decision=Normal  and friendship=False (tn)
        self.stats = None   
    
    def getSummary(self):
        myStr = 'OT='+str(self.OT)+', OF='+str(self.OF)+', NT='+str(self.NT)+', NF='+str(self.NF)+', stats='+str(self.stats)
        return myStr
    
    def update(self, decisions, goldMarkers):
        for i in range(len(decisions)):   
            if(decisions[i] == DECISION.OUTLIER and goldMarkers[i] == GOLDMARKER.TRUE):
                self.OT += 1        
            elif(decisions[i] == DECISION.OUTLIER and goldMarkers[i] == GOLDMARKER.FALSE):
                self.OF += 1
            elif(decisions[i] == DECISION.NORMAL and goldMarkers[i] == GOLDMARKER.TRUE):
                self.NT += 1
            elif(decisions[i] == DECISION.NORMAL and goldMarkers[i] == GOLDMARKER.FALSE):
                self.NF += 1
    '''
        try:         
            rec  = float(self.OT)/float(self.OT + self.NT) #tp/tp+fn
            prec = float(self.OT)/float(self.OT + self.OF)
            fscore= (2*prec*rec) / (prec+rec)
            self.stats = [rec, prec, fscore]
        except:
            self.stats = [0,0,0]
    '''
            
    def calculateStats(self):
        try:         
            rec  = float(self.OT)/float(self.OT + self.NT) #tp/tp+fn
            prec = float(self.OT)/float(self.OT + self.OF)
            fscore= (2*prec*rec) / (prec+rec)
            self.stats = [rec, prec, fscore]
        except:
            self.stats = [0,0,0]
        
    
    

class Bayesian(Metric):    
    def __init__(self):  
        self.type = METRIC.BAYESIAN          
        self.OT = 0 #OT: Decision=outlier and friendship=True.
        self.OF = 0 
        self.NT = 0
        self.NF = 0 #NF: Decision=Normal  and friendship=False             
        self.stats = None
        self.samplesCount = 5000
        self.OT_priorConst = 1.0
        self.OF_priorConst = 1.0
        self.NT_priorConst = 1.0
        self.NF_priorConst = 1.0
    
    def getSummary(self):
        myStr = 'OT='+str(self.OT)+', OF='+str(self.OF)+', NT='+str(self.NT)+', NF='+str(self.NF)+', stats='+str(self.stats)
        return myStr
        
    def update(self, decisions, goldMarkers):
        for i in range(len(decisions)):        
            if(decisions[i] == DECISION.OUTLIER and goldMarkers[i] == GOLDMARKER.TRUE):
                self.OT += 1        
            elif(decisions[i] == DECISION.OUTLIER and goldMarkers[i] == GOLDMARKER.FALSE):
                self.OF += 1
            elif(decisions[i] == DECISION.NORMAL and goldMarkers[i] == GOLDMARKER.TRUE):
                self.NT += 1
            elif(decisions[i] == DECISION.NORMAL and goldMarkers[i] == GOLDMARKER.FALSE):
                self.NF += 1
            
        
        #self.stats = [fisher_exact([[self.OT, self.OF], [self.NT, self.NF]])]
    
    def calculateStats(self):
        trueCount_TgO = 0
        trueCount_OT = 0
        trueCount_full = 0
        P_T = float(self.NT+self.OT) / float(self.OF+self.OT+self.NT+self.NF)
        P_F = float(self.NF+self.OF) / float(self.OF+self.OT+self.NT+self.NF)
        
        OT_post = self.OT + self.OT_priorConst * P_T
        OF_post = self.OF + self.OF_priorConst * P_F
        NT_post = self.NT + self.NT_priorConst * P_T
        NF_post = self.NF + self.NF_priorConst * P_F
        
        for i in range(self.samplesCount):
            P = np.random.dirichlet((OT_post, OF_post, NT_post, NF_post), 1)
            #P = np.random.dirichlet((self.OT+1, self.OF+1, self.NT+1), 1)
            P_OT = P[0][0]
            P_OF = P[0][1]
            P_NT = P[0][2]
            P_NF = P[0][3]
            
            P_O = P_OT + P_OF
            P_TgO = P_OT / P_O
            P_T = P_OT + P_NT
            
            if((P_OT*P_NF) > (P_OF*P_NT)):
                trueCount_full += 1
                
            if(P_TgO > P_T):
                trueCount_TgO += 1
            
            if(P_OT > (P_T*P_O)):
                trueCount_OT += 1
            
        
        self.probTrue_TgO = float(trueCount_TgO) / float(self.samplesCount)
        self.probTrue_OT = float(trueCount_OT) / float(self.samplesCount)
        self.probTrue_full = float(trueCount_full) / float(self.samplesCount)
        
        self.stats = ['Full', self.probTrue_full,'T|O', self.probTrue_TgO,'OT', self.probTrue_OT]
    

def main():
    b = Bayesian()
    b.OT = 0
    b.NF = 250
    b.OF = 0
    b.NT = 250
    b.calculateStats()
    print(b.getSummary())
    
main() 

    
        
