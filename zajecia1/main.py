import pandas
import matplotlib.pyplot as plt
import numpy as np

def data_loader(PATH: str) -> pandas.DataFrame:
    data = pandas.read_excel(PATH)
    return data

def group_splitter(data: pandas.DataFrame, group_name: str) -> pandas.DataFrame:
    data_group = data.groupby(group_name)
    return data_group

def LOQ():
    pass

def wartosci_odstajace():
    pass

def stats(data: pandas.DataFrame, conv_to_csv: bool = False):
    '''
    mean, median, std, min, max, LOQ
    '''

    columns = data.columns
    
    for column in columns:
        if type(data[column][0]) == str:
            columns = columns.drop(column)
            print(f'Removed {column}')

    _columns = ['Column name']
    _mean = ['Mean']
    _median = ['Median']
    _std = ['STD']
    _min = ['Min value']
    _max = ['Max value']
    for column in columns:
        _columns = np.append(_columns, column)
        _mean = np.append(_mean, data[column].mean())
        _median = np.append(_median, data[column].median())
        _std = np.append(_std, data[column].std())
        _min = np.append(_min, data[column].min())
        _max = np.append(_max, data[column].max())


    stat = [_columns, _mean, _median, _std, _min, _max]

    if conv_to_csv:
        stat = pandas.DataFrame(stat)
        stat.to_csv('stat.csv')
    return stat

def missing_values(data: pandas.DataFrame):
    '''
    data: pandas.DataFrame - data to check for missing values

    prints out columns with missing values
    '''
    miss = 0
    for column in data.columns:
        for val in data[column]:
            if val == 0:
                miss += 1
        if miss != 0:
            print(f'Column: {column} has {miss} missing values')
        miss = 0
    
    

def OALGB():
    PATH_OALGB = 'Dane_OALGB_Kwasy.xlsx'

    data = data_loader(PATH=PATH_OALGB)
    groups = data['Group'].unique()

    groupped_data = {}

    for group in groups:
        groupped_data[group] = data[data['Group'] == group]

    missing_values(data)
    print(stats(data))

def EGGPLANT():
    PATH_EGGPLANT = 'Dane_Eggplants_Percent.xlsx'

    data = data_loader(PATH=PATH_EGGPLANT)

    missing_values(data)
    print(stats(data, conv_to_csv=True))


if __name__=='__main__':
    ## OALGB
    OALGB()
    ## EGGPLANT
    EGGPLANT()


