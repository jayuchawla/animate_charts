import os
import pandas as pd

def csv_merger(identifier_col, cols_to_include, col_prefixes, saveas, *args, cached=True):
    """
    pass multiple csv files to merge based on a specific column present in each file
    parameters
    ----------
    identifier_col (merge key)
    cols_to_include (what columns to include)
    col_prefixes (value to prefix )
    example:
    ----------
    identifier_col -> year
    cols_to_include -> Fossil CO2Emissions(tons)
    col_prefixes -> [China, India, ...]
    saveas -> merged.csv
    """
    if cached and os.path.isfile(saveas):
        # log this below statement
        # print('Cached mode: ON and File exists, returning same file content!')
        return None
    else:
        if len(col_prefixes) != len(args):
            # raise custom exception
            print('Num of csv files and col_prexis shape do not match!')
            return None
        
        merged_df = pd.read_csv(args[0])
        merged_df = merged_df[[identifier_col, cols_to_include]]
        merged_df = merged_df.rename(columns={cols_to_include:col_prefixes[0] + '_' + cols_to_include})
        # print(merged_df)
        for index in range(len(args) - 1):
            # read_csv
            csv = pd.read_csv(args[index+1])
            # filter only required columns
            csv = csv[[identifier_col, cols_to_include]]
            merged_df = merged_df.merge(csv, left_on=identifier_col, right_on=identifier_col, how='outer')
            merged_df = merged_df.rename(columns={cols_to_include:col_prefixes[index+1] + '_' + cols_to_include})

        # write to csv
        # check if dir exists
        dir = os.path.dirname(saveas)
        if not os.path.isdir(dir):
            os.mkdir(dir)

        merged_df.to_csv(saveas, index=False)    


if __name__ == '__main__':
    csvs = (
        'F:/work_learning/Chart Animation/data/afghanistan-co2.csv',
        'F:/work_learning/Chart Animation/data/albania-co2.csv'
    )

    csv_merger('Year', 'Fossil CO2Emissions(tons)', ['Afghanistan', 'Albania'], 'F:/work_learning/Chart Animation/utility/data/merged.csv', *csvs)