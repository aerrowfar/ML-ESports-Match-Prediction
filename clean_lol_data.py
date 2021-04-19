import glob
import re
import json

import pandas as pd
import numpy as np

import great_expectations as ge

from get_champions import marshall_champion_data

# Variables

OUTPUT_FILE = "lol_game_data"
CHAMPION_FILE = "lol_classes"

USECOL = [
    "date",
    "game",
    "playerid",
    "position",
    "player",
    "team",
    "champion",
    "result",
    "golddiffat10",
    "golddiffat15",
]

VALID_ENTRY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 200]

TEAMGOLDDIFF = ["teamgolddiffat10", "teamgolddiffat15"]

# Functions


def return_filenames_in_directory(extension="csv"):
    print("Reading csv data from disk")
    csv_filenames = [
        i
        for i in glob.glob(f"*.{extension}")
        if not (re.search(OUTPUT_FILE, i) or re.search(CHAMPION_FILE, i))
    ]
    csv_filenames.sort()
    print("Current csv files to be combined:")
    [print(name) for name in csv_filenames]
    return csv_filenames


def combine_lol_files(csv_filenames):
    print("Combining csv data into a single dataframe")
    dataframes = [pd.read_csv(f, usecols=USECOL) for f in csv_filenames]
    df = pd.DataFrame(np.concatenate([df.values for df in dataframes]), columns=USECOL)
    print(f"The size of the combined csv files is: {df.size}")
    return df


def add_team_gold(df):

    df = df.copy().reset_index()

    # Get team values
    golddiff10_team_1 = df.loc[10, "golddiffat10"]
    golddiff10_team_2 = df.loc[11, "golddiffat10"]
    golddiff15_team_1 = df.loc[10, "golddiffat15"]
    golddiff15_team_2 = df.loc[11, "golddiffat15"]

    # Drop unecessary rows
    df.drop([10, 11], inplace=True)

    teamgolddiff10 = pd.Series(
        np.repeat([golddiff10_team_1, golddiff10_team_2], [5, 5])
    ).astype(int)

    teamgolddiff15 = pd.Series(
        np.repeat([golddiff15_team_1, golddiff15_team_2], [5, 5])
    ).astype(int)

    # Create new columns
    df[TEAMGOLDDIFF[0]] = teamgolddiff10
    df[TEAMGOLDDIFF[1]] = teamgolddiff15

    return df


def get_starting_index_value(df):
    indexes_of_one = df.index[df.loc[:, "playerid"] == 1].tolist()
    return indexes_of_one


def check_if_entry_is_valid(df_entry_to_check):
    player_positions_to_check = df_entry_to_check.loc[:, "playerid"].values

    is_index_valid = player_positions_to_check == VALID_ENTRY
    is_missing_values_gold10 = (
        df_entry_to_check.loc[:, "golddiffat10"].isnull().values.any()
    )
    is_missing_values_gold15 = (
        df_entry_to_check.loc[:, "golddiffat15"].isnull().values.any()
    )
    is_containing_unknown = (
        df_entry_to_check.loc[:, "team"].str.contains("unknown_team").any()
    )

    is_valid_entry = (
        is_index_valid.all()
        and not is_missing_values_gold10
        and not is_missing_values_gold15
        and not is_containing_unknown
    )

    return is_valid_entry


def return_valid_entries(df, indexes_of_one):
    print("Processing data to find valid entries")
    valid_length = len(VALID_ENTRY)
    valid_entries = []

    for idx in indexes_of_one:
        ending_index = idx + valid_length
        entry_to_check = df.iloc[idx:ending_index]

        is_valid_entry = check_if_entry_is_valid(entry_to_check)

        if is_valid_entry:
            entry_with_team_gold = add_team_gold(entry_to_check)
            valid_entries.append(entry_with_team_gold)

            if len(valid_entries) % 1000 == 0:
                print(f"Current valid entries : {len(valid_entries)}")

    print(f"Total valid entries : {len(valid_entries)}")
    return valid_entries


def combine_valid_entries(valid_entries):
    print("Combining all valid entries into a single dataframe")

    usecol_with_teamgold = USECOL + TEAMGOLDDIFF

    dataframes = [
        pd.DataFrame(entry, columns=usecol_with_teamgold) for entry in valid_entries
    ]

    df = pd.DataFrame(
        np.concatenate([df.values for df in dataframes]), columns=usecol_with_teamgold
    )

    return df


def add_champion_metadata(df) -> pd.DataFrame:
    champ_dict = marshall_champion_data()
    classes = df.loc[:, "champion"].map(champ_dict)
    df.insert (8, "classes", classes)
    return df


def move_column_to_end(df, column_name):
    cols = df.columns.tolist()
    cols.pop(cols.index(column_name))
    cols = cols + [column_name]

    return df.reindex(columns=cols)


def test_uniqueness_of_dataframe(df):
    """
    Check if each row in the dataframe is unique
    """
    duplicated_rows = df[df.duplicated()]

    if not duplicated_rows.empty:
        print("Duplicate Rows except first occurrence based on all columns are:")
        print(duplicated_rows)
        raise ValueError

    print("No duplicated values")


def test_dataframe(df):
    """
    Test the resulting dataframe to ensure data integrity. Can be expanded
    if further tests are needed.
    """
    print("Performing final validation test on dataframe")
    ge_df = ge.from_pandas(df)

    # Check nulls

    columns_not_null = df.columns

    for column in columns_not_null:
        result = ge_df.expect_column_values_to_not_be_null(column)
        assert (
            result["success"] == True
        ), "Coluns contain null value. Please check data."

    # Ensure result is only between 0 and 1
    result = ge_df.expect_column_values_to_be_between(
        "result", min_value=0, max_value=1
    )

    assert result["success"] == True, "Results not between 0 and 1, please check data"

    # Make sure the gold delta does not have outliders
    gold_delta = [
        "golddiffat10",
        "golddiffat15",
        "teamgolddiffat10",
        "teamgolddiffat15",
    ]

    for column in gold_delta:
        result = ge_df.expect_column_values_to_be_between(
            column, min_value=-20000, max_value=20000
        )
        assert result["success"] == True, "Gold diff values too high, please check data"

    print("Data validation passed.")
    return df


def write_dataframe_to_disk(df):
    print("Writing to disk")
    df.to_csv("lol_game_data.csv")


def app():
    print("Starting processing")

    files = return_filenames_in_directory()
    df = combine_lol_files(files)
    indexes_of_one = get_starting_index_value(df)
    valid_entries = return_valid_entries(df, indexes_of_one)
    df_combined = combine_valid_entries(valid_entries)
    df_metadata = add_champion_metadata(df_combined)
    df_reindexed = move_column_to_end(df_metadata, "result")
    test_uniqueness_of_dataframe(df_reindexed)
    df_final = test_dataframe(df_reindexed)
    write_dataframe_to_disk(df_final)

    print("Finishied processing. Closing app.")


if __name__ == "__main__":
    app()
