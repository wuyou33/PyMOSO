"""The solve and testsolve command"""

from .basecomm import *
from inspect import getmembers, isclass


class Solve(BaseComm):
    """Run some experiment"""
    def run(self):
        trials = int(self.options['--trials'])
        name = self.options['--name']
        budgarg = self.options['--budget']
        budget = int(budgarg)
        prntype = mrg.MRG32k3a
        probarg = self.options['<problem>']
        probmod = getattr(orclib, probarg)
        solvarg = self.options['<solver>'][0]
        solvclasses = getmembers(solvers, isclass)
        solvclass = [solvc[1] for solvc in solvclasses if solvc[0] == solvarg][0]
        params = self.options['<param>']
        vals = self.options['<val>']
        paramtups = []
        for i, p in enumerate(params):
            ptup = (p, float(vals[i]))
            paramtups.append(ptup)
        orcseeds, solvseeds, xorseeds = get_seeds()
        xprn = mrg.MRG32k3a(xorseeds[0])
        print('*********** Beginning Optimization Trials ***********')
        start_opt_time = time.time()
        joblst = []
        for t in range(trials):
            orcseed = orcseeds[t]
            solvseed = solvseeds[t]
            x0 = get_x0(probmod, xprn)
            tup = (solvclass, budget, probmod, prntype, orcseed, prntype, solvseed, x0, paramtups)
            joblst.append(tup)
        res = mprun.par_runs(joblst)
        end_opt_time = time.time()
        opt_durr = end_opt_time - start_opt_time
        humtxt = gen_humanfile(name, probarg, solvarg, budget, opt_durr, trials, params, vals)
        print('-- Run time: {0:.2f} seconds'.format(opt_durr))
        print('-- Saving data and details in folder ', name, ' ...')
        save_files(name, humtxt, res)
        print('-- Done!')