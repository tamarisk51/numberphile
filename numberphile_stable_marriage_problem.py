# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 13:20:36 2014

@author: James
"""

class Women():
    def __init__(self,name,preferences):
        self.name = name
        self.preferences = preferences
        self.hope_rank = 0
        self.tentative_partner = None

    def propose(self):
        global men
        if self.tentative_partner is None:
            man_to_proposed_to = self.preferences[self.hope_rank]
            men[man_to_proposed_to].proposals.append(self.name)
            
            print self.name,'proposes to',man_to_proposed_to     
                    
class Men():
    def __init__(self,name,preferences):
        self.name = name
        self.preferences = preferences
        self.proposals = []
        self.tentative_partner = None
    
    def respond_to_proposals(self):               
        global women
        # Find the best proposal, if any.
        best = None
        for woman in self.proposals:
            if best is None:
                best = woman
            elif self.preferences.index(woman)<self.preferences.index(best):
                best = woman
             
        # Compare proposals, accept or decline them
        if best is not None:
            if self.tentative_partner is None:       
                # accept best proposal
                self.tentative_partner = best
                women[best].tentative_partner = self.name
                # send out declinations
                self.proposals.remove(best)
                for w in self.proposals:
                    women[w].hope_rank +=1
                self.proposals = []

            
                if len(self.proposals)>0:
                    print "{} accepts {}, declines({})".format(
                            self.name,best,', '.join(self.proposals))
                else:
                    print "{} accepts {}".format(
                            self.name,best)
       
            elif self.tentative_partner is not None:
                 current_rank =  self.preferences.index(self.tentative_partner)           
                 new_rank = self.preferences.index(best)     
                 if new_rank < current_rank:
                     # reject current tentative partner
                     rejected = self.tentative_partner
                     women[self.tentative_partner].tentative_partner = None
                     women[self.tentative_partner].hope_rank +=1
                     # accept best proposal
                     self.tentative_partner = best
                     women[best].tentative_partner = self.name
                     # send out declinations
                     self.proposals.remove(best)
                     for w in self.proposals:
                         women[w].hope_rank +=1
                     self.proposals = []
          
                     if len(self.proposals)>0:
                         print "{} rejects {}, accepts {}, declines({})".format(
                         self.name,rejected,best,', '.join(self.proposals))
                     else:
                         print "{} rejects {}, accepts {}".format(
                         self.name,rejected,best) 
           
                 elif new_rank > current_rank:
                     # send out declinations
                     for w in self.proposals:
                         women[w].hope_rank +=1
                     self.proposals = []
                         
                     print "{} declines({})".format(
                         self.name,', '.join(self.proposals)) 
                               
def all_matched(women):
    all_matched=True
    for name in women:
        if women[name].tentative_partner is None:
            all_matched=False
    return all_matched

if __name__=='__main__':
    
    womens_preferences = {'Charlotte':['Bingley','Darcy','Collins','Wickham'],
                          'Elizabeth':['Wickham','Darcy','Bingley','Collins'],
                          'Jane':['Bingley','Wickham','Darcy','Collins'],
                          'Lydia':['Bingley','Wickham','Darcy','Collins']
                          }
    mens_preferences = {'Bingley':['Jane','Elizabeth','Lydia','Charlotte'],
                        'Collins':['Jane','Elizabeth','Lydia','Charlotte'],
                        'Darcy':['Elizabeth','Jane','Charlotte','Lydia'],
                        'Wickham':['Lydia','Jane','Elizabeth','Charlotte']
                        }       
                        
    men = {}                   
    for name in mens_preferences:
        men[name] = Men(name,mens_preferences[name])
    women = {}                   
    for name in womens_preferences:
        women[name] = Women(name,womens_preferences[name])
    
    day=0
    while not all_matched(women):
        print ' '
        print '### Day =',day,'###'
        # Women give proposals
        for wname in women:
            women[wname].propose()
        print ' - - - '        
        # Men evaluate their proposals
        for mname in men:
            men[mname].respond_to_proposals()
        print ' - - - '
        print '# Matches at end of Day',day              
        for name in women:
            print name," ~ ",women[name].tentative_partner
        day +=1

