import algoDis
import dataCenter
import dataViz
import pandas as pd
import numpy as np
import multiprocessing
import math
import time
import plotly as py
import plotly.graph_objs as go
import cleanBrand



# Main execution
if __name__ == "__main__":
    # test专用
    file='D:\\pycharm_workspace\\projetLibre\\fr.openfoodfacts.org.products.csv'
    # file = 'test.csv'
    # file='D:\\pycharm_workspace\\projetLibre\\fileOrigin.csv'
    df = pd.DataFrame()
    with open(file)as f:
        chunk_iter = pd.read_csv(file, sep='\t', iterator=True, chunksize=100000, low_memory=False)  # error_bad_lines=False low_memory=False ,nrows=100
        # chunk_iter = pd.read_csv(file, sep=',', iterator=True, chunksize=100000)
        for chunk in chunk_iter:
            df = pd.concat([df, chunk])

    # 正式的程序
    dataCenter = dataCenter.DataCenter()
    colslist = ['code','url', 'product_name', 'brands', 'categories', 'categories_fr', 'labels', 'allergens_fr', 'traces_fr',
                'additives_n',
                'additives_fr', 'main_category_fr', 'image_small_url', 'energy_100g', 'energy-from-fat_100g',
                'fat_100g', 'saturated-fat_100g', 'butyric-acid_100g', 'caproic-acid_100g', 'caprylic-acid_100g',
                'capric-acid_100g', 'lauric-acid_100g', 'myristic-acid_100g', 'palmitic-acid_100g',
                'stearic-acid_100g', 'arachidic-acid_100g', 'behenic-acid_100g', 'lignoceric-acid_100g',
                'cerotic-acid_100g', 'montanic-acid_100g', 'melissic-acid_100g', 'monounsaturated-fat_100g',
                'polyunsaturated-fat_100g', 'omega-3-fat_100g', 'alpha-linolenic-acid_100g',
                'eicosapentaenoic-acid_100g', 'docosahexaenoic-acid_100g', 'omega-6-fat_100g', 'linoleic-acid_100g',
                'arachidonic-acid_100g', 'gamma-linolenic-acid_100g', 'dihomo-gamma-linolenic-acid_100g',
                'omega-9-fat_100g', 'oleic-acid_100g', 'elaidic-acid_100g', 'gondoic-acid_100g', 'mead-acid_100g',
                'erucic-acid_100g', 'nervonic-acid_100g', 'trans-fat_100g', 'cholesterol_100g', 'carbohydrates_100g',
                'sugars_100g', 'sucrose_100g', 'glucose_100g', 'fructose_100g', 'lactose_100g', 'maltose_100g',
                'maltodextrins_100g', 'starch_100g', 'polyols_100g', 'fiber_100g', 'proteins_100g', 'casein_100g',
                'serum-proteins_100g', 'nucleotides_100g', 'salt_100g', 'sodium_100g', 'alcohol_100g',
                'vitamin-a_100g', 'beta-carotene_100g', 'vitamin-d_100g', 'vitamin-e_100g', 'vitamin-k_100g',
                'vitamin-c_100g', 'vitamin-b1_100g', 'vitamin-b2_100g', 'vitamin-pp_100g', 'vitamin-b6_100g',
                'vitamin-b9_100g', 'folates_100g', 'vitamin-b12_100g', 'biotin_100g', 'pantothenic-acid_100g',
                'silica_100g', 'bicarbonate_100g', 'potassium_100g', 'chloride_100g', 'calcium_100g',
                'phosphorus_100g', 'iron_100g', 'magnesium_100g', 'zinc_100g', 'copper_100g', 'manganese_100g',
                'fluoride_100g', 'selenium_100g', 'chromium_100g', 'molybdenum_100g', 'iodine_100g', 'caffeine_100g',
                'taurine_100g', 'ph_100g', 'fruits-vegetables-nuts_100g', 'fruits-vegetables-nuts-estimate_100g',
                'collagen-meat-protein-ratio_100g', 'cocoa_100g', 'chlorophyl_100g', 'carbon-footprint_100g',
                'nutrition-score-fr_100g', 'nutrition-score-uk_100g', 'glycemic-index_100g', 'water-hardness_100g',
                'choline_100g', 'phylloquinone_100g', 'beta-glucan_100g', 'inositol_100g', 'carnitine_100g']
    df = dataCenter.cleanData(df, colslist)
    cols = df.columns.values.tolist()
    df.info()

    clean_brand=cleanBrand.CleanBrand()
    dfBrand1=clean_brand.getBrandsClean()
    df['brand1']=dfBrand1

    df['brand1']=df['brand1'].fillna(value='NoBrand',axis=0)

    # 计算两条记录的2gram的余弦值
    algo = algoDis.AlgoDis()
    data_Viz = dataViz.DataViz()

    # 并行！！！！
    num_pois = 5
    num_divide_df = 100

    # 开始选取参考点
    timeStartKmeans=time.localtime()
    print('choose POIs: ' + str(timeStartKmeans))
    list_pois, pois = dataCenter.selectPOIs(df.iloc[1:5000], num_pois)
    # list_pois, pois = dataCenter.selectPOIsRandom(num_pois,df)
    list_pois_labels=[]
    for index in list_pois:
        list_pois_labels.append(index)
    df_copy = df
    df_copy = df_copy.drop(list_pois, axis=0)
    num_divide_dfc= math.floor(len(df_copy)/64)

    # 获取参考点的坐标和标签
    poisCoord = data_Viz.drawCircle(num_pois, list_pois_labels)
    timeEndKmeans = time.localtime()
    print('choose POIs finish: ' + str(timeEndKmeans))

    # 开始计算所有点和参考点的距离
    m = multiprocessing.Manager()
    directory = m.dict()
    p = multiprocessing.Pool(3)
    for i in range(64):
        p.apply_async(data_Viz.draw, args=(df_copy.iloc[i * num_divide_dfc:(i * num_divide_dfc + num_divide_dfc if i * num_divide_dfc + num_divide_dfc < len(df_copy) else len(df_copy))], num_pois, pois, i, directory))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

    # 开始插入参考点
    for index in range(len(poisCoord)):
        info = 'name: ' + str(df.iloc[list_pois_labels[index]]['product_name']) + ', brand: ' + str(df.iloc[list_pois_labels[index]]['brand1'])
        directory[list_pois_labels[index]]=[poisCoord[index][0], poisCoord[index][1], df.iloc[list_pois_labels[index]]['code'],info,df.iloc[list_pois_labels[index]]['brand1']]

    print('length: '+ str(len(directory)))
    print(str(time.localtime()))
    print('All subprocesses done.')

    # 开始画所有的点
    print('Begin to draw.')
    dfDirectory=pd.DataFrame.from_dict(data=directory,orient='index',columns=['px','py','code','info','brands'])
    groupBrands=dfDirectory.groupby(['brands']).size().reset_index(name='brandCounts').sort_values(by='brandCounts',ascending=False).head(5)
    dfDirectory0=dfDirectory[dfDirectory['brands'] == groupBrands.iloc[0]['brands']]
    dfDirectory1=dfDirectory[dfDirectory['brands'] == groupBrands.iloc[1]['brands']]
    dfDirectory2=dfDirectory[dfDirectory['brands'] == groupBrands.iloc[2]['brands']]
    dfDirectory3=dfDirectory[dfDirectory['brands'] == groupBrands.iloc[3]['brands']]
    dfDirectory4=dfDirectory[dfDirectory['brands'] == groupBrands.iloc[4]['brands']]
    dfDirectory5=dfDirectory[(dfDirectory['brands'] != groupBrands.iloc[0]['brands']) & (dfDirectory['brands'] != groupBrands.iloc[1]['brands'])
                      & (dfDirectory['brands'] != groupBrands.iloc[2]['brands']) & (dfDirectory['brands'] != groupBrands.iloc[3]['brands'])
                         & (dfDirectory['brands'] != groupBrands.iloc[4]['brands'])]
    count5=len(df.index)-len(dfDirectory0.index)-len(dfDirectory1.index)-len(dfDirectory2.index)-len(dfDirectory3.index)-len(dfDirectory4.index)
    layout=go.Layout(
        title='OpenFood Analysis, Polytech Tours, 2019',
        shapes=[{
                'type': 'circle',
                'xref': 'x',
                'yref': 'y',
                'x0': -1,
                'y0': -1,
                'x1': 1,
                'y1': 1,
                'opacity': 0.2,
                'line': {
                    'color': 'blue',
                },
            }],
        width=800,
        height=800,
    )
    trace0 = go.Scattergl(
        x=dfDirectory0['px'],
        y=dfDirectory0['py'],
        text=dfDirectory0['info'],
        name=str(groupBrands.iloc[0]['brands'])+' - count:'+str(groupBrands.iloc[0]['brandCounts']),
        mode='markers',
        marker=dict(
            color='#f90303',
        )
    )
    trace1 = go.Scattergl(
        x=dfDirectory1['px'],
        y=dfDirectory1['py'],
        text=dfDirectory1['info'],
        name=str(groupBrands.iloc[1]['brands'])+' - count: '+str(groupBrands.iloc[1]['brandCounts']),
        mode='markers',
        marker=dict(
            color='#4a19e7',
        )
    )
    trace2 = go.Scattergl(
        x=dfDirectory2['px'],
        y=dfDirectory2['py'],
        text=dfDirectory2['info'],
        name=str(groupBrands.iloc[2]['brands'])+' - count: '+str(groupBrands.iloc[2]['brandCounts']),
        mode='markers',
        marker=dict(
            color='#787f32', #olive-colored
        )
    )
    trace3 = go.Scattergl(
        x=dfDirectory3['px'],
        y=dfDirectory3['py'],
        text=dfDirectory3['info'],
        name=str(groupBrands.iloc[3]['brands'])+' - count: '+str(groupBrands.iloc[3]['brandCounts']),
        mode='markers',
        marker=dict(
            color='#dbd310', #yellowish-green
        )
    )
    trace4 = go.Scattergl(
        x=dfDirectory4['px'],
        y=dfDirectory4['py'],
        text=dfDirectory4['info'],
        name=str(groupBrands.iloc[4]['brands'])+' - count: '+str(groupBrands.iloc[4]['brandCounts']),
        mode='markers',
        marker=dict(
            color='#9f00ff', # violet-colored
        )
    )
    trace5 = go.Scattergl(
        x=dfDirectory5['px'],
        y=dfDirectory5['py'],
        text=dfDirectory5['info'],
        name='Other brands'+' - count: '+str(count5),
        mode='markers',
        marker=dict(
            color='#008542', #green
        )
    )
    data = [trace0,trace1,trace2,trace3,trace4,trace5]
    #greeny #008542
    fig = {
        'data': data,
        'layout': layout,
    }
    py.offline.plot(fig, filename='WEBGL755205.html')

    timeEnd = time.localtime()
    print('END OF THE PROJECT: '+str(timeEnd))

