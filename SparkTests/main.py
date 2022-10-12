import multiprocessing
import os
from multiprocessing import Process, Queue
import time
from queue import Empty

import numpy as np
import pyspark
import xgboost
from pyspark.mllib.tree import GradientBoostedTrees, GradientBoostedTreesModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.sql import SparkSession

from sklearn.linear_model import LinearRegression


def run_process_timeout_wrapper(function, args, timeout):
    def foo(n, out_q):
        res = function(*n)
        out_q.put(res)  # to get result back from thread target

    result_q = Queue()
    p = Process(target=foo, args=(args, result_q))
    p.start()

    try:
        x = result_q.get(timeout=timeout)
    except Empty as e:
        p.terminate()
        raise multiprocessing.TimeoutError("Timed out after waiting for {}s".format(timeout))

    p.terminate()
    return x


def my_function(fun):
    print("Started")
    t1 = time.time()

    trainingData = (np.random.rand(5, 1500), np.random.rand(5, 1))
    pairs = []
    for x,y in zip(*trainingData):
        pairs.append(LabeledPoint(y, x)) # note, it's val, features

    spark: SparkSession = SparkSession.builder.master("local[1]").appName("SparkByExamples.com").getOrCreate()

    rdd = spark.sparkContext.parallelize(pairs)
    pol = GradientBoostedTrees.trainRegressor(rdd, categoricalFeaturesInfo={}, numIterations=3)

    #pol = LinearRegression()
    # pol = xgboost.XGBRegressor()

    #pol.fit(*trainingData)
    print("Took ", time.time() - t1)
    pol.predict(np.random.rand(2, 1500))

    return 5


if __name__ == '__main__':
    t1 = time.time()
    pol = xgboost.XGBRegressor()
    pol.fit(np.random.rand(50, 150000), np.random.rand(50, 1))
    print("Took ", time.time() - t1)

    my_function(None)

    t1 = time.time()
    res = run_process_timeout_wrapper(my_function, (None,), 6)

    print("Res ", res, " Time ", time.time() - t1)