import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import calendar

def normalize(original_df,resampled_df, time):
    for col in resampled_df.columns:

        missing_mask = resampled_df[col].isnull()

        for idx, value in resampled_df[col][missing_mask].items():
          idx = pd.Timestamp(idx)
          before_idx = original_df.loc[:idx, 'Caudal'].last_valid_index()
          after_idx = original_df.loc[idx:, 'Caudal'].first_valid_index()
          if before_idx is not None and after_idx is not None and (after_idx - before_idx).total_seconds() <= pd.Timedelta(minutes=time).total_seconds():
            resampled_df.at[idx, col] = original_df[col][before_idx] + \
                                            ((original_df[col][after_idx] - original_df[col][before_idx]) /
                                            (after_idx - before_idx).total_seconds()) * \
                                            (idx - before_idx).total_seconds()
            