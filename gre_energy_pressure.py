import os
import pandas as pd

def grep_energy(csv_file="energy_data.csv"):
    """Extract energy/pressure from OUTCAR files and save to CSV with stats."""
    data = []
    for i in range(10, 10001, 10):
        al_file = f"Al666sym/OUTCAR.{i}"
        almg_file = f"AlMg666sym/OUTCAR.{i}"
        
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
            
            if all(v is not None for v in values.values()):   # checks fi all is treu
                data.append({
                    'ealmg': values['ealmg'],
                    'eal': values['eal'],
                    'energy_diff': values['ealmg'] - values['eal'],
                    'pal': values['pal'],
                    'palmg': values['palmg'],
                    'pressure_diff': values['pal'] - values['palmg']
                })
    
    # Use pandas to write data and compute stats
    if data:
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
