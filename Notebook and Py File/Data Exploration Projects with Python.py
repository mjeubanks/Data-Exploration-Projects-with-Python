#!/usr/bin/env python
# coding: utf-8

# # Data Exploration Projects with Python

# Foreword:
# 
# When you find a data set in the wild and out in the open or the internet, you will likely understand the dataset by itself due to:
# 
# - There will be column names that you don't understand.
# - Numerical Units aren't specified.
# - Values such as item numbers, PO numbers or SKU numbers have an unfamiliar nomeclature.
# - Some values are a calculation or dependent on other features and must match the inputs of other columns.
# - Columns contain digit values that aren't numerical and should be classified as a catagorical such as social security numbers or employee ID numbers.
# 
# Always look, request or ask for an explanation file which can contain the above information. An explanation file would like something like this:
# 
# ![image.png](attachment:image.png)
# 
# The goal of this notebook is to demonstrate the common functions/tools/revisions and ways of thinking when it comes to exploring the data. Most importantly, data exploring should be fun! You're creativity will help guide your exploration.
# 
# __IMPORTANT NOTE: The data set for 'EXAMPLE 1 - New York City Trees' can be downloaded at https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh__

# ## EXAMPLE 1 - New York City Trees

# In[59]:


import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
plt.style.use('ggplot')


# In[5]:


tree_census = pd.read_csv(r"2015_Street_Tree_Census_-_Tree_Data.csv") #Enter your path
tree_census.head(3)


# NOTE: There are so many columns that pandas doesn't display all of them (see the '...' symbol in columns).
# 
# Below will allow you to see all the columns

# In[9]:


pd.set_option('display.max_columns', None)
tree_census


# ### FILTER THE DATA WITH ONLY RELAVENT INFORMATION
# 
# You know must know the the purpose of studying the dataset or overall business objective to help decide which information is important and which information can be discarded.
# 
# The goal in this example is to understand the overall health of trees in New York City.

# Copy and pasting column names directly from `df.columns` makes it easier to delete names from coluns columns as it avoids errors in typos and/or incorrect format.

# In[11]:


tree_census.columns


# Below columns were considered irrelavent:
# 
# ['block_id', 'created_at', 'spc_common', 'spc_common', 'guards', 'user_type', 'address', 'postcode',
#        'zip_city', 'community board', 'borocode', 'borough', 'cncldist',
#        'st_assem', 'st_senate', 'nta', 'nta_name', 'boro_ct', 'state',
#        'latitude', 'longitude', 'x_sp', 'y_sp', 'council district',
#        'census tract', 'bin', 'bbl']

# In[13]:


tree_census_subset = tree_census[['tree_id','tree_dbh', 'stump_diam',
       'curb_loc', 'status', 'health', 'spc_latin', 'steward',
       'sidewalk','problems', 'root_stone',
       'root_grate', 'root_other', 'trunk_wire', 'trnk_light', 'trnk_other',
       'brch_light', 'brch_shoe', 'brch_other']]
tree_census_subset


# ### OBSERVE HOW MANY ROWS ARE NA
# 
# Note: Just because the values are na doesn't necessarily always mean it is wise to delete.
# 
# `df.isna().sum()`

# In[15]:


tree_census_subset.isna().sum()


# We notice that 'health', 'spc_latin', 'steward', 'sidewalk', 'problems' contain a significant quanity of values that are na.
# 
# Let's see how that data set looks with those na values:

# In[17]:


tree_census_subset[tree_census_subset['health'].isna()]


# ### UNDERSTAND THE TYPES OF DATA

# `df.dtypes` - states which values are numerical or catagorical
# 
# NOTE: Notice that tree_id is classified as numerical since it contains digit values. However, it is an ID number and should be considered a catagorical variables.

# In[22]:


tree_census_subset.dtypes


# ### LOOK FOR OUTLIERS

# `df.describe()` - summarizes the distribution of numerical values.
# 
# Observing the mean, max and std are a good way to gauge the risk of the dataset having outliers.

# In[23]:


tree_census_subset.describe()


# We notice that tree depth (tree_dbh) has a max of 450in but the mean is only 11in. This requires a further investigation by looking at the histogram.
# 
# NOTE: Just because bars are not visible on the chart does not mean there are no values within that bin. You can tell how many bins there are by the x-axis.

# In[26]:


tree_census_subset.hist(bins=60, figsize =(20,10) )


