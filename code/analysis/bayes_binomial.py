'''
These functions allow you to compare two sets of count data, and determine the odds they come from the
same underlying process.

So, for example, 350 out of 500 white people got a citation, and 45 out of 200 Black people got a citation.
What are the odds that the police are actually giving out citations at the same rate, and the apparent difference
is just statistical fluctuations?

The math is described here: https://docs.google.com/document/d/1PIbjUNIGPNrwBhwurz1mnvWimBgyyVz7SXAQBopg1FQ/edit#heading=h.6p0r8oblogaq
This will be proven out using a monte carlo in code/simulations/bayes_binomial_sim.py

In all of this file, we use:
n1, k1: For the first population, there are k1 positives in n1 total.
n2, k2: For the second population, there are k2 positives in n2 total.
'''

import numpy as np
import scipy.stats as stats
import scipy.integrate as integrate


def binprob(p, k, n):
    # scipy.integrate wants the integration parameter first, so let's make a wrapper function
    return stats.binom.pmf(k, n, p)


def onepop(k1, n1, k2, n2):
    '''
    :return: the non-normalized posterior of a one-population binomial model, marginalized over p
    '''
    integrand = lambda p: binprob(p, k1, n1) * binprob(p, k2, n2)
    result = integrate.quad(integrand, 0, 1)
    return result[0]


def twopop(k1, n1, k2, n2):
    '''
    :return: the non-normalized posterior of a two-population binomial model marginalized over both p's
    '''
    part1 = integrate.quad(binprob, 0, 1, (k1, n1))
    part2 = integrate.quad(binprob, 0, 1, (k2, n2))
    return part1[0] * part2[0]


def odds_different(k1, n1, k2, n2, prior=1):
    '''
    Odds ratio that the two-population is favored over the one-population.
    :param prior: Defaults to uniform ratio preference. >1 implies prior prefers two-pop
    :return: Odds ratio, >1 prefers two-pop
    '''
    one = onepop(k1, n1, k2, n2)
    if one == 0:
        result = np.infty
    else:
        result = prior * twopop(k1, n1, k2, n2) / one
    return result


def impliedProb(odds):
    '''
    Return implied probability [0,1] from a given odds ratio
    :param odds: odds
    :return: probability
    '''
    return (odds / (odds + 1))
