import pandas as pd

def metadata( dataframe ):
  '''Given a dataframe, returns a dataframe of metadata about the dataframe'''
  metadata_df = pd.DataFrame()
  metadata_df["Nulls"] = dataframe.isnull().sum()
  metadata_df.insert(0, "Count", len(dataframe))
  metadata_df["Nulls_pct"] = ( metadata_df["Nulls"] / metadata_df["Count"] * 100 ).round(1)
  metadata_df["Data_types"] = dataframe.dtypes
  metadata_df["Memory"] = dataframe.memory_usage( deep = True)
  metadata_df["NUnique"] = dataframe.nunique()
  metadata_df["NUnique_pct"] = (dataframe.nunique() / metadata_df["Count"] * 100).round(1)
  metadata_df = metadata_df.join( dataframe.describe( include = "all" ).transpose() )
  metadata_df["IRQ"] = metadata_df["75%"] - metadata_df["25%"]
  metadata_df["range"] = metadata_df["max"] - metadata_df["min"]
  metadata_df["sum"] = metadata_df["mean"] * metadata_df["count"]
  metadata_df = (
    metadata_df
    .astype( { "count" : int } )
    .rename( columns = {
      "25%" : "Q1_25%",
      "50%" : "Q2_median",
      "75%" : "Q3_75%",
      }
    )
  )
  return metadata_df
  
def cols_to_drop( dataframe ):
  '''Given a dataframe, returns columns that should likely be dropped'''
  md = metadata( dataframe )
  filter = md["Nulls_pct"] >= 40
  return md[ filter ]["Nulls_pct"].to_dict()

def likely_ids( dataframe ):
  '''Given a dataframe, returns a dictionary of likely ID columns'''
  md = metadata( dataframe )
  return md["NUnique_pct"][ md["NUnique_pct"] > 95 ].sort_values( ascending = False )





