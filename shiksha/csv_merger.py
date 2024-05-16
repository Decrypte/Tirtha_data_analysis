import pandas as pd
import os
import glob


csv_directory = "D:/#VSCode/Collegedunia/Tirtha"
output_directory = "D:/#Data/Scraped Data"
output_file = "merged_questions.csv"

# glob to match the CSV file pattern
csv_files = glob.glob(os.path.join(csv_directory, "shiksha_lpu_questions_*.csv"))

df_list = []

for file in csv_files:
    df = pd.read_csv(file)
    df_list.append(df)

merged_df = pd.concat(df_list, ignore_index=True)

output_path = os.path.join(output_directory, output_file)
merged_df.to_csv(output_path, index=False)

print(f"Successfully merged {len(csv_files)} files and saved to {output_path}.")
