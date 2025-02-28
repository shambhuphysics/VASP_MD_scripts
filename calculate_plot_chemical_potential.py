import numpy as np
import matplotlib.pyplot as plt
import math

def calculate_and_plot_free_energy(lambda0_data, lambda1_data):
    """
    Calculate the free energy integral and plot piecewise linear functions using thermodynamic integration.

    This function computes the integral of two linear functions representing energy states at Lambda=0 and Lambda=1,
    determining their intersection point and integrating each segment over its respective domain within [0, 1].
    The method follows the thermodynamic integration principle to estimate free energy differences.

    Parameters
    ----------
    lambda0_data : list of float
        Energy data at Lambda=0 containing four elements:
        - [0]: Average energy (<E>_0)
        - [1]: Uncertainty in average energy
        - [2]: Energy fluctuation term (-beta/2 * <dE^2>_0)
        - [3]: Uncertainty in fluctuation term
    lambda1_data : list of float
        Energy data at Lambda=1 containing four elements:
        - [0]: Average energy (<E>_1)
        - [1]: Uncertainty in average energy
        - [2]: Energy fluctuation term (-beta/2 * <dE^2>_1)
        - [3]: Uncertainty in fluctuation term

    Returns
    -------
    None
        Prints the intersection point (if within [0, 1]), the calculated integral with uncertainty,
        and displays a plot of the piecewise function and integrated area.

    Theory
    ------
    The integral represents the free energy difference and is computed using two linear functions:
    - y_0(x) = m_0 * x + c_0 (for Lambda=0)
    - y_1(x) = m_1 * x + c_1 (for Lambda=1)
    where:
    - m_0 = 2 * lambda0_data[2], c_0 = lambda0_data[0]
    - m_1 = 2 * lambda1_data[2], c_1 = lambda1_data[0] - 2 * lambda1_data[2]

    Steps:
    1. **Intersection Point (x_c)**:
       - Calculated as: x_c = (c_0 - c_1) / (m_1 - m_0)
       - If x_c is not in [0, 1], the integral is approximated as the average of <E>_0 and <E>_1.

    2. **Integral Calculation**:
       - If x_c in [0, 1]:
         - For y_0 from 0 to x_c:
           ∫[0,x_c] (m_0 * x + c_0) dx = (m_0 * x_c²)/2 + c_0 * x_c
         - For y_1 from x_c to 1:
           ∫[x_c,1] (m_1 * x + c_1) dx = (m_1 * (1 - x_c²))/2 + c_1 * (1 - x_c)
         - Total integral I = integral_y0 + integral_y1
       - The integral represents the area under the piecewise linear function, corresponding to the
         free energy difference between the two states.

    3. **Uncertainty**:
       - Propagates errors from input uncertainties through the intersection and integral calculations.

    Visualization
    -------------
    - Plots y_0 and y_1 as blue and green lines, respectively
    - Marks the intersection point in red
    - Shades the integrated area in orange
    - Includes a grid and legend for clarity

    Examples
    --------
    >>> lambda0 = [2.93809314, 0.00598791, -0.08426016, 0.00364061]
    >>> lambda1 = [2.76668567, 0.00611661, -0.08411737, 0.003613]
    >>> calculate_and_plot_free_energy(lambda0, lambda1)
    """
    # Print input data in a standardized format
    print("Input Data Summary:")
    print("Lambda=0:")
    print(f"  Average Energy: {lambda0_data[0]:.6f} ± {lambda0_data[1]:.6f}")
    print(f"  Fluctuation Term: {lambda0_data[2]:.6f} ± {lambda0_data[3]:.6f}")
    print("Lambda=1:")
    print(f"  Average Energy: {lambda1_data[0]:.6f} ± {lambda1_data[1]:.6f}")
    print(f"  Fluctuation Term: {lambda1_data[2]:.6f} ± {lambda1_data[3]:.6f}")
    print("-" * 50)

    # Extract values with meaningful names
    e0_avg, e0_err, e0_fluc, e0_fluc_err = lambda0_data
    e1_avg, e1_err, e1_fluc, e1_fluc_err = lambda1_data
    
    # Calculate line parameters
    y0_intercept = e0_avg
    y0_intercept_err = e0_err
    y1_intercept = e1_avg - 2 * e1_fluc
    y1_intercept_err = math.sqrt(e1_err**2 + 4 * e1_fluc_err**2)
    
    y0_slope = 2 * e0_fluc
    y0_slope_err = 2 * e0_fluc_err
    y1_slope = 2 * e1_fluc
    y1_slope_err = 2 * e1_fluc_err

    # Calculate intersection point
    x_intersect = (y0_intercept - y1_intercept) / (y1_slope - y0_slope)
    
    if not 0 <= x_intersect <= 1:
        integral = (e0_avg + e1_avg) / 2
        integral_err = math.sqrt(e0_err**2 + e1_err**2) / 2
        print(f"x_intersect = {x_intersect:.4f}, no intercept in [0, 1]")
        print(f"Integral = {integral:.4f} ± {integral_err:.4f}")
    else:
        # Calculate uncertainty in intersection
        x_intersect_err = math.sqrt(
            (y0_intercept_err**2 + y1_intercept_err**2) / (y1_slope - y0_slope)**2 +
            (y0_intercept - y1_intercept)**2 / (y1_slope - y0_slope)**2 * (y1_slope_err**2 + y0_slope_err**2)
        )
        
        # Calculate integral
        integral_y0 = (y0_slope * x_intersect**2) / 2 + y0_intercept * x_intersect
        integral_y1 = (y1_slope * (1 - x_intersect**2)) / 2 + y1_intercept * (1 - x_intersect)
        integral = integral_y0 + integral_y1
        
        # Calculate integral uncertainty
        integral_err = math.sqrt(
            e1_err**2 + y1_slope_err**2/4 + x_intersect_err**2 * (y0_intercept - e1_avg + y1_slope)**2 +
            x_intersect**2 * (y0_intercept_err**2 + e1_err**2 + y1_slope_err**2) +
            x_intersect**2 * x_intersect_err**2 * (y0_slope - y1_slope)**2 +
            x_intersect**4 / 4 * (y0_slope_err**2 + y1_slope_err**2)
        )
        print(f"Intersection at x = {x_intersect:.4f} ± {x_intersect_err:.4f}")
        print(f"Integral = {integral:.4f} ± {integral_err:.4f}")

    return integral, integral_err

    # Plotting
    x = np.linspace(0, 1, 500)
    y = np.where(x <= x_intersect, 
                 y0_slope * x + y0_intercept, 
                 y1_slope * x + y1_intercept)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y0_slope * x + y0_intercept, 'b-', label=r"$y_0 = m_0 x + c_0$")
    plt.plot(x, y1_slope * x + y1_intercept, 'g-', label=r"$y_1 = m_1 x + c_1$")
    plt.scatter(x_intersect, y0_slope * x_intersect + y0_intercept, c='r', 
                label=f"Intersection at x = {x_intersect:.3f}")
    plt.fill_between(x, y, color='orange', alpha=0.3, label="Integral Area")
    
    plt.xlabel("Lambda")
    plt.ylabel("Energy")
    plt.title("Free Energy Integration")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    lambda0 = [2.93809314, 0.00598791, -0.08426016, 0.00364061]
    lambda1 = [2.76668567, 0.00611661, -0.08411737, 0.003613]
    calculate_and_plot_free_energy(lambda0, lambda1)
