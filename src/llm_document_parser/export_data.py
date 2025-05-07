import pandas as pd
from pathlib import Path
import json
from typing import List


def convert_json_to_df(json_data: str) -> pd.DataFrame:
    """
    Convert a JSON string into a pandas DataFrame.
    Automatically extracts the first top-level list if present.
    """
    data = json.loads(json_data)

    # Try to extract the list of transactions if it's wrapped
    list_name = None
    for key, value in data.items():
        if isinstance(value, list):
            list_name = key
            break

    if list_name:
        data = data[list_name]

    return pd.DataFrame(data)

def combine_json_data_into_df(json_data_objects: List[str]) -> pd.DataFrame:
    json_dfs = list()
    for json_object in json_data_objects:
        json_dfs.append(convert_json_to_df(json_object))

    return pd.concat(json_dfs)

def export_as_csv(df: pd.DataFrame, output_folder: str, output_file_name: str) -> str:
    """
    Save a DataFrame as a CSV file, avoiding overwriting by incrementing filenames.
    """
    output_folder_path = Path(output_folder)
    if not output_folder_path.is_dir():
        print(f"Creating path {output_folder}")
        output_folder_path.mkdir(parents=True)

    file_index = 0
    while True:
        full_output_path = output_folder_path / f"{output_file_name}{file_index}.csv"
        if not full_output_path.exists():
            break
        file_index += 1

    df.to_csv(full_output_path, index=False)
    print(f"Saved CSV to {full_output_path}")
    return df.to_csv(path_or_buf=None, index=False)


def export_as_json(df: pd.DataFrame, output_folder: str, output_file_name: str) -> str:
    """
    Save raw JSON string to a file, avoiding overwriting by incrementing filenames.
    """
    output_folder_path = Path(output_folder)
    if not output_folder_path.is_dir():
        print(f"Creating path {output_folder}")
        output_folder_path.mkdir(parents=True)

    file_index = 0
    while True:
        full_output_path = output_folder_path / f"{output_file_name}{file_index}.json"
        if not full_output_path.exists():
            break
        file_index += 1

    df.to_json(full_output_path, orient='records')
    print(f"Saved JSON to {full_output_path}")
    return df.to_json(orient='records') or ""
