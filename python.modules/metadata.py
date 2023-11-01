import pandas as pd

def metadata( dataframe ):
  '''Given a dataframe, returns a dataframe of metadata about the dataframe'''
  metatdata_df = dataframe.describe( include = "all" ).transpose()
  metatdata_df = (
    metatdata_df
    .astype( { "count" : int } )
    .rename( columns = {
      "25%" : "Q1_25%",
      "50%" : "Q2_median",
      "75%" : "Q3_75%",
      }
    )
  )
  metatdata_df["unique"] = dataframe.nunique()
  metatdata_df["Nulls"] = dataframe.isnull().sum()
  metatdata_df["Nulls_pct"] = ( metatdata_df["Nulls"] / dataframe.shape[0] * 100 ).round(1)
  metatdata_df["Data_types"] = dataframe.dtypes
  metatdata_df["Memory"] = dataframe.memory_usage( deep = True)
  return metatdata_df
  
def cols_to_drop( dataframe ):
  '''Given a dataframe, returns columns that should likely be dropped'''
  md = metadata( dataframe )
  filter = md["Nulls_pct"] >= 80
  return md[ filter ]["Nulls_pct"].to_dict()

def likely_ids( dataframe ):
  '''Given a dataframe, returns a dictionary of likely ID columns'''
  md = metadata( dataframe )
  ids = ( md["unique"]/md["count"] ) * 100
  return  ids[ ids > 95 ].sort_values( ascending = False).to_dict()





