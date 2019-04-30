import numpy as np
import algoDis
import dataCenter
import dataViz
import time
import os


# classe pour visualiser l'analyse
class DataViz:
    dataCenter = dataCenter.DataCenter()
    algo = algoDis.AlgoDis()

    def draw(self, df, num_pois, pois,ind,directory):
        print('Run task %s (%s)...' % (ind, os.getpid()))
        start = time.time()
        for index, point in df.iterrows():
            dis = [ ]
            for i, poi in pois.iterrows():
                dis.append(self.algo.calculateDis(poi, point))
            coordonnee=self.drawPoint(dis, num_pois)
            info='name: '+str(point['product_name'])+', brand: '+str(point['brand1'])
            directory[index] = [coordonnee[0],coordonnee[1],point['code'],info,point['brand1']]
            # directory[ind+index] = [coordonnee[0],coordonnee[1],point['code']]
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (ind, (end - start)))

    def save(self):
        pass

    def drawCircle(self, num_points,list_pois_labels):
        r = 1
        o_x, o_y = (0., 0.)

        theta = np.arange(0, 2 * np.pi, 0.01)
        x = o_x + r * np.cos(theta)
        y = o_y + r * np.sin(theta)

        poisCoord=[]
        # ax.plot(x, y)
        for i in range(num_points):
            px = o_x + r * np.cos((i / num_points) * 2 * np.pi + 0.5 * np.pi)
            py = o_y + r * np.sin((i / num_points) * 2 * np.pi + 0.5 * np.pi)
            poisCoord.append([px,py,list_pois_labels[i]])
        return poisCoord

    def drawPoint(self, prlist, num_pois, index=''):
        sumdis = sum(prlist)
        W = [ ]
        for dis in prlist:
            W.append(dis / sumdis)

        p_x, p_y = 0, 0
        r = 1
        o_x, o_y = (0., 0.)

        theta = np.arange(0, 2 * np.pi, 0.01)
        for i in range(num_pois):
            p_x += W[ i ] * (o_x + r * np.cos((i / num_pois) * 2 * np.pi + 0.5 * np.pi))
            p_y += W[ i ] * (o_y + r * np.sin((i / num_pois) * 2 * np.pi + 0.5 * np.pi))


        coordonnee=[p_x,p_y]
        return coordonnee

    def calculateLambda(self, data1, data2,num_pois):
        distance=[]
        data_viz=dataViz.DataViz()
        for i, poi in data2.iterrows():
            distance.append(self.algo.calculateDis(poi, data1))
        coordonnee = self.drawPoint(distance, num_pois)
        coordonnee.append(data1['product_name'])
        return coordonnee