# Let's eyeball the histogram and remove all points that aren't visible on the histogram. Let's see how the data looks for the 'outliers'.

# In[30]:


big_trees = tree_census_subset[tree_census_subset['tree_dbh'] > 50]
big_trees


# In[32]:


big_trees[['tree_id', 'tree_dbh']].plot(kind='scatter', x='tree_id', y='tree_dbh')


# In[ ]:


Let's repeat this excecise for tree stump


# In[35]:


tree_stump = tree_census_subset[tree_census_subset['stump_diam'] > 50]
tree_stump


# In[36]:


tree_stump[['tree_id', 'stump_diam']].plot(kind='scatter', x='tree_id', y='stump_diam')


# ### Further Exploration

# Now comes the fun part, take your time to explore the data to better understand what you are looking at. Look for 'eyeball' rough estimatations of distributions, correlations or other outliers.
# 
# Below is an example of things to look at:
# 
# Looking at the most common trees

# In[39]:


tree_census_subset['spc_latin'].value_counts().plot(kind='bar')


# Assume you're unfamiliar with what the column 'steward', 'sidewalk', 'curb_loc' exactly entails by looking at the data. So you want to know all the possible values:
# 
# `df['ColumnName'].value_counts()`

# In[44]:


tree_census_subset['steward'].value_counts()


# In[45]:


tree_census_subset['sidewalk'].value_counts()


# In[46]:


tree_census_subset['curb_loc'].value_counts()


# In[49]:


stumps = tree_census_subset[tree_census_subset['status']=='Stump']
stumps


# When there are multiple columns with the same assigned responses. It's good to visually see the value counts of the responses. 

# In[56]:


tree_problems = tree_census_subset[['root_stone',
       'root_grate', 'root_other', 'trunk_wire', 'trnk_light', 'trnk_other',
       'brch_light', 'brch_shoe', 'brch_other']]
tree_problems


# In[57]:


tree_problems.apply(pd.Series.value_counts)


# ### CONCLUSION
# 
# This is a good example a data exploration prior to data cleaning. The scatterplots and bar charts were necessary to be more familiar with the data prior to more in-depth data cleaning. Sometimes data exploration is key in preventing yourself from wrong formatting columns and accurately interpetting relationships between features.

# ## EXAMPLE 2 - Rollercoasters

# ### Data Understanding
# - `df.shape`
# 
# - `df.head()`
# 
# - `df.tail()`
# 
# - `df.dtypes`
# 
# - `df.describe()`
# - `df.columns`
# 

# In[86]:


df = pd.read_csv("coaster_db.csv")
data = df.copy() 
# 'data' will be used as a backup in case we make any revisions 
# to the database that can't be reversed.


# We see that there are 56 columns (features) and 1087 rows of data:

# In[84]:


df.shape


# We can get a general idea of how the the table looks and establish what the values look like.
# 
# One thing to notice is that the column 'Speed' and 'Height' are string values instead of numerical values. This can be deemed undesirable for certain methods of Machine Learning so it's likely something that would have to be revised in preparation for advanced statistical methods.

# In[63]:


df.head(3)


# There are a lot of columns, so let's see what kind of features the data has:

# In[68]:


df.columns


# Now that we know the feature names. Let's see what kind of data it is (catagorical or numerical), this will give us a rough estimate on the type of data visualizaton/manipulation we will be able to do.

# In[80]:


df.dtypes


# We can immediately look at all the features with numerical values using the __describe__ tool. This is a good gauge to look at the distribution of data and look at the min/max value hypothesize if there are outliers.

# In[70]:


df.describe()


# ### Data Preparation
# - Drop irrelevant columsn and rows
# - Identify duplicate columns
# - Rename Columns
# - Feature Creation

# Based on looking at the data values, data columns and data distrubution. Let's remove any data we subjectively think aren't valuable.

# #### DROP COLUMNS

# There's two ways to elminate columns: filter the current dataframe by only including desired columns or filter the current dataframe by dropping undesired columns (there's a subtle difference).
# 
# For the 'dropping' method - here's the code:

# In[89]:


#axis = 1 let's the code know we are dropping by column and not by row.

#df.drop(['Opening date'], axis=1) #<---drops one column
#df.drop(['Theme'], axis=1) #<---drops multiple columns


# We're going to use the 'including' method:

# In[90]:


