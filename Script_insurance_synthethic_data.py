import pandas as pd
import numpy as np
from scipy.stats import norm
import csv

url2 = "https://raw.githubusercontent.com/jsaraviadrago/genai_synthethic/main/"
insurance_compare_train = 'insurance_compare_train.csv'

filename = url2 + insurance_compare_train

# Read the CSV file into a DataFrame
df = pd.read_csv(filename)

# Group by 'sex', 'smoker', and 'region'
grouped = df.groupby(['sex', 'smoker', 'region'])

# Initialize dictionaries to store group counts and group lists
groupCount = {}
groupList = {}

# Iterate over each group and its corresponding DataFrame
for group, group_df in grouped:
    sex, smoker, region = group
    group_key = f"{sex}\t{smoker}\t{region}"

    for cnt, row in enumerate(group_df.itertuples(index=False)):
        groupCount[group_key] = cnt + 1
        groupList[(group_key, cnt)] = (row.age, row.bmi, row.children, row.charges)

# Seed for reproducibility
seed = 453
np.random.seed(seed)

# Output file
OUT = open("insurance_synth.txt", "w")

# Generate synthetic data
for group in groupCount:
    nobs = groupCount[group]
    age = []
    bmi = []
    children = []
    charges = []

    for cnt in range(nobs):
        features = groupList[(group, cnt)]
        age.append(float(features[0]))  # uniform outside very young or very old
        bmi.append(float(features[1]))  # Gaussian distribution?
        children.append(float(features[2]))  # geometric distribution?
        charges.append(float(features[3]))  # bimodal, not gaussian

    mu = [np.mean(age), np.mean(bmi), np.mean(children), np.mean(charges)]
    zero = [0, 0, 0, 0]
    z = np.stack((age, bmi, children, charges), axis=0)
    corr = np.corrcoef(z)  # correlation matrix for Gaussian copula for this group

    print("------------------")
    print("\n\nGroup: ", group, "[", nobs, "obs ]\n")
    print("mean age: %2d\nmean bmi: %2d\nmean children: %1.2f\nmean charges: %2d\n"
          % (mu[0], mu[1], mu[2], mu[3]))
    print("correlation matrix:\n")
    print(corr, "\n")

    nobs_synth = nobs  # number of synthetic obs to create for this group
    gfg = np.random.multivariate_normal(zero, corr, nobs_synth)
    g_age = gfg[:, 0]
    g_bmi = gfg[:, 1]
    g_children = gfg[:, 2]
    g_charges = gfg[:, 3]

    # Generate synthetic observations for this group
    print("synthetic observations:\n")
    for k in range(nobs_synth):
        u_age = norm.cdf(g_age[k])
        u_bmi = norm.cdf(g_bmi[k])
        u_children = norm.cdf(g_children[k])
        u_charges = norm.cdf(g_charges[k])
        s_age = np.quantile(age, u_age)  # synthesized age
        s_bmi = np.quantile(bmi, u_bmi)  # synthesized bmi
        s_children = np.quantile(children, u_children)  # synthesized children
        s_charges = np.quantile(charges, u_charges)  # synthesized charges

        line = group + "\t" + str(s_age) + "\t" + str(s_bmi) + "\t" + str(s_children) + "\t" + str(s_charges) + "\n"
        OUT.write(line)
        print("%3d. %d %d %d %d" % (k, s_age, s_bmi, s_children, s_charges))

OUT.close()
