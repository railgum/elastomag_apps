from fileinput import filename
import os
import pandas as pd
import sqlite3


# переменные в отдельный файл?
# добавить исключения
# добавить логирование
# запись в файл вынести отдельно
# база данных(SQLite?)

path_files = None
files = os.listdir(path_files)
nessesary_sheets = ['Наряд']
skip_cols = ['Мастер', 'Брак шт.', 'доп. отметка']
header_row = 1
df_total = pd.DataFrame()


# scip_cols если нужно пропустить столбцы
def summary_sheet(files, nessesary_sheets, use_cols, header_row):
    concat_list = []
    for file in files:
        if file.endswith('.xlsx'):
            excel_file = pd.ExcelFile(file)
            sheets = excel_file.sheet_names
            for _ in sheets:
                df = excel_file.parse(
                    sheet_name=nessesary_sheets[0],
                    header=header_row,
                    # usecols=lambda x: x not in skip_cols
                    usecols=use_cols
                )
        concat_list.append(df)
    return concat_list


# Функция создания справки(внутренний документ компании)


def reference_sheet(df, index, columns=None, values=None, aggfunc='sum', zero_values_column=None):
    pt = pd.pivot_table(df,
                        index=index,
                        values=values,
                        aggfunc=aggfunc)
    pt = pt[pt[zero_values_column] != 0]  # фильтруем нулевые значения
    return pt


index = ['Наименование детали']
values = ['Годных шт.', 'Стоимость вул-ции']
aggfunc = ['sum']
column_filter_empty = 'Годных шт.'


# функция преобразования Excel-файла в БД Sqlite

def convert_excel_to_db(file_name, db_name):
    db = sqlite3.connect(db_name)

    dfs = pd.read_excel(file_name, sheet_name=None)
    for table, df in dfs.items():
        df.to_sql(table, db, if_exists='replace')


if __name__ == "__main__":
    concat_list = summary_sheet(files, nessesary_sheets, skip_cols, header_row)
    df_total = pd.concat(concat_list, ignore_index=True)
    df_total['Дата'] = df_total['Дата'].dt.strftime('%d.%m.%Y')
    df_total = df_total[df_total['Прессовщик'] != 0]
    df_total.reset_index(drop=True, inplace=True)

    with pd.ExcelWriter(filename) as writer:
        reference_sheet(df_total, ['Дата', 'Прессовщик']).to_excel(
            writer, sheet_name='справка')
        df_total.to_excel(writer, sheet_name='сводная', index=False)