df = df[['coaster_name','Location','Status', 'Manufacturer','year_introduced',
         'latitude', 'longitude', 'Type_Main','opening_date_clean','speed_mph',
        'height_ft','Inversions_clean', 'Gforce_clean']]


# The original shape was (1087, 56) and the new shape is below:

# In[92]:


df.shape


# #### MODIFY DATA TYPE

# We saw in `info()` that __opening_date_clean__ was an object time. We should convert that to a datetime object:

# In[98]:


print(df['opening_date_clean'].dtype)

df['opening_date_clean'] = pd.to_datetime(df['opening_date_clean'])

print(df['opening_date_clean'].dtype)


# We don't want to do it in this circumstance, but below are two methods of converting __year_introduced__ to a numercial value.

# In[109]:


#pd.to_numeric(df['year_introduced'])
#int(df['year_introduced']) #<--sometimes will get errors due to nan values


# #### RENAME COLUMNS
# 
# Not always necessary to rename columns. But each organizaton could have a preference in column nomeclature to keep all cleaned datasets unified. 

# In[111]:


df = df.rename(columns={'coaster_name': 'Coaster_Name',
                   'year_introduced': 'Year_Introduced',
                  'opening_date_clean': 'Opening_Date_Clean',
                  'speed_mph': 'Speed_MPH',
                  'height_ft': 'Height_Ft',
                  'Inversions_clean': 'Inversions_Clean',
                  'Gforce_clean': 'Gforce_Clean'})

df.head(3)


# #### IDENTIFY MISSING VALUES
# - `.isna().sum()`
# - `.duplicated()`
# - `.query()`

# In[112]:


df.isna().sum()


# #### IDENTIFY DUPLICATED VALUES
# `df.duplicated()`
# 
# The below line of code demonstrates that there are no duplicates in the data as a whole. But sometimes it's valuable to see if there are duplicate values on a row/feature level.

# In[116]:


df.loc[df.duplicated()]


# We can see below that certain coasters are the same but the difference is simply the year introduced.

# In[118]:


df.loc[df.duplicated(subset=['Coaster_Name'])].head()


# In[122]:


df.query('Coaster_Name == "Crystal Beach Cyclone"')


# In this scenario, we're only concerned with unique values for each Coaster so we're going to drop psuedo-duplicates.

# '~' is the symbol for 'not'

# In[131]:


df = df.loc[~df.duplicated(subset=['Coaster_Name', 'Location', 'Opening_Date_Clean'])].reset_index(drop=True)
df.shape


# ### Feature Understanding
# 
# -Plotting feature distributions
# 
# -histogram
# 
# -kde
# 
# -Boxplot

# __NOTE__: This example will only be performed on one feature in this notebook. However, in reality this process will be repeated all 13 features.
# 
# We can use `value_counts()` to see how frequent unique values occur. The below line of code let's us know that 1999 introduced the most roller coasters.

# In[135]:


df['Year_Introduced'].value_counts()


# We will make a plot to show the top 10 years introduced.
# 
# NOTE:
#     
# Saving plot as 'ax' saves diagram as a matplotlib. This will allow us to add additional information to it.

# In[141]:


ax = df['Year_Introduced'].value_counts().head(10).plot(kind='bar', title='Top 10 Years Introduced')
ax.set_xlabel('Year Introduced')
ax.set_ylabel('Counts')


# We're going to now look at Speed. But it's important to observe that it was not common to document speed on coasters built in 1800s/early 1900s which is why there will be some null values. This is an important example as to it is important to understand the dataset and read the explanation file.

# In[144]:


df.head(3)


# It's easy to see that the most common speed is 50mph

# In[149]:


ax = df['Speed_MPH'].plot(kind='hist', bins=20, title='Coaster Speed (mph)')
ax.set_xlabel('Speed (mph)')


# An alternative plot is a density plot

# In[151]:


ax = df['Speed_MPH'].plot(kind='kde',title='Coaster Speed (mph)')
ax.set_xlabel('Speed (mph)')


# ### Feature Relationships
# - Scatterplot
# - Heatmap
# - Pairplot
# - Group By
# 
# Rather than know the distribution of each feature, it's equally important to know the feature's correlations (or lack thereof).
# 
# Without formal Linear Regression, it is clear there is a linear relationship between Speed and Height:

# In[153]:


df.plot(kind='scatter', x='Speed_MPH', y='Height_Ft', title= 'Coaster Speed vs. Height')
plt.show()


# Seaborn as different features than matplotlib. Such as adding complexity to the graphs by using hue as a 3rd plotting variable.

