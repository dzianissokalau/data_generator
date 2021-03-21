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
print(df.head().to_markdown())