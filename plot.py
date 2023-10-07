###### LIBRARIES
import random, time
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
from divide_and_conquer_merge import *


###### FUNCTIONS
def generate_random_points(num_points):
    """
    Generate random 2D points based on inputed number of points

    Args:
        num_points (int): The size of list of random 2D points
    
    Returns:
        list: A list of (x, y) points of size num_points
    """
    return [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(num_points)]


def measure_time(func, *args):
    """
    Measures time of algorithm func(*args).

    Args:
        func (callable): The function to be timed
        *args: Variable arg to pass to the function
    
    Returns:
        float: Time taken, in seconds
    """
    start_time = time.time()
    func(*args)
    end_time = time.time()
    return end_time - start_time


def plot_data_log_log(dataset_sizes, times):
    """
    Plot execution times against dataset sizes on a log-log scale, and compare with theoretical O(n log n) times.

    Args:
        dataset_sizes (list): List of execution times
        times (list): List of execution times for each dataset size.
    """

    log_dataset_sizes = np.log(dataset_sizes)
    log_times = np.log(times)

    # Linear regression
    slope, intercept, r_value, p_value, std_err = linregress(log_dataset_sizes, log_times)
    fit_times = slope * log_dataset_sizes + intercept

    # Compute the theoretical O(n log n) times
    theoretical_times = [n * np.log(n) for n in dataset_sizes]

    # Normalize the theoretical times to fit on the plot
    normalization_factor = times[5] / theoretical_times[5]  # Use an arbitrary index, like 5, for normalization
    normalized_theoretical_times = [time * normalization_factor for time in theoretical_times]

    plt.figure(figsize=(10, 6))
    plt.loglog(dataset_sizes, times, 'o', label='Experimental Data')
    plt.loglog(dataset_sizes, normalized_theoretical_times, 'g-', label='Theoretical O(n log n): Slope ≈ 1')
    plt.loglog(dataset_sizes, np.exp(fit_times), 'r--', label=f'Fitted Line: Slope = {slope:.2f}')
    plt.xlabel('Log of Number of Data Points')
    plt.ylabel('Log of Execution Time')
    plt.title('Performance of D&C Algorithm on Log-Log Scale')
    plt.legend()
    plt.grid(True)
    plt.show()


##### DRIVER CODE
if __name__ == '__main__':
    powers = np.linspace(1, 6, 10)  # Create 10 points between 1 and 6
    dataset_sizes = [int(10**p) for p in powers]  # Raise 10 to each power

    times = []
    for size in dataset_sizes:
        points = generate_random_points(size)
        elapsed_time = measure_time(convex_hull, points)
        times.append(elapsed_time)
        print(f"Size: {size}, Time: {elapsed_time} seconds")
    
    plot_data_log_log(dataset_sizes, times)
