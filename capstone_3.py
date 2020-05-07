# -*- coding: utf-8 -*-
"""CAPSTONE 3

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DV47odusZQD1ALVheMY0Hc6xdg34JxRg

<p><img alt="Colaboratory logo" height="45px" src="/img/colab_favicon.ico" align="left" hspace="10px" vspace="0px"></p>

<h1>Welcome to Colaboratory!</h1>


Colaboratory is a free Jupyter notebook environment that requires no setup and runs entirely in the cloud.

With Colaboratory you can write and execute code, save and share your analyses, and access powerful computing resources, all for free from your browser.
"""

#@title Introducing Colaboratory { display-mode: "form" }
#@markdown This 3-minute video gives an overview of the key features of Colaboratory:
from IPython.display import YouTubeVideo
YouTubeVideo('inN8seMm7UI', width=600, height=400)

!pip install sqlalchemy
!pip install psycopg2


# Import the SQL ALchemy engine
from sqlalchemy import create_engine

# Database credentials
postgres_user = 'dabc_student'
postgres_pw = '7*.8G9QH21'
postgres_host = '142.93.121.174'
postgres_port = '5432'
postgres_db = 'homecreditdefaultrisk'

# use the credentials to start a connection
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
postgres_user, postgres_pw, postgres_host, postgres_port, postgres_db))

"""Anlysis on repayment capabilities of different categories of loan applicants related to to financial institutions.

***Methodology***
Use application data from  previous loans which are reported to credit bureau and provide information on demographic and historical credit behavior of current application loan data.

**Limitations**
Due to  the first function comparing paid applicants over overdue applicants conclusions are only from the analysis of current data based from loan_application_train. Since many data is missing(NULL values) from different columns, analysis accuracy is not based on many depended data columns. This function is limited based on amount income input by the user.
Second function is based on overall paid and overdue loan numbers of applicants conclusions are not based on amounts of paid and overdue. I have limited the data input while extracting data from SQL database due to large number of data and risk of system craching & producing delayed results.
Third function for predicting repayment abilities of loan applicants for calculating interest  is not based on data provided by bereau or current applicants rate. There is no data provided on past repayment data abilities of past applicants on percentage basis or number basis.


**Next steps**
The first functions can be analyzed by credit input by user with same function.
Second fuction can be improvised by including if else statements of amounts of paid/unpaid.
Third function can be improvised by gathering and using current interest rates institutions following and  repayment data abilities of the previous applicants.

> Indented block
"""

# importing pandas as pd 
import pandas as pd 
import numpy as np
import math
import seaborn as sns 
import matplotlib.pyplot as plt
sns.set(style="white")
sns.set()
import warnings
warnings.filterwarnings("ignore")
np.seterr(divide='ignore', invalid='ignore')
class style:
   BOLD = '\033[1m'
   END = '\033[0m'
from pylab import rcParams
rcParams['figure.figsize'] = 20,8



# Compare paid applicants vs overdue applicants*******************************
overduecheck='''
SELECT name_income_type,name_family_status,name_contract_type,code_gender,amt_income_total,amt_credit
FROM loan_application_train  
'''

catagoryapp_df = pd.read_sql_query(overduecheck, con=engine)
engine.dispose()

lowest_income = int(input("Enter the lowest side of income you want to calculate? Minimal amount can be entered is 25650...."))
highest_income = int(input("Enter the highest side of the income you want to calculate? Maximum amount can be entered is 1.17e+08.... "))