# In[158]:


sns.scatterplot(x='Speed_MPH', y='Height_Ft', hue='Year_Introduced', data=df)


# Pairplot is an amazing why to plot multiple variables along an x and y axis. It's one of my favorite tools.

# In[165]:


sns.pairplot(df, hue='Type_Main', vars=['Year_Introduced', 'Speed_MPH', 'Height_Ft', 'Inversions_Clean', 'Gforce_Clean'])


# In[162]:


df.columns


# Let's look at correlation between the values.

# In[169]:


df_corr = df[['Year_Introduced','Speed_MPH', 'Height_Ft','Inversions_Clean','Gforce_Clean' ]].dropna().corr()

df_corr


# A heatmap is perfect for plotting the correlation.

# In[170]:


sns.heatmap(df_corr, annot=True)


# ### Ask a Question About the Data
# 
# Now that you know your data. It's a good time to brainstorm questions and see if your data can answer that question. If not, that's ok! Questions know the limitations of your current dataset and provide guidance on if it's worth collecting more data.
# 
# Below is an example of a question that may come up:

# #### What are the locations with the fastest roller coasters (min of 10)?
# 
# The below plot can answer that question!

# In[181]:


ax = df.query('Location != "Other"').groupby('Location')['Speed_MPH'].agg(['mean','count']).query('count >= 10').sort_values('mean').plot(kind='barh', figsize=(12,5), title='Average Coaster Speed by Location')
ax.set_xlabel('Average Coaster Speed')


# ### CONCLUSION
# 
# The first example was a scenario of a prelminary data exploration prior to data cleaning; this scenario is when data exploration comes _after/in-parallel_ to data cleaning.
# 
# This data is perfect for advanced data analysis; we've shown scatterplots, density plots, histograms, heatmaps, pairplots. That's even before Machine Learning and Deep Learning tools.

# ## EXAMPLE 3 - World Population
# 
# If you've reviewed and studied the first two examples, you're now a pro so we're going to limit the commentary in this excerise to eliminate redundancy.
# 

# In[191]:


df = pd.read_csv(r"world_population.csv") #Enter your path
df.head(3)


# In[190]:


pd.set_option('display.float_format', lambda x: '%.2f' % x)


# In[192]:


df.info()


# In[193]:


df.describe()


# In[194]:


df.isnull().sum()


# This appears to be a a small dataset so it is recommended to be conservative with deleting rows with null values.

# In[196]:


df.shape


# `df.nunique()` is diffrent than `df.unique()`in the sense that the latter is used to display all the unique values for a specific column. The former will give you a count of all the unique values. 
# 
# It makes sense that population has a substantial quantity of unique values since it's expected to be a continous variable and Continent makes sense to have a small quantity of unique values.

# In[201]:


df.nunique()


# `df.sort_values(by='Column_name')` - sorts values.

# In[204]:


df.sort_values(by='2022 Population', ascending=False).head()


# In[207]:


df_corr = df.corr()
df_corr


# In[213]:


sns.heatmap(df_corr, annot=True)
plt.rcParams['figure.figsize'] = (20, 20)
plt.show()


# Are there certain populations growing at a significantly faster rate?

# In[215]:


df.groupby('Continent').mean()


# `df['Column_Name'].str.contains('String_value')`

# In[216]:


df[df['Continent'].str.contains('Oceania')]


# In[228]:


df2 = df.groupby('Continent')[['1970 Population',
       '1980 Population', '1990 Population', '2000 Population',
       '2010 Population', '2015 Population', '2020 Population',
       '2022 Population']].mean().sort_values(by='2022 Population', ascending = False)
df2


# In[229]:


df2.plot()


# In[230]:


df3 = df2.transpose()
df3


# In[231]:


df3.plot()


# In[232]:


df.boxplot(figsize=(20,10))


# In[234]:


df.plot(kind='box') #alternative method for boxplot


# `df.select_dtypes(include='datatype')` - This allows you to filter an entire dataset to include only the features that have your desired datatype.

# In[236]:


df.select_dtypes(include='number')


# In[237]:


df.select_dtypes(include='object')


# In[238]:


df.select_dtypes(include='float')


# ### CONCLUSION
# 
# Now that you've explored that data and are confident that the table contains all the information you need. The next step is to clean the data by fixing or removing incorrect, corrupted, incorrectly formatted, duplicate, or incomplete data within a dataset.
