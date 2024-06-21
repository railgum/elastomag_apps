from fileinput import filename
import os
from convert_db import convert_excel_to_db


if __name__ == "__main__":
    convert_excel_to_db(
        filename, 'data.db')