def catagory_income(b):
    income1=income2=income3=credit1=credit2=credit3=income4=credit4=0
    
    visual=[]
    for data in b:
      if lowest_income <= data[0] and highest_income >= data[0] and choice[0]==data[1]:
          income1=income1+data[0]
          credit1=credit1+data[2]
          visual.append(data)
         
      elif lowest_income <= data[0] and highest_income >= data[0] and choice[1]==data[1]:
           income2=income2+data[0]
           credit2=credit2+data[2]
           visual.append(data)
          
      elif lowest_income <= data[0] and highest_income >= data[0] and choice[2]==data[1]:
           income3=income3+data[0]
           credit3=credit3+data[2]
           visual.append(data)
        
      elif lowest_income <= data[0] and highest_income >= data[0] and choice[3]==data[1]:
           income4=income4+data[0]
           credit4=credit4+data[2]
           visual.append(data)
          
    
    print('\033[1m' +"****Total Income and Credit calculation between income of $"+str(lowest_income)+" and $"+ str(highest_income) +
                  "  based on by income selection and catagory*****\n"+ '\033[0m')


    print(("The Total Income for "+choice[0] + " catagory,is :${}, and Total credit is :${}\n").format(income1,credit1,)+
           ("The Total Income for "+choice[1] + " catagory, is :${},and Total credit is :${}\n").format(income2,credit2)+
          ("The Total Income for "+choice[2] + " catagory, is :${}, and Total credit is :${}\n").format(income3,credit3)+
          ("The Total Income for "+choice[3] + " catagory,is :${}, and Total credit is :${}\n").format(income4,credit4))

    visual_df = pd.DataFrame(visual, columns = ['amt_income_total', 'category','amt_credit']) 
    #sns.lineplot(x='amt_income_total', y='amt_credit',hue='category',data=visual_df)
    sns.relplot(x='amt_income_total', y='amt_credit',hue='category', 
            sizes=(40, 400), alpha=.5, palette="muted",
            height=6, data=visual_df)
   
catagory=(catagoryapp_df[['amt_income_total','code_gender','amt_credit']]).values         
choice=(['F','M','XNA',''])
catagory_income(catagory) 
 
catagory=(catagoryapp_df[['amt_income_total','name_income_type','amt_credit']]).values
choice=(['Working','State servant','Commercial associate','Pensioner'])
catagory_income(catagory)

print("=========================================================================================================================================")

# Compare paid applicants vs overdue applicants*******************************
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
np.seterr(divide='ignore', invalid='ignore')
import plotly.express as px

overduecheck='''
SELECT credit_day_overdue,name_income_type,name_family_status,name_contract_type,code_gender
FROM loan_application_train  JOIN bureau
ON loan_application_train.sk_id_curr=bureau.sk_id_curr
LIMIT 75000
'''
loanapp_df = pd.read_sql_query(overduecheck, con=engine)
engine.dispose()


