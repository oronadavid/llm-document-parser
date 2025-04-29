import pandas as pd
from pathlib import Path
import json

def convert_json_to_df(json_data: str) -> pd.DataFrame:
    data = json.loads(json_data)

    # Check for a list in the response
    list_name = None
    for key, value in data.items():
        if isinstance(value, list):
            list_name = key
    if list_name:
        data = data[list_name]

    return pd.DataFrame(data)

def export_as_csv(df: pd.DataFrame, output_folder: str, output_file_name: str):
    """
    """
    output_folder_path = Path(output_folder)
    if not output_folder_path.is_dir():
        print(f"Creating path {output_folder}")
        output_folder_path.mkdir()

    file_index = 0
    while True:
        full_output_path = output_folder_path / Path(output_file_name + str(file_index) + ".csv")
        if not full_output_path.exists():
            break
        file_index += 1

    df.to_csv(full_output_path, index=False)

def export_as_json(json_data: str, output_folder: str, output_file_name: str):
    data = json.loads(json_data)
    print(data)

    output_folder_path = Path(output_folder)
    if not output_folder_path.is_dir():
        print(f"Creating path {output_folder}")
        output_folder_path.mkdir()

    file_index = 0
    while True:
        full_output_path = output_folder_path / Path(output_file_name + str(file_index) + ".json")
        if not full_output_path.exists():
            break
        file_index += 1

    with open(full_output_path, "w") as f:
        f.write(json_data)

