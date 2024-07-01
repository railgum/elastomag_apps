import os
from fileinput import filename
from convert_db import convert_excel_to_db


if __name__ == "__main__":
    convert_excel_to_db(file_name, 'data.db')
