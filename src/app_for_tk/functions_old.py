from fileinput import filename
import os
import pandas as pd

from .get_summary_excel import reference_sheet, summary_sheet

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
