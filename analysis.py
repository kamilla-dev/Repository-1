import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import re
from datetime import datetime

# Загрузка (предполагаем, что файл загружен в среду Colab)
df = pd.read_csv('message.csv', sep=';', encoding='utf-8-sig', on_bad_lines='warn')

# Предобработка
df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
df['views'] = pd.to_numeric(df['views'], errors='coerce')
df['comments'] = pd.to_numeric(df['comments'], errors='coerce')
df['reactions_total'] = pd.to_numeric(df['reactions_total'], errors='coerce')
df['forwarded'] = pd.to_numeric(df['forwarded'], errors='coerce')
df['forwards'] = pd.to_numeric(df['forwards'], errors='coerce')
df['channel_members_count'] = pd.to_numeric(df['channel_members_count'], errors='coerce')

# Признаки
df['is_media'] = df['message'] == 'MediaMessage'
df['message_len'] = df['message'].apply(lambda x: len(str(x)) if x != 'MediaMessage' else 0)
df['has_comments'] = df['comments'].fillna(0) > 0
df['engagement'] = (df['reactions_total'].fillna(0) + df['comments'].fillna(0)) / df['views'].replace(0, np.nan)

# Извлечение дня недели, часа
df['weekday'] = df['date'].dt.day_name()
df['hour'] = df['date'].dt.hour
df['month'] = df['date'].dt.to_period('M')

# Парсинг реакций (пример)
def parse_reactions(s):
    if pd.isna(s) or s == '':
        return {}
    try:
        return ast.literal_eval(s)
    except:
        return {}

df['reactions_dict'] = df['reactions'].apply(parse_reactions)

# Пример: общее количество реакций по типам
from collections import Counter
all_reactions = Counter()
for d in df['reactions_dict']:
    for k, v in d.items():
        all_reactions[k] += v

print(all_reactions.most_common(10))