def overdues(a):
    overdue1=paid1=overdue2=paid2=overdue3=paid3=overdue4=paid4=overdue5=paid5=overdue6=paid6=0
    
    visual2=[]
    paid=[]
    for dues in a:
          if dues[1]==choice[0] and dues[0]> 0:
              overdue1=overdue1+1
              visual2.append(dues)
          elif dues[1]==choice[0] and dues[0]==0:
              paid1=paid1+1
              paid.append(dues)
          elif dues[1]==choice[1] and dues[0]> 0:
              overdue2=overdue2+1
              visual2.append(dues)
          elif dues[1]==choice[1] and dues[0]==0:
              paid2=paid2+1
              paid.append(dues)
          elif dues[1]==choice[2] and dues[0]> 0:
              overdue3=overdue3+1
              visual2.append(dues)
          elif dues[1]==choice[2] and dues[0]==0:
              paid3=paid3+1
              paid.append(dues)
          elif dues[1]==choice[3] and dues[0]> 0:
              overdue4=overdue4+1
              visual2.append(dues)
          elif dues[1]==choice[3] and dues[0]==0:
              paid4=paid4+1
              paid.append(dues)
          elif dues[1]!=(choice[1],choice[2],choice[3],choice[0]) and dues[0]>0:
               overdue5=overdue5+1
               visual2.append(dues)
          elif dues[1]!=(choice[1],choice[2],choice[3],choice[0]) and dues[0]==0:
               paid5=paid5+1
               paid.append(dues)
          else:
               overdue6=overdue6+1
               visual2.append(dues)
               paid6=0
               paid.append(dues)
          
          
    print('\033[1m' +"\n********Compare paid applicants vs overdue applicants*******************************"+ '\033[0m') 
    
       
    percent1=round(np.divide(overdue1*100,(overdue1+paid1)),2)  
    percent2=round(np.divide(paid1*100,(overdue1+paid1)),2) 
    percent3=round(np.divide(overdue2*100,(overdue2+paid2)),2)
    percent4=round(np.divide(paid2*100,(overdue2+paid2)),2)
    percent5=round(np.divide(overdue3*100,(overdue4+paid4)),2)
    percent6=round(np.divide(paid4*100,(overdue4+paid4)),2)
    percent5=round(np.divide(overdue3*100,(overdue3+paid3)),2)
    percent6=round(np.divide(paid3*100,(overdue3+paid3)),2)
    percent7=round(np.divide(overdue4*100,(overdue4+paid4)),2)
    percent8=round(np.divide(paid4*100,(overdue4+paid4)),2)
    percent9=round(np.divide(overdue5*100,(overdue5+paid5)),2)
    percent10=round(np.divide(paid5*100,(overdue5+paid5)),2) 
     
    print( "\nThe number of "+choice[0]+" applicants for overdues are  :{} with {}% and paid are {} with {}% ".format(overdue1,percent1,paid1,percent2)+
           "\nThe number of "+choice[1]+" applicants for overdues are  :{} with {}% and paid are {} with {}% ".format(overdue2,percent3,paid2,percent4)+
           "\nThe number of "+choice[2]+" applicants for overdues are  :{} with {}% and paid are {} with {}% ".format(overdue3,percent5,paid3,percent6)+
           "\nThe number of "+choice[3]+" applicants for overdues are  :{} with {}% and paid are {} with {}% ".format(overdue4,percent7,paid4,percent8)+
           "\nThe number of other applicants for overdues are  :{} with {}% and paid are {} with {}%\n ".format(overdue5,percent9,paid5,percent10))   
    
    
    #sns.boxenplot(x="Overdue", y="Category",
           #   color="b", 
              #scale="linear", data=visual_df )
    visual_df1 = pd.DataFrame(visual2, columns = ['Overdue','Category'])
    visual_df2=  pd.DataFrame(paid, columns = ['Paid','Category'])
    df_cd = pd.merge(visual_df1, visual_df2, how='inner', on = 'Category')
    #sns.scatterplot(x="Overdue", y="Paid", hue="Category", data=df_cd)
    sns.relplot(x='Overdue', y='Paid',hue='Category', 
            sizes=(40, 400), alpha=.5, palette="muted",
            height=6, data=df_cd)
       
      

overdue_days=(loanapp_df[['credit_day_overdue','code_gender']]).values
choice=(['F','M','XNA',''])
overdues(overdue_days)

overdue_days=(loanapp_df[['credit_day_overdue','name_family_status']]).values
choice=(['Single / not married','Married','Civil marriage','Widow'])
overdues(overdue_days)

overdue_days=(loanapp_df[['credit_day_overdue','name_contract_type']]).values
choice=(['Cash loans','Revolving loans','',''])
overdues(overdue_days)

overdue_days=(loanapp_df[['credit_day_overdue','name_income_type']]).values
choice=(['Working','State servant','Commercial associate','Pensioner'])
overdues(overdue_days)


print("=========================================================================================================================================")

#***********Predict clients repayment abilities according to catagories**************************************


repaymentcheck='''
SELECT code_gender,name_income_type,amt_credit_sum,credit_day_overdue,amt_credit_sum_overdue FROM bureau JOIN loan_application_train
ON bureau.sk_id_curr = loan_application_train.sk_id_curr
WHERE credit_day_overdue > 0
ORDER BY credit_day_overdue
'''
repayanalysis_df = pd.read_sql_query(repaymentcheck, con=engine)
engine.dispose()

