import numpy as np
import pandas as pd
from sklearn import preprocessing

class hits_algorithm(object):
    def __init__(self, iter=10, early_stop=False, tol=0):
        self.iter = iter
        self.early_stop = early_stop
        self.tol = tol
        self.fin_flag = False

    def update_auths_and_hubs(self, data, iter_num):
        auth_norm = calc_norm(self.auth_scores)
        print('auth_norm = {}'.format(auth_norm))

        print('grad = {}'.format(auth_norm - self.auth_norm_prev))
        if iter_num != 0:
            if self.early_stop and auth_norm - self.auth_norm_prev < tol:
                self.fin_flag_auths = True

        self.auth_scores = self.auth_scores / auth_norm

        self.auths['score'] = self.auth_scores

        self.hub_norm_prev = hub_norm
        self.auth_norm_prev = auth_norm
        data = pd.merge(data.drop(columns=['score']), auths)

        hub_norm = calc_norm(self.hub_scores)
        print('hub_norm = {}'.format(hub_norm))

        print('grad = {}'.format(hub_norm - self.hub_norm_prev))
        if iter_num != 0:
            if self.early_stop and hub_norm - self.hub_norm_prev < tol:
                self.fin_flag_hubs = True
        self.hub_scores = self.hub_scores / hub_norm
        self.hubs['score'] = self.hub_scores
        data = pd.merge(data.drop(columns=['score']), auths)
        return data, auths, hubs

    def train(
            self,
            data,
            from_links_col='from_link',
            to_links_col='to_link'):
        data['score'] = np.ones(len(df))

        self.hub_norm_prev = 0
        self.auth_norm_prev = 0
        for i in range(self.iter):
            print('iter={}'.format(i))
            if not self.fin_flag_auths and not self.fin_flag_hubs:
                auths, hubs = get_auths_and_hubs(data)
                data, auths, hubs = self.update_auths_and_hubs(data, i)
            else:
                break
        print('finish training')
        self.hubs = self.hubs.sort_values(by='score', ascending=False)
        self.auths = self.auths.sort_values(by='score', ascending=False)
        return self.hubs, self.auths

    def init_scores(self, df, colname):
        df_scores = df.groupby('id').sum()
        df_scores[colname] = le.inverse_transform(df_scores.index)
        df_scores = df_scores.ix[:,[colname, 'score']]
        scores = np.array(df_scores['score'])
        return scores, df_scores

    def get_auths_and_hubs(self, df):
        auths = df.groupby(to_links_col).sum()
        hubs = df.groupby(from_links_col).sum()
        return auths, hubs


    def save_scores(
            self,
            filenames=['hub_scores.csv', 'auth_scores.csv'],
            format='csv'):
        if format == 'csv':
            self.hubs.to_csv(filenames[0], index=False)
            self.auths.to_csv(filenames[1], index=False)
        elif format == 'pickle':
            self.hub_scores.to_pickle(filenames[0])
            self.auth_scores.to_pickle(filenames[1])


def calc_norm(scores):
        return np.sqrt(np.square(scores).sum())

@click.command()

def main():
    recipe_ingredients = pd.read_csv(
        'data/train.csv',
        delimiter=',',
        names=[
            'id',
            'qid1',
            'qid2',
            'question1',
            'question2',
            'is_duplicate'])

    hits = hits_algorithm(iter=10)
    hub_scores, auth_scores = hits.train(
            data=recipe_ingredients,
            from_links_col='qid2',
            to_links_col='qid1')
    return hub_scores, auth_scores

if __name__ == '__main__':
    main()
