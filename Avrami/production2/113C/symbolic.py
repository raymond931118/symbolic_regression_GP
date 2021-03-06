from gplearn.genetic import SymbolicRegressor
from sklearn.utils.random import check_random_state
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit
import sys

files = ['113C_mod.csv']

for filename in files:
    print('')
    print(filename)
    print('')
    # hyperparameters
    Ly_def = [True, False]                       # whether we use Y = y_data or Y = 1 - y_data
    Lscale_X = [10.]
    Lpop_size = [2000, 5000]                # generations = 100,000 / pop_size
    Ltour_factor = [100, 500]                 # tour_size = pop_size / tour_factor
    Lpars_coeff = [0.001, 0.005]

    # read data
    data = pd.read_csv(filename, sep=',', header=0)
    X_data = data.drop('Y', axis=1).values.astype(float)
    y_data = data['Y'].values.astype(float) / 100.
    

    for scale_X in Lscale_X:
        for y_def in Ly_def:
            if scale_X is not None: X_train = X_data * scale_X / max(X_data)
            else: X_train = X_data
            
            if y_def: y_train = 1 - y_data
            else: y_train = y_data

            for pop_size in Lpop_size:
                for tour_factor in Ltour_factor:
                    for pars_coeff in Lpars_coeff:
                        
                        #gen_size = int(50000 / pop_size)
                        gen_size = 20
                        tour_size = int(pop_size / tour_factor)
                        
                        print('')
                        print('')
                        line_format = '{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}'
                        print(line_format.format('filename', 'y_def', 'scale_X', 'pop_size', 'gen_size', 'tour_size', 'tour_factor', 'pars_coeff'))
                        print(line_format.format(filename, str(y_def), str(scale_X), str(pop_size), str(gen_size), str(tour_size), str(tour_factor), str(pars_coeff)))
                        print('')
                        print('')
                        
                        est_gp = SymbolicRegressor(population_size=pop_size, 
                                                   generations=gen_size, tournament_size=tour_size,
                                                   stopping_criteria=0.01, const_range=(-1, 1),
                                                   init_depth=(2, 6), init_method='half and half',
                                                   function_set=('add', 'sub', 'mul', 'neg', 'exp'), 
                                                   metric='rmse', parsimony_coefficient=pars_coeff,
                                                   p_crossover=0.7, p_subtree_mutation=0.1, p_hoist_mutation=0.05,
                                                   p_point_mutation=0.1, p_point_replace=0.05,
                                                   max_samples=1.0, warm_start=False, low_memory=True,
                                                   n_jobs=8, verbose=1, random_state=0)
                               
                        est_gp.fit(X_train, y_train.ravel())
                        print('printing the best individuals for the last 5 generations:')
                        for p in est_gp._best_programs[-5:]:
                            print(p)
                        print('Age of extinction, kill all.. Start new generation..')
                        print('')
                        sys.stdout.flush()