conditions=[
       (repayanalysis_df['credit_day_overdue']<=30),
       (repayanalysis_df['credit_day_overdue']>=30) & (repayanalysis_df['credit_day_overdue']<=60),
       (repayanalysis_df['credit_day_overdue']>=60) & (repayanalysis_df['credit_day_overdue']<=90),
       (repayanalysis_df['credit_day_overdue']>=90) & (repayanalysis_df['credit_day_overdue']<=180),
       (repayanalysis_df['credit_day_overdue']>=180) & (repayanalysis_df['credit_day_overdue']<=365),
       (repayanalysis_df['credit_day_overdue']>=365) & (repayanalysis_df['credit_day_overdue']<=730)]

#Change perecents according to requirements***********************
percents=[0.00,0.01,0.03,0.06,0.12,0.30]

repayanalysis_df['Percents_interest_charge']=np.select(conditions,percents,default=0.50)
repayanalysis_df['Interest_charge']=repayanalysis_df.Percents_interest_charge*repayanalysis_df.amt_credit_sum_overdue

def preditpayment(r):
    count1=count2=count3=count4=totalcount=amt_due1=amt_due2=amt_due3=amt_due4=int_due1=int_due2=int_due3=int_due4=0
    visual3=[]
    for data in r:
        if data[0]==choice[0] and data[3]!=0:
            count1=count1+1
            amt_due1=amt_due1+data[3]
            int_due1=int_due1+data[4]
            visual3.append(data)
        elif data[0]==choice[1] and data[3]!=0:
            count2=count2+1
            amt_due2=amt_due2+data[3]
            int_due2=int_due2+data[4]
            visual3.append(data)
        elif data[0]==choice[2] and data[3]!=0:
            count3=count3+1
            amt_due3=amt_due3+data[3]
            int_due3=int_due3+data[4]  
            visual3.append(data)
        elif data[0]==choice[3] and data[3]!=0:
            count4=count4+1
            amt_due4=amt_due4+data[3]
            int_due4=int_due4+data[4]
            visual3.append(data)

    totalcount=np.divide(100,(count1+count2+count3+count4))
    
    print('\033[1m' +"***********Predict clients repayment abilities according to catagories**************************************"+ '\033[0m')
    print("The total number of "+choice[0]+ " need to repay credit are {} with {}% with total amount due ${} and total interest due ${}".format(count1,round((count1*totalcount),2),round((amt_due1),2),round(int_due1),2))
    print("The total number of "+choice[1]+ " need to repay credit are {} with {}% with total amount due ${} and total interest due ${}".format(count2,round((count2*totalcount),2),round((amt_due2),2),round(int_due2),2))
    print("The total number of "+choice[2]+ " need to repay credit are {} with {}% with total amount due ${} and total interest due ${}".format(count3,round((count3*totalcount),2),round((amt_due3),2),round(int_due3),2))
    print("The total number of "+choice[3]+ " need to repay credit are {} with {}% with total amount due ${} and total interest due ${}\n".format(count4,round((count4*totalcount),2),round((amt_due4),2),round(int_due4),2))


    visual_df3 = pd.DataFrame(visual3, columns = ['Category','amt_credit_sum','credit_day_overdue','amt_credit_sum_overdue','Interest_charge'])
    g = sns.lmplot(x="amt_credit_sum_overdue", y="Interest_charge", hue="Category",
               truncate=True, height=8, data=visual_df3)
# Use more informative axis labels than are provided by default
    g.set_axis_labels("Credit Amount ", "Interest Amount")

#***********Predict clients repayment abilities according to catagories**************************************

repaymentanalysis=(repayanalysis_df[['code_gender','amt_credit_sum','credit_day_overdue','amt_credit_sum_overdue','Interest_charge']]).values
choice=(['F','M','',''])
preditpayment(repaymentanalysis)

repaymentanalysis=(repayanalysis_df[['name_income_type','amt_credit_sum','credit_day_overdue','amt_credit_sum_overdue','Interest_charge']]).values
choice=(['Working','State servant','Commercial associate','Pensioner'])
preditpayment(repaymentanalysis)


# Save in Excel
#writer = pd.ExcelWriter('repaymentanalysis.xlsx', engine='openpyxl')
#repayanalysis_df.to_excel( excel_writer = writer, sheet_name = 'repayment' , header = True, index = True )
#writer.save()/*

"""## Getting Started

The document you are reading is a  [Jupyter notebook](https://jupyter.org/), hosted in Colaboratory. It is not a static page, but an interactive environment that lets you write and execute code in Python and other languages.

For example, here is a **code cell** with a short Python script that computes a value, stores it in a variable, and prints the result:
"""

seconds_in_a_day = 24 * 60 * 60
seconds_in_a_day

"""To execute the code in the above cell, select it with a click and then either press the play button to the left of the code, or use the keyboard shortcut "Command/Ctrl+Enter".

All cells modify the same global state, so variables that you define by executing a cell can be used in other cells:
"""

seconds_in_a_week = 7 * seconds_in_a_day
seconds_in_a_week

"""For more information about working with Colaboratory notebooks, see [Overview of Colaboratory](/notebooks/basic_features_overview.ipynb).

## More Resources

Learn how to make the most of Python, Jupyter, Colaboratory, and related tools with these resources:

### Working with Notebooks in Colaboratory
- [Overview of Colaboratory](/notebooks/basic_features_overview.ipynb)
- [Guide to Markdown](/notebooks/markdown_guide.ipynb)
- [Importing libraries and installing dependencies](/notebooks/snippets/importing_libraries.ipynb)
- [Saving and loading notebooks in GitHub](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb)
- [Interactive forms](/notebooks/forms.ipynb)
- [Interactive widgets](/notebooks/widgets.ipynb)
- <img src="/img/new.png" height="20px" align="left" hspace="4px" alt="New"></img>
 [TensorFlow 2 in Colab](/notebooks/tensorflow_version.ipynb)

### Working with Data
- [Loading data: Drive, Sheets, and Google Cloud Storage](/notebooks/io.ipynb) 
- [Charts: visualizing data](/notebooks/charts.ipynb)
- [Getting started with BigQuery](/notebooks/bigquery.ipynb)

### Machine Learning Crash Course
These are a few of the notebooks from Google's online Machine Learning course. See the [full course website](https://developers.google.com/machine-learning/crash-course/) for more.
- [Intro to Pandas](/notebooks/mlcc/intro_to_pandas.ipynb)
- [Tensorflow concepts](/notebooks/mlcc/tensorflow_programming_concepts.ipynb)
- [First steps with TensorFlow](/notebooks/mlcc/first_steps_with_tensor_flow.ipynb)
- [Intro to neural nets](/notebooks/mlcc/intro_to_neural_nets.ipynb)
- [Intro to sparse data and embeddings](/notebooks/mlcc/intro_to_sparse_data_and_embeddings.ipynb)

### Using Accelerated Hardware
- [TensorFlow with GPUs](/notebooks/gpu.ipynb)
- [TensorFlow with TPUs](/notebooks/tpu.ipynb)

## Machine Learning Examples: Seedbank

To see end-to-end examples of the interactive machine learning analyses that Colaboratory makes possible, check out the [Seedbank](https://research.google.com/seedbank/) project.

A few featured examples:

- [Neural Style Transfer](https://research.google.com/seedbank/seed/neural_style_transfer_with_tfkeras): Use deep learning to transfer style between images.
- [EZ NSynth](https://research.google.com/seedbank/seed/ez_nsynth): Synthesize audio with WaveNet auto-encoders.
- [Fashion MNIST with Keras and TPUs](https://research.google.com/seedbank/seed/fashion_mnist_with_keras_and_tpus): Classify fashion-related images with deep learning.
- [DeepDream](https://research.google.com/seedbank/seed/deepdream): Produce DeepDream images from your own photos.
- [Convolutional VAE](https://research.google.com/seedbank/seed/convolutional_vae): Create a generative model of handwritten digits.
"""