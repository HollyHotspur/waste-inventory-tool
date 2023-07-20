import pandas as pd

def evaluate_activity_limits(streams: pd.DataFrame, radionucleide_cols: list[str], activity_limits: pd.Series):
    is_within_limit = pd.DataFrame(index=streams.index, columns=['Normalised Activity', 'Is Within Limit'])

    is_within_limit['Normalised Activity'] = streams[radionucleide_cols].div(activity_limits).sum(axis=1)
    is_within_limit['Is Within Limit'] = True
    is_within_limit.loc[is_within_limit['Normalised Activity']>=1, 'Is Within Limit'] = False

    return is_within_limit