import os
from typing import Tuple
import pandas as pd

def grep_energy(prefix: str, csv_file: str = "energy_data.csv") -> Tuple[float, float]:
    """
    Extract energy and pressure data from OUTCAR files and save to CSV.

    This function reads energy and pressure values from VASP OUTCAR files in
    directories named Al{prefix} and AlMg{prefix}, computes differences, and
    saves them to a CSV file. It returns the mean and standard error of the
    energy differences.

    Args:
        prefix (str): Directory prefix for Al and AlMg folders (e.g., '666sym').
        csv_file (str, optional): Path to the output CSV file. Defaults to "energy_data.csv".

    Returns:
        Tuple[float, float]: Mean and standard error of the energy differences.
                             If no data is found, returns (nan, nan).

    Examples:
        >>> mean, error = grep_energy("666sym")
        >>> print(f"Mean: {mean}, Std Error: {error}")
    """
    data = []
    for i in range(10, 10001, 10):
        al_file = f"Al{prefix}/OUTCAR.{i}"
        almg_file = f"AlMg{prefix}/OUTCAR.{i}"
        
        if os.path.isfile(al_file) and os.path.isfile(almg_file):
            values = {'eal': None, 'pal': None, 'ealmg': None, 'palmg': None}
            for file, (e_key, p_key) in [(al_file, ('eal', 'pal')), (almg_file, ('ealmg', 'palmg'))]:
                with open(file, 'r') as rf:
                    for line in rf:
                        if "free  en" in line:
                            values[e_key] = float(line.split()[4])
                        elif "external pressure" in line:
                            parts = line.split()
                            if len(parts) > 3 and parts[3].replace('.', '', 1).isdigit():
                                values[p_key] = float(parts[3])
            
            if all(v is not None for v in values.values()):
                data.append({
                    'ealmg': values['ealmg'],
                    'eal': values['eal'],
                    'energy_diff': values['ealmg'] - values['eal'],
                    'pal': values['pal'],
                    'palmg': values['palmg'],
                    'pressure_diff': values['pal'] - values['palmg']
                })
    
    # Write data to CSV (empty DataFrame with columns if no data)
    columns = ['ealmg', 'eal', 'energy_diff', 'pal', 'palmg', 'pressure_diff']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(csv_file, index=False)
    
    # Return mean and standard error (nan if no data)
    return df['energy_diff'].mean(), df['energy_diff'].sem()

if __name__ == "__main__":
    mean, error = grep_energy("666sym")
    print(f"Mean: {mean}, Std Error: {error}")
