import math
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import pow

class hits_algorithm(obj):
    def __init__(self, spark, iter=10, early_stop=False, tol=0):
        self.spark = spark
        self.iter = iter
        self.early_stop = early_stop
        self.tol = tol
        self.fin_flag = False

    def train(self, data, from_links_col='from_links', to_links_col='to_links'):
        self.hub_scores, self.hubs = self.init_scores(data, from_links_col)
        self.auth_scores, self.auths = self.init_scores(data, tolinks_col)
        self.hub_norm_prev = 0
        self.auth_norm_prev = 0
        for i in range(self.iter):
            print('iter={}'.format(i))
            if ! fin_flag:
                self.update_auths_and_hubs(i)
            else:
                break
        print('finish training')
        self.hub_scores = self.hubs.join(
                self.hub_scores,
                self.hubs.id == self.hub_scores.id
                ).select(self.hubs.id, self.hubs.title, self.hub_scores.score)

        self.auth_scores = self.auths.join(
                self.auth_scores,
                self.auths.id == self.auth_scores.id
                ).select(self.auths.id, self.auths.title, self.auth_scores.score)
        return self.hub_scores, self.auth_scores

    def update_auths_and_hubs(self, iter_num):
        hub_norm = calc_norm(self.hub_scores)
        auth_norm = calc_norm(self.auth_scores)

        print('grad = {}'.format(hub_norm - self.hub_norm_prev))
        iter_num != 0:
            if self.early_stop and hub_norm - self.hub_norm_prev < tol:
                self.fin_flag = True

        self.hub_scores = self.hub_scores.select(
                self.hub_scores.id,
                self.hub_scores / hub_norm)
        self.auth_scores = self.auth_scores.select(
                self.auth_scores.id,
                self.auth_scores / auth_norm)
        self.hub_norm_prev = hub_norm
        self.auth_norm_prev = auth_norm

    def calc_norm(self, df):
        norm = (math.sqrt(
            df.select('id', pow(df.score, df.score))
            .groupBy().sum('pow').first()[0]))
        return norm

    def init_scores(self, data, links_col):
        out_col = ''.format(links_col, '_idx')
        indexer = StringIndexer(inputCol=links_col, outputCol=out_col)
        model = indexer.fit(data)
        indexed = model.transform(data)
        scores = (indexed.select(out_col).groupBy(out_col)
                .count()
                .withColumnRenamed('count', 'score'))
        return scores, indexed


def main(spark):
    data = spark.read.load(data_path)
    hits = hits(spark, iter=10)
    hits.train(data)


if __name__ == "__main__":

    # Initialization of SparkSession
    spark = SparkSession.builder \
        .appName('hits_algorithm') \
        .config('spark.debug.maxToStringFields', 1000) \
        .config('spark.sql.shuffle.partitions', 10).getOrCreate()

   data_path = 's3://research-data.ap-northeast-1/datas/skills/recipe_ingredieents'
   main(spark, data_path)
