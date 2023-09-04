import numpy as np
import pandas as pd


def generate_negative_matrix(filename, threshold=0.8):
    df = pd.read_csv(filename, sep='\t')
    barcodes = sorted(set(df.index1 + df.index2 + df.tag))
    genes = sorted(set(df.gene_id))
    tags = sorted(set(df.tag))
    
    res = df.groupby(['tag', 'umi', 'gene_id', 'index1', 'index2']).size().to_frame()
    res.rename(columns={0: 'counts'}, inplace=True)
    res['tot1'] = res.assign(tot1=lambda x: x.groupby(['tag', 'umi', 'gene_id', 'index1'])['counts'].sum())['tot1']
    res = res.swaplevel('index1', 'index2').assign(tot2=lambda x: x.groupby(['tag', 'umi', 'gene_id', 'index2'])['counts'].sum())
    res['filter'] = res['counts'] < threshold * (res['tot1'] + res['tot2'] - res['counts'])
    res = res[res['filter']].reset_index().drop(columns=['counts', 'tot1', 'tot2', 'filter'])
    res['CB'] = res['index1'] + res['index2'] + res['tag']
    res.drop(columns=['index1', 'index2', 'tag'], inplace=True)
    res = res.groupby(['CB', 'gene_id']).nunique()
    res = res.unstack(fill_value=0)
    res.columns = res.columns.droplevel()
    res.index.name = None
    res.columns.name = None
    count_mtx = res.reindex(index=barcodes, columns=genes, copy=True)
    count_mtx.fillna(0, inplace=True)
    return count_mtx