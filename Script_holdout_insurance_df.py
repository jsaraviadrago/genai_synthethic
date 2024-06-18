import pandas as pd

insurance_compare = 'insurance_compare.csv'
url = "https://raw.githubusercontent.com/jsaraviadrago/genai_synthethic/main/"

raw_insurance_compare_update = url + insurance_compare

df_insurance_compare_update = pd.read_csv(raw_insurance_compare_update) #step 3

# Filter the data just to get real data.
df_insurance_compare_update_real = df_insurance_compare_update.loc[df_insurance_compare_update['Data'] == 'Real']

# Hold 50% of the real data to make the synthetise data.
#df_insurance_compare_update_real_train = df_insurance_compare_update_real.sample(frac=0.5).reset_index()
df_insurance_compare_update_real_train = df_insurance_compare_update_real.iloc[:669,] # Getting the first 668
df_insurance_compare_update_real_test = df_insurance_compare_update_real.iloc[670:,] # Getting the last 668

df_insurance_compare_update_real_train = df_insurance_compare_update_real_train.dropna(axis= 'columns')
df_insurance_compare_update_real_train = df_insurance_compare_update_real_train.drop('Data', axis=1)

df_insurance_compare_update_real_train.to_csv("insurance_compare_train.csv", sep=',', encoding='utf-8', index=False)
#df_insurance_compare_update_real_test.to_csv("insurance_compare_test.csv", sep=',', encoding='utf-8')


