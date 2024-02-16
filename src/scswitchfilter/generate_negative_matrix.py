import numpy as np
import pandas as pd


def generate_negative_matrix(filename, threshold=0.8, is_tag=False):
    df = pd.read_csv(filename, sep='\t')
    genes = sorted(set(df.gene_id))
    group_lst = ['umi', 'gene_id', 'index1', 'index2']
    drop_lst = ['index1', 'index2'] + (['tag'] if is_tag else [])

    if is_tag:
        group_lst.insert(0, 'tag')
        barcodes = sorted(set(df.index1 + df.index2 + df.tag))
    else:
        barcodes = sorted(set(df.index1 + df.index2))

    res = df.groupby(group_lst).size().to_frame()
    res.rename(columns={0: 'counts'}, inplace=True)

    tmp_lst = group_lst.copy()
    tmp_lst.remove('index2')
    res['tot1'] = res.assign(tot1=lambda x: x.groupby(tmp_lst)['counts'].sum())['tot1']

    tmp_lst = group_lst.copy()
    tmp_lst.remove('index1')
    res = res.swaplevel('index1', 'index2').assign(tot2=lambda x: x.groupby(tmp_lst)['counts'].sum())

    res['filter'] = res['counts'] < threshold * (res['tot1'] + res['tot2'] - res['counts'])
    res = res[res['filter']].reset_index().drop(columns=['counts', 'tot1', 'tot2', 'filter'])
    if is_tag:
        res['CB'] = res['index1'] + res['index2'] + res['tag']
    else:
        res['CB'] = res['index1'] + res['index2']
    res.drop(columns=drop_lst, inplace=True)
    res = res.groupby(['CB', 'gene_id']).nunique()
    res = res.unstack(fill_value=0)
    res.columns = res.columns.droplevel()
    res.index.name = None
    res.columns.name = None
    count_mtx = res.reindex(index=barcodes, columns=genes, copy=True)
    count_mtx.fillna(0, inplace=True)
    return count_mtx
