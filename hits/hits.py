import numpy
import pandas
from sklearn import import preprocessing

class hits_algorithm(obj):
    def __init__(self, iter=10, early_stop=False, tol=0):
        self.iter = iter
        self.early_stop = early_stop
        self.tol = tol
        self.fin_flag = False

    def update_auths_and_hubs(self, iter_num):
        hub_norm = calc_norm(self.hub_scores)
        auth_norm = calc_norm(self.auth_scores)

        if iter_num != 0:
            if self.early_stop and hub_norm - self.hub_norm_prev < tol:
                self.fin_flag = True

        self.hub_scores = hub_scores / hub_norm
        self.auth_scores = auth_scores / auth_norm

        self.hubs['score'] = self.hub_scores
        self.auths['score'] = self.auth_scores

        self.hub_norm_prev = hub_norm
        self.auth_norm_prev = auth_norm

    def train(self, data, from_links_col='from_links', to_links_col='to_links'):
        self.hub_scores, self.hubs = self.init_scores(data[from_links_col])
        self.auth_scores, self.auths = self.init_scores(data[to_links_col])
        self.hub_norm_prev = 0
        self.auth_norm_prev = 0
        for i in range(self.iter):
            if ! fin_flag:
                self.update_auths_and_hubs(i)
            else:
                break
        return self.hub_scores, self.auth_scores

    def init_scores(self, link_list):
        le = preprocessing.LabelEncoder()
        encoded = le.fit_transform(link_list)
        df = pd.DataFrame(encoded, columns=['id'])
        df['score'] = np.ones(encoded.shape)
        df_scores = df.groupby('id').sum()
        scores = np.array(df_scores).reshape(-1)
        df_scores['titles'] = le.inverse_transform(df_scores['id'])

        return scores, df_scores

    def save_scores(self, filenames=['hub_scores.pkl', 'auth_scores.pkl']):
        self.hub_scores.to_pickle(filenames[0])
        self.auth_scores.to_pickle(filenames[1])


def calc_norm(scores):
        return np.sqrt(np.square(scores).sum())

def main():
    hits = hits_algorithm(iter=10)
    hub_scores, auth_scores = hits.train()
    return hub_scores, auth_scores

if __name__ == '__main__':
    main()
