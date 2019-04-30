import numpy as np
import operator
import math
import twoGrams
import unicodedata

class AlgoDis:

    def deleteNull(self, data1, data2):
        data1_no_null = [ ]
        data2_no_null = [ ]
        for i in range(len(data1)):
            if isinstance(data1[ i ], str) and isinstance(data2[ i ], str):
                if (len(data1[ i ]) != 0 and len(data2[ i ]) != 0):
                    if (operator.eq(str.lower(data1[ i ]), 'unknown') or operator.eq(str.lower(data2[ i ]), 'unknown')):
                        continue
                    else:
                        data1_no_null.append(data1[ i ])
                        data2_no_null.append(data2[ i ])
                else:
                    continue
            else:
                if (isinstance(data1[ i ], list) and isinstance(data2[ i ], list)) or (
                        isinstance(data1[ i ], dict) and isinstance(data2[ i ], dict)):
                    if len(data1[ i ]) != 0 and len(data2[ i ]) != 0:
                        if isinstance(data1[ i ], list) and isinstance(data2[ i ], list) and operator.eq(
                                str.lower(data1[ i ][ 0 ]), 'unknown') == False and operator.eq(
                            str.lower(data2[ i ][ 0 ]),
                            'unknown') == False:
                            data1_no_null.append(data1[ i ])
                            data2_no_null.append(data2[ i ])
                        else:
                            continue
                    else:
                        continue
                else:
                    if (isinstance(data1[ i ], list) == False and isinstance(data2[ i ], list) == False and
                            isinstance(data1[ i ], dict) == False and isinstance(data2[ i ], dict) == False and
                            isinstance(data1[ i ], str) == False and isinstance(data2[ i ], str) == False and
                            math.isnan(data1[ i ]) == False and math.isnan(data2[ i ]) == False):
                        data1_no_null.append(data1[ i ])
                        data2_no_null.append(data2[ i ])
                    else:
                        continue
        return data1_no_null, data2_no_null

    def selectNumeric(self, data):
        data_num = [ ]
        for d in data:
            if isinstance(d, str) == False and isinstance(d, list) == False and isinstance(d, dict) == False:
                data_num.append(d)
        data_num = np.array(data_num)
        return data_num

    def selectStr(self, dataFrame1):
        GramLabels = [ "categories_fr", "labels", "allergens_fr", "traces_fr", "additives_fr", "main_category_fr" ]
        vecFrame1 = [ ]
        for i in GramLabels:
            df1 = dataFrame1[ i ]
            if (isinstance(df1, list) == False and isinstance(df1, dict) == False and
                    isinstance(df1, str) == False and math.isnan(df1) == True):
                value1, _ = twoGrams.sorVec("")
                if (len(vecFrame1) == 0):
                    vecFrame1 = np.array(list(value1))
                else:
                    vecFrame1 = vecFrame1 + np.array(list(value1))
            else:
                value1, _ = twoGrams.sorVec(self.changeAccents(df1))
                if (len(vecFrame1) == 0):
                    vecFrame1 = np.array(list(value1))
                else:
                    vecFrame1 = vecFrame1 + np.array(list(value1))
        return vecFrame1

    def euclideanDistance(self, data1, data2):
        data1, data2 = self.deleteNull(data1, data2)
        data1 = self.selectNumeric(data1)
        data2 = self.selectNumeric(data2)

        dis = np.linalg.norm(data1 - data2)
        return dis


    def calculateDis(self, data1, data2):
        dis = 0.2 * self.euclideanDistance(data1, data2) +0.8 * self.calculate2GramCos(data1, data2)
        return dis

    def changeAccents(self, phase):
        unCode = unicodedata.normalize('NFKD', phase).encode('ascii', 'ignore').decode("utf-8")
        # print(unCode)
        return unCode

    # entree: 2 phrases
    # sortie: distance
    def calculateDis2GramNoUse(self, data1, data2):
        distance = 0
        value1, _ = twoGrams.sorVec(self.changeAccents(data1))
        value2, _ = twoGrams.sorVec(self.changeAccents(data2))
        distance = np.linalg.norm(np.array(list(value1)) - np.array(list(value2)))
        # print(distance)
        return distance

    def calculate2GramCos(self, dataFrame1, dataFrame2):
        GramLabels = [ "categories_fr", "labels", "allergens_fr", "traces_fr", "additives_fr", "main_category_fr" ]
        vecFrame1 = [ ]
        vecFrame2 = [ ]

        np.seterr(divide='ignore', invalid='ignore')

        for i in GramLabels:
            df1 = dataFrame1[ i ]
            if (isinstance(df1, list) == False and isinstance(df1, dict) == False and
                    isinstance(df1, str) == False and math.isnan(df1) == True):
                value1, _ = twoGrams.sorVec("")
                if (len(vecFrame1) == 0):
                    vecFrame1 = np.array(list(value1))
                else:
                    vecFrame1 = vecFrame1 + np.array(list(value1))
            else:
                value1, _ = twoGrams.sorVec(self.changeAccents(df1))
                if (len(vecFrame1) == 0):
                    vecFrame1 = np.array(list(value1))
                else:
                    vecFrame1 = vecFrame1 + np.array(list(value1))

            df2 = dataFrame2[ i ]
            if (isinstance(df2, list) == False and isinstance(df2, dict) == False and
                    isinstance(df2, str) == False and math.isnan(df2) == True):
                value2, _ = twoGrams.sorVec("")
                if (len(vecFrame2) == 0):
                    vecFrame2 = np.array(list(value2))
                else:
                    vecFrame2 = vecFrame2 + np.array(list(value2))
            else:
                value2, _ = twoGrams.sorVec(self.changeAccents(df2))
                if (len(vecFrame2) == 0):
                    vecFrame2 = np.array(list(value2))
                else:
                    vecFrame2 = vecFrame2 + np.array(list(value2))
        if((np.linalg.norm(vecFrame1) * np.linalg.norm(vecFrame2))==0 and np.dot(vecFrame1, vecFrame2)==0):
            cos=1
        elif((np.linalg.norm(vecFrame1) * np.linalg.norm(vecFrame2))==0):
            cos=0
        else:
            cos = np.dot(vecFrame1, vecFrame2) / (np.linalg.norm(vecFrame1) * np.linalg.norm(vecFrame2))
        return cos

