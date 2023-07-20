import pandas as pd

def get_route_factor_adjustments(streams: pd.DataFrame, 
                                 route_factors: pd.DataFrame, 
                                 radionucleide_cols: list[str]) -> pd.DataFrame:
    """
    Takes an input stream dataframe and the routing factors for volume, mass, and activity, 
    and multiplies the values in the stream table by the corresponding factors. This function
    returns a new dataframe (it does not modify the input data).
    """
    tmp = streams.merge(route_factors, left_on="Route Number", right_on="Route number", how="left", suffixes=("", " Factor"))

    route_adjusted_values = pd.DataFrame()
    route_adjusted_values["Volume"] = tmp["Volume"] * tmp["Volume Factor"]
    route_adjusted_values["Mass"] = tmp["Mass"] * tmp["Mass Factor"]

    for col in radionucleide_cols:
        route_adjusted_values[col] = tmp[col] * tmp["Activity"] 

    return route_adjusted_values


def get_route_number(stream_id: pd.Series) -> pd.Series:
     return stream_id.str.split("_").apply(lambda x: x[1]).astype(int)