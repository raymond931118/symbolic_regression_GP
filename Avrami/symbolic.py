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

files = ['135C_curve30.csv', '119C_curve30.csv', '112C_curve30.csv', '102C_curve30.csv', '88C_curve30.csv', '43C_curve30.csv',
         '135C_origin.csv',  '119C_origin.csv',  '112C_origin.csv',  '102C_origin.csv',  '88C_origin.csv',  '43C_origin.csv',
         '135C_tail.csv',  '119C_tail.csv',  '112C_tail.csv',  '102C_tail.csv',  '88C_tail.csv',  '43C_tail.csv']
dirfolder = '../data/'

f = open("fit_results.txt", 'w')
f.close()
    
def avrami(t, k, n):
    return (1 - np.exp(-k * np.power(t, n)))

files = ['119C_gen.dat']
for filename in files:
    data = pd.read_csv(dirfolder+filename, sep=',', header=0)
    
    X_data = data.drop('Y', axis=1).values.astype(float)
    X_data = X_data * 10. / max(X_data)
    y_data = data['Y'].values.astype(float) / 100.
    
    stdscal = StandardScaler(with_mean=False, with_std=False)
    X_data = stdscal.fit_transform(X_data)
    y_data = stdscal.fit_transform(y_data.reshape(-1, 1))

    """
    plt.plot(X_data, y_data, 'b-', label='data')
    
    popt, pcov = curve_fit(avrami, X_data[:, 0], y_data[:, 0])
    y_pred = avrami(X_data, *popt)
    
    plt.plot(X_data, y_pred, 'r-', label='fit')
    plt.xlabel('t')
    plt.ylabel('y')
    plt.legend()
    plt.savefig(filename+'.png')
    plt.clf()
    
    f = open("fit_results.txt", "a")
    f.write("%s : " %filename)
    for var in popt:
        f.write(str(var) + '; ')
    f.write('\n')
    f.close()
    
    """    
    
    est_gp = SymbolicRegressor(population_size=5000, 
                               generations=10, tournament_size=50,
                               stopping_criteria=0.0, const_range=(0, 3),
                               init_depth=(2, 6), init_method='half and half',
                               function_set=('add', 'sub', 'mul', 'neg', 'exp'), 
                               metric='mse', parsimony_coefficient=0.01,
                               p_crossover=0.4, p_subtree_mutation=0.2, p_hoist_mutation=0.05,
                               p_point_mutation=0.3, p_point_replace=0.05,
                               max_samples=0.9, warm_start=False,
                               n_jobs=8, verbose=1, random_state=np.random.randint(0, 100))
                               
    est_gp.fit(X_data, y_data.ravel())
    print(est_gp._program)
