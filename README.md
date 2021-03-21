# Data Generator  

`data_generator` is a python module for generating synthetic datasets.  
The function uses `numpy` for generating arrays from known set of values, probabilities or distributions.  
The result is stored to `pandas` data frame.  
-----
Function `create_dataset` takes the following arguments:  
* **rows** (integer) - desired number of rows in the dataset;  
* **params** (dictionary) - dictionary of input parameters;  
* **seed** (integer) - random seed, 1 by default.  
  
  
### Example
```python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import data_generator


params = {
    'dates': {
        'date': {
            'start': '2021-02-01', 
            'end': '2021-02-14'
        }
    }, 
    'categorical': {
        'country': {
            'categories': ['UK', 'DE', 'FR', 'IT'], 
            'probs': [0.31, 0.27, 0.23, 0.19], 
            'indices': [0.98, 1.03, 0.99, 1.02]
        }, 
        'platform': {
            'categories': ['android', 'ios', 'web'], 
            'probs': [0.41, 0.29, 0.3], 
            'indices': [0.99, 1.06, 0.94]
        }
    }, 
    'values': {
        'payment': {
            'distribution': 'binomial', 
            'parameters': {
                'n': 1, 
                'p': 0.2
            }, 
            'indices': False
        }, 
        'amount': {
            'distribution': 'exponential', 
            'parameters': {
                'scale': 10
            }, 
            'indices': True, 
            'min': 1, 
            'round': 2
        }
    }, 
    'dependencies': {
        'amount': [
            {
                'from': 'payment', 
                'condition': '==0', 
                'value': 0
            }
        ]
    }
}


df = data_generator.create_dataset(rows=1000, params=params, seed=1)
```
  

### params  
Parameters `params` are created in json format.  
There are 3 types of data that can be created with the module:  
* date - for generating dates column. It can have the following parameters:  
    * start - start date in yyyy-mm-dd format (used if list of values is not specified)  
    * end - end date in yyyy-mm-dd format (used if list of values is not specified)  
    * values - list of possible dates in yyyy-mm-dd format  
    * probs - list of weights for every value in values, sum of weights should be equal to 1. Only used if values is specified.  
Example 1:  
```json
{
    "dates": {
        "date": {
            "start": "2021-03-01",
            "end": "2021-03-04"
        }
    }
}
```  
Example 2:  
```json
{
    "dates": {
        "date": {
            "values": ["2021-03-01", "2021-03-02", "2021-03-03", "2021-03-04"],
            "probs": [0.3, 0.25, 0.2, 0.25]
        }
    }
}
```  
  
* categorical  
* values   
   
There is dedicated section in `params` for every type of the data. All sections are optional, but at least one should be specified (otherwise no data will be created).    
There is an additional section for describing dependencies.  



## TBD