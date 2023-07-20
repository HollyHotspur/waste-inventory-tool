import pandas as pd

def calculate_material_mass(streams: pd.DataFrame, non_hazardous_material_cols: list[str]) -> pd.DataFrame:
    """ 
    Take a streams dataframe, and a list of column names denoting weight percentages. The
    returned value should be a DataFrame with n columns (where n = number of weight percentage columns)
    with values equal to the weights for each material type.
    """
    material_masses = pd.DataFrame()
    
    df_material_sum = streams[non_hazardous_material_cols].sum(axis=1)/100
    normalised_masses = streams[non_hazardous_material_cols].div(df_material_sum, axis = 'index')
    material_masses[non_hazardous_material_cols] = normalised_masses.multiply(streams['Mass'], axis = 'index')/100 
    return material_masses


def calculate_haz_material_mass(streams: pd.DataFrame, hazardous_material_col: list[str]) -> pd.DataFrame:
    haz_masses = pd.DataFrame()

    haz_masses = streams[hazardous_material_col].multiply(streams['Mass'], axis = 'index')/100
    
    return haz_masses

