import flask
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='templates')

df2 = pd.read_csv('./model/tmdb.csv')

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])
all_titles = [df2['title'][i] for i in range(len(df2['title']))]


def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix)
    print("cosine sim", cosine_sim)
    idx = indices[title]
    print("idx" , idx)
    sim_scores = list(enumerate(cosine_sim[idx]))
    print("simscores" , sim_scores)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    print("simscores" , sim_scores)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['title'].iloc[movie_indices]
    return_df = pd.DataFrame(columns=['Title'])
    return_df['Title'] = tit
    return return_df


# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')

    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
        if m_name not in all_titles:
            return flask.render_template('notfound.html', name=m_name)
        else:
            result_final = get_recommendations(m_name)
            names = []
            print(result_final)
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])

            return flask.render_template('found.html', movie_names=names, search_name=m_name)


if __name__ == '__main__':
    app.run()
