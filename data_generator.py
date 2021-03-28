import numpy as np
import pandas as pd
from datetime import datetime, timedelta




def map_indices(params):
    keys = params['categories']
    values = params['indices']
    
    mapper = {}
    
    for i in range(len(keys)):
        mapper[keys[i]] = values[i]
    
    return mapper



def get_indices(rows, params, data_dict):
    indices = np.ones(rows)
    
    for column in params['categorical'].keys():
        if 'indices' in params['categorical'][column].keys():
            mapper = map_indices(params['categorical'][column])
            
            indices_column = np.array([mapper[x] for x in data_dict[column]])
            
            indices = indices * indices_column
            
    return indices



def get_dates(rows, params, seed):
    # set randomiser
    rand = np.random.default_rng(seed)
    
    # if list of possible dates provided, use it
    if 'values' in params.keys():
        dates_list = params['values']
    
    # else build the list using start and end date
    else:
        # get start and end dates
        start = datetime.strptime(params['start'], '%Y-%m-%d')
        end = datetime.strptime(params['end'], '%Y-%m-%d')
        
        # get list of possible dates
        dates_list = [(start + timedelta(x)).strftime('%Y-%m-%d') for x in range((end - start).days + 1)]
    
    # use probabilities of values, if given
    if 'probs' in params.keys():
        dates = rand.choice(a=dates_list, p=params['probs'], size=rows)
    
    # else assume they have equal probability
    else:
        dates = rand.choice(a=dates_list, size=rows)
    
    return dates



def get_categorical(rows, params, seed):
    rand = np.random.default_rng(seed)
    
    # use probabilities of values, if given
    if 'probs' in params.keys():
        cat = rand.choice(a=params['categories'], p=params['probs'], size=rows)
    
    # else assume they have equal probability
    else:
        cat = rand.choice(a=params['categories'], size=rows)
        
    return cat



def get_values(rows, params, indeces, seed):
    rand = np.random.default_rng(seed)
    
    distribution = params['distribution']
    distribution_params = params['parameters'].copy()
    
    
    if params['indices'] == False:
        distribution_params_str = ', '.join([key + '=' + str(distribution_params[key]) for key in distribution_params.keys()])
        values = eval('rand.' + distribution + '(' + distribution_params_str + ', size={})'.format(rows))
    
    #elif distribution = 'binomial':
    else:
        distribution_params_str = ', '.join([key + '=' + str(distribution_params[key]) for key in distribution_params.keys()])
        values = eval('rand.' + distribution + '(' + distribution_params_str + ', size={})'.format(rows))
        values = values * indeces
    
    
    # round values
    if 'round' in params.keys():
        values = np.around(values, decimals=params['round'])

    # set everything lower than the min to the min
    if 'min' in params.keys():
        values[values < 1] = 1
    
    return values



def create_dataset(rows, params, seed=1):
    # create dict to sore data to
    data_dict = {}

    # create randomizer
    rand = np.random.default_rng(seed)
    
    # generate dates
    if 'dates' in params.keys():
        for key in params['dates'].keys():
            new_seed = rand.integers(low=1, high=100, size=1)[0]
            data_dict[key] = get_dates(rows=rows, params=params['dates'][key], seed=new_seed)

    # generate categorical observations
    if 'categorical' in params.keys():
        for key in params['categorical'].keys():
            new_seed = rand.integers(low=1, high=100, size=1)[0]
            data_dict[key] = get_categorical(rows=rows, params=params['categorical'][key], seed=new_seed)

    # use indices
    if 'categorical' in params.keys():
        indeces = get_indices(rows=rows, params=params, data_dict=data_dict)
    else:
        indeces = 1
            
    # generate values
    if 'values' in params.keys():
        for key in params['values'].keys():
            new_seed = rand.integers(low=1, high=100, size=1)[0]
            data_dict[key] = get_values(rows=rows, params=params['values'][key], indeces=indeces, seed=new_seed)
    
    # create data frame from dict
    data = pd.DataFrame(data_dict)
    
    # check dependencies
    if 'dependencies' in params.keys():
        for column in params['dependencies'].keys():
            for condition in params['dependencies'][column]:
                data.loc[eval("data['{from}'] {condition}".format(**condition)), column] = condition['value']
    
    return data    

