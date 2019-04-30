import algoDis
import dataCenter
import dataViz
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
import math
import time

def testFunction(i,d):
    d[i]=i+100
    print(d.values())

annotations=[]
def showLabel(event):
    # print(event.key)
    visibility_changed = False
    for point, annotation in annotations:
        vector1 = np.array([point[0], point[1]])
        vector2 = np.array([event.xdata, event.ydata])

        should_be_visible = ((np.linalg.norm(vector1-vector2)<0.002) == True)

        if should_be_visible != annotation.get_visible():
            print(should_be_visible)
            visibility_changed = True
            annotation.set_visible(should_be_visible)

    if visibility_changed:
        plt.draw()


# Main execution
if __name__ == "__main__":
    # test专用
    file='D:\\pycharm_workspace\\projetLibre\\fr.openfoodfacts.org.products.csv'
    # file = 'test.csv'
    # file='D:\\pycharm_workspace\\projetLibre\\fileOrigin.csv'
    df = pd.DataFrame()
    with open(file)as f:
        chunk_iter = pd.read_csv(file, sep='\t', iterator=True, chunksize=100000, low_memory=False,nrows=500)  # error_bad_lines=False low_memory=False
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

    dfBrands=df['brands']
    dfBrands=dfBrands.fillna(value='NoBrand',axis=0).unique()

    # 计算两条记录的2gram的余弦值
    algo = algoDis.AlgoDis()
    data_Viz = dataViz.DataViz()

    # 画图配置
    fig1 = plt.figure(num='fig1')
    r = 1
    o_x, o_y = (0., 0.)
    theta = np.arange(0, 2 * np.pi, 0.01)
    x = o_x + r * np.cos(theta)
    y = o_y + r * np.sin(theta)
    plt.plot(x,y)
    plt.axis('equal')

    # 并行！！！！
    num_pois = 5
    num_divide_df = 100

    # 开始选取参考点
    timeStartKmeans=time.localtime()
    print('start k-means: ' + str(timeStartKmeans))
    # list_pois, pois = dataCenter.selectPOIs(df, num_pois)
    list_pois, pois = dataCenter.selectPOIsRandom(num_pois,df)
    list_pois_labels=[]
    for index in list_pois:
        list_pois_labels.append(df.iloc[index]['product_name'])
    df_copy = df
    df_copy = df_copy.drop(list_pois, axis=0)
    num_divide_dfc= math.floor(len(df_copy)/16)

    # 获取参考点的坐标和标签
    poisCoord = data_Viz.drawCircle(num_pois, list_pois_labels)
    for index in range(len(poisCoord)):
        plt.text(poisCoord[index][0], poisCoord[index][1] + 0.01, poisCoord[index][2], ha='center', va='bottom', fontsize=9)
        plt.plot(poisCoord[index][0], poisCoord[index][1], 'r*', label="point")
    timeEndKmeans = time.localtime()
    print('k-means finit: '+ str(timeEndKmeans))

    # 开始计算所有点和参考点的距离
    m = multiprocessing.Manager()
    directory = m.dict()
    p = multiprocessing.Pool(4)
    for i in range(16):
        p.apply_async(data_Viz.draw, args=(df_copy.iloc[i * num_divide_dfc:(i * num_divide_dfc + num_divide_dfc if i * num_divide_dfc + num_divide_dfc < len(df_copy) else len(df_copy))], num_pois, pois, i, directory))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

    # 开始画所有的点
    print('length: '+ str(len(directory)))
    print(str(time.localtime()))
    print('All subprocesses done.')
    for key,value in directory.items():
        point=plt.plot(value[0],value[1],'mo',MarkerSize=8)
        product_name=df.iloc[key]['product_name']
        product_brand = df.iloc[key]['brands']
        product_info='name: '+str(product_name)+', brand: '+str(product_brand)
        anno=plt.annotate(product_info,xy=(value[0], value[1]),xytext =(value[0]+0.0001, value[1]+0.0001))
        anno.set_visible(False)
        coordonnee=[value[0], value[1]]
        annotations.append([coordonnee,anno])
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    fig1.canvas.mpl_connect('button_press_event',showLabel)
    plt.show()
    timeEnd = time.localtime()
    print('END OF THE PROJECT: '+str(timeEnd))

    # dataCenter.selectPOIs(df)

