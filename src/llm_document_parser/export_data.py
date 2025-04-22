from io import StringIO
import pandas as pd
from pathlib import Path

def export_as_csv(json_data: str, output_folder: str, output_file_name: str):
    data = pd.read_json(StringIO(json_data))
    df = pd.DataFrame(data)

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
