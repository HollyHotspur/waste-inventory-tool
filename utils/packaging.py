import pandas as pd

def construct_package_routes(package_routes: list[tuple[str, str]], package_definitions: pd.DataFrame) -> pd.DataFrame:
    primary_containers = []
    secondary_containers = []

    for (primary_step, secondary_step) in package_routes:
        primary_containers.append(package_definitions.loc[package_definitions["Package type"] == primary_step])
        secondary_containers.append(package_definitions.loc[package_definitions["Package type"] == secondary_step])

    primary_df = pd.concat(primary_containers).reset_index()
    secondary_df = pd.concat(secondary_containers).reset_index().add_prefix("Secondary ", axis="columns")

    package_routes_df = primary_df.merge(secondary_df, left_index=True, right_index=True, how="left")
    return package_routes_df


def get_packaging_changes(streams: pd.DataFrame, package_routes: pd.DataFrame) -> pd.DataFrame:
    stream_data = streams.merge(package_routes, left_on="Package type", right_on="Package type", how="left")
    
    primary_packaged_volume = stream_data["Volume"] * (stream_data["Packaging factor"] / stream_data["Conditioning factor"])
    number_of_primary_containers = primary_packaged_volume / stream_data["External volume"]
    primary_mass_delta = number_of_primary_containers * stream_data["Container weight"]

    result = pd.DataFrame()
    result["Primary Package"] = stream_data["Package type"]
    result["Primary Packaged Volume"] = primary_packaged_volume
    result["Primary Mass Delta"] = primary_mass_delta.fillna(0)
    result["No. of Primary Containers"] = number_of_primary_containers.fillna(0)

    secondary_packaged_volume = primary_packaged_volume * stream_data["Secondary Default packing factor"]
    number_of_secondary_containers = (secondary_packaged_volume / stream_data["Secondary External volume"]).fillna(0)
    secondary_mass_delta = number_of_secondary_containers * stream_data["Secondary Container weight"]

    result["Secondary Package"] = stream_data["Secondary Package type"]
    result["Secondary Packaged Volume"] = secondary_packaged_volume
    result["Secondary Mass Delta"] = secondary_mass_delta
    result["No. of Secondary Containers"] = number_of_secondary_containers
    return result