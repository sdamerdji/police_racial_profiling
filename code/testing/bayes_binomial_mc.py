import numpy as np
import scipy.stats as stats
import pandas as pd
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'analysis'))
import bayes_binomial as bayes


def create_data(model_true_p, n1, n2, trials=10):
    models = np.array([1 if x > model_true_p else 2 for x in np.random.uniform(size=trials)])
    p1 = np.random.uniform(size=trials)
    p2 = np.random.uniform(size=trials)
    p2[models == 1] = p1[models == 1]

    k1 = stats.binom.rvs(n1, p1)
    k2 = stats.binom.rvs(n2, p2)

    df = pd.DataFrame(list(zip(models, p1, p2, k1, [n1] * trials, k2, [n2] * trials)),
                      columns=['true_model', 'p1', 'p2', 'k1', 'n1', 'k2', 'n2'])
    return df


def rowwise_odds(row):
    return bayes.odds_different(row['k1'], row['n1'], row['k2'], row['n2'])


def rowwise_score(row):
    if row['odds'] > 1:  # guessing it's 2-pop
        if row['true_model'] == 1:  # wrong
            score = -row['odds']
        else:
            score = 1  # right
    else:  # guessing it's 1-pop
        if row['true_model'] == 1:  # right
            score = 1
        else:
            score = -1 / row['odds']
    return score


def correct_vs_odds(df):
    bin_starts = [1, 1.5, 2, 3, 4, 5, 6, 7, 8]
    bin_ends = bin_starts[1:]
    bin_ends.append(np.infty)
    for start, end in zip(bin_starts, bin_ends):
        vc = df[(df['odds'] >= start) & (df['odds'] < end)]['true_model'].value_counts()
        if 2 in vc.keys():
            twocount = vc[2]
        else:
            twocount = 0
        if sum(vc) > 0:
            correct_frac = twocount / sum(vc)
        else:
            correct_frac = np.nan
        print("[{}, {}): Expected: {:.2f}-{:.2f}  Correct: {} of {} = {:.2f}".format(
            start, end, bayes.impliedProb(start), bayes.impliedProb(end),
            twocount, sum(vc), correct_frac))


def run_monte_carlo(model_ps=[0.25, 0.5, 0.75], ns=[20, 100, 1000], trials=10000,
                    path="../testing/mc_data"):
    os.makedirs(path, exist_ok=True)
    for model_p in model_ps:
        for n in ns:
            print("Simulating model_p={}, n={}, trials={}...".format(model_p, n, trials))
            df = create_data(model_p, n, n, trials)
            df['odds'] = df.apply(rowwise_odds, axis=1)
            df['score'] = df.apply(rowwise_score, axis=1)
            filename = "{}/mc_modelp_{}_n_{}_trials_{}.csv".format(path, model_p, n, trials)
            df.to_csv(filename, index=False)


def display_mc(model_ps=[0.25, 0.5, 0.75], ns=[20, 100, 1000], trials=10000,
               path="../testing/mc_data"):
    for model_p in model_ps:
        for n in ns:
            filename = "{}/mc_modelp_{}_n_{}_trials_{}.csv".format(path, model_p, n, trials)
            print("\nModel p = {}, n = {}, trials = {}".format(model_p, n, trials))
            try:
                df = pd.read_csv(filename)
            except Exception as e:
                print("File {} could not be read. Maybe it doesn't exist.".format(filename))
                print(e.strerror)
                continue
            correct_vs_odds(df)
