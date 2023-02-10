import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

warnings.filterwarnings('ignore')


# '
# ;Function to add missing bathroom values
def bath_finder(x, y):
    if y == -1:
        if x >= 5:
            return x + 1
        elif x == 4 | x == 3:
            return x
        elif x == 1:
            return x
        else:
            return x - 1
    else:
        return y


# Function to add missing age values
def age_finder(x):
    if x == -1:
        return 0
    else:
        return x


# Removing Outliers
def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft > (m - st)) & (subdf.price_per_sqft <= (m + st))]
        df_out = pd.concat([df_out, reduced_df], ignore_index=True)
    return df_out


# Plotting scatter plot Area Vs. Price
def plot_scatter_chart(df, location):
    bhk2 = df[(df.location == location) & (df.bhk == 2)]
    bhk3 = df[(df.location == location) & (df.bhk == 3)]
    matplotlib.rcParams['figure.figsize'] = (15, 10)
    plt.scatter(bhk2.area, bhk2.price, color='blue', label='2 BHK', s=50)
    plt.scatter(bhk3.area, bhk3.price, marker='+', color='green', label='3 BHK', s=50)
    plt.xlabel("Total Square Feet Area")
    plt.ylabel("Price (Lakh Indian Rupees)")
    plt.title(location)
    plt.legend()


# Removing Outliers
def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk - 1)
            if stats and stats['count'] > 5:
                exclude_indices = np.append(exclude_indices,
                                            bhk_df[bhk_df.price_per_sqft < (stats['mean'])].index.values)
    return df.drop(exclude_indices, axis='index')


# 'static/files/clean_data.csv'

# Function to predict price
def predict_price(location, builder, sqft, bath, bhk, year, file_path):
    df1 = pd.read_csv(file_path)

    # Filling null with -1
    df1["bathroom"].fillna(-1, inplace=True)
    df1["age"].fillna(-1, inplace=True)
    df1["bath"] = df1.apply(lambda x: bath_finder(x["bhk"], x["bathroom"]), axis=1)
    df1['year'] = df1['age'].apply(age_finder)

    # Dropping old columns
    df1.drop(['bathroom', 'age'], axis=1, inplace=True)

    location_stats = df1['location'].value_counts(ascending=False)

    # Storing locations with less than 10 count
    location_stats_less_than_10 = location_stats[location_stats <= 10]

    # Grouping all less than 10 locations as other
    df1.location = df1.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)

    builder_stats = df1['builder'].value_counts(ascending=False)

    builder_stats = df1['builder'].value_counts(ascending=False)

    # Storing builders with less than 10 count
    builder_stats_less_than_10 = builder_stats[builder_stats <= 10]

    # Grouping all less than 10 builders as other
    df1.builder = df1.builder.apply(lambda x: 'other' if x in builder_stats_less_than_10 else x)

    # Removing Outliers
    df2 = df1[~(df1.area / df1.bhk < 300)]

    df2['price_per_sqft'] = df2['price'] * 100000 / df2['area']

    df3 = remove_pps_outliers(df2)
    df4 = remove_bhk_outliers(df3)

    df5 = df4.drop(['price_per_sqft'], axis='columns')

    # Changing text to binary data
    dummies1 = pd.get_dummies(df5.location)
    dummies2 = pd.get_dummies(df5.builder)

    df5.drop(['status'], axis=1, inplace=True)

    # Adding to the main dataframe
    df5 = pd.concat(((df5, dummies1, dummies2)), axis=1)

    # Dropping the columns whose value is changed
    df5.drop(['location', 'builder'], axis=1, inplace=True)

    X = df5.drop(['price'], axis=1)

    y = df5.price

    # Splitting for test and train

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

    # Implementing Liner Regression

    lr_clf = LinearRegression()
    lr_clf.fit(X_train, y_train)
    lr_clf.score(X_test, y_test)

    loc_index = np.where(X.columns == location)[0]
    builder_index = np.where(X.columns == builder)[0]

    x = np.zeros(len(X.columns))
    x[0] = sqft
    x[1] = bhk
    x[2] = bath
    x[3] = year
    if loc_index >= 0:
        x[loc_index] = 1
    if builder_index >= 0:
        x[builder_index] = 1

    return lr_clf.predict([x])[0]

# print(predict_price('Pammal', 'MC Foundation', 1000, 2, 2, 1 , 'static/files/clean_data.csv'))
