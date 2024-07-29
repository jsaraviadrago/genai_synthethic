# Generative AI and Synthethic data
This repo shows examples of data synthethization from the Vincent Granville book[[1]](#1). It doesn't only show the answers to the task but also other situations were this technology has been used. 

The idea of this repo is to show you how to create synthethic data bsed on the exercise from the book. There are some important files here:

- **Example_insurance.py:** here there is all the script to create synthethic data which throws a .txt file with the synthethic data. 
- **Notebook_task1.ipynb:** here there is all the process that I followed to create the synthethic data. 
  - The first part is an example.
  - The second part is creating synthethic data from real data and plotting
  - The third part is creating synthethic data from the synthethic data and then plotting. The detail is explained in the notebook.

- The data is "insurance.csv" which you can find the details from it here[[2]](#2). Regardless of that, in the Notebook you can also find the urls from where I got the information so you can reproduce it. 
- The script_holdout_insurance_df.py is just a script I created to seperate the real data in half and have a test and train. 

The algorithm used hear is "copulas", you can find reference of it in the synthetic data book

### Reference

<a id="1">[1]</a>
Granville, V. (2022).
[Synthetic Data and Generative AI](https://mltechniques.com/2022/11/28/new-book-synthetic-data/)
Mltecniques.

<a id="2">[2]</a>
Datta, A. (2020).
[US Health Insurance Dataset](https://www.kaggle.com/datasets/teertha/ushealthinsurancedataset)
Kaggle. 