import pandas as pd

def get_conditioning_deltas():
    pass

def assign_conditioning_materials(streams: pd.DataFrame) -> pd.DataFrame:
    """
    Determines the conditioning material to use for a stream.
    If an override is already provided in the stream, the override is assigned.
    If no override is assigned and the conditioning factor > 1, grout is assigned.
    If no override is assigned and the conditioning factor <= 1, "No Conditioning Material" is assigned.

    The corresponding density is also returned.

    This function returns a series and does not modify the stream dataframe in place.
    """
    no_conditioning_material_override = streams["Conditioning material"].isna()
    is_grout_conditioned = no_conditioning_material_override & (streams["Conditioning factor"] > 1)
    is_not_conditioned = no_conditioning_material_override & ~is_grout_conditioned

    conditioning_materials = pd.Series(index=streams.index, name="Conditioning material")

    conditioning_materials.loc[~no_conditioning_material_override] = streams["Conditioning material"].loc[~no_conditioning_material_override]
    conditioning_materials.loc[is_grout_conditioned] = "Grout"
    conditioning_materials.loc[is_not_conditioned] = "No Conditioning Material"

    return conditioning_materials.to_frame().merge(MATERIALS_DENSITY_TABLE, left_on="Conditioning material", right_index=True, how="left")


def get_conditioning_deltas(streams: pd.DataFrame) -> pd.DataFrame:
    additional_volume = additional_conditioning_volume(streams)
    conditioning_materials = assign_conditioning_materials(streams)

    additional_mass = conditioning_materials["Density"] * additional_volume

    result = pd.DataFrame()
    result["Volume Delta"] = additional_volume
    result["Mass Delta"] = additional_mass
    result["Conditioning material"] = conditioning_materials["Conditioning material"]
    return result


def additional_conditioning_volume(streams: pd.DataFrame) -> pd.Series:
    return (streams["Conditioning factor"] - 1) * streams["Volume"]


def total_conditioning_volume(streams: pd.DataFrame) -> pd.Series:
    return streams["Volume"] + additional_conditioning_volume(streams)


MATERIALS_DENSITY_TABLE = pd.Series({
    "Air": 0, 
    "Grout": 1.7, 
    "No Conditioning Material": 0,
}, name="Density")