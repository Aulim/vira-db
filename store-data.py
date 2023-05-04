import datetime
import pandas as pd

def load_old_csv(category: str):
    fname = 'data/viraindo_'+ category + '.csv'
    df = pd.read_csv(fname)
    return df

def get_today_date():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+7))).strftime("%Y-%m-%d")

def get_prev_month():
    return (datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+7))) - datetime.timedelta(weeks=2)).strftime("%Y-%m")


def save_split_old_new(df: pd.DataFrame, category: str):
    date = get_today_date()
    old_data = df.query('date != @date')
    new_data = df.query('date == @date').reset_index(drop=True)
    old_fname = 'data/viraindo_' + get_prev_month() + '.pkl'
    old_data.to_pickle(old_fname)
    new_fname = 'data/viraindo_'+ category + '.csv'
    new_data.to_csv(new_fname, index=False)
    assert len(df) == len(old_data) + len(new_data)

if __name__ == '__main__':
    df = load_old_csv('notebook')
    save_split_old_new(df, 'notebook')
    # df = pd.read_pickle('data/viraindo_2023-04.pkl')
    # print(df.head())