# =============================================================================================================================
#
# NOTE: THIS IS A SAMPLE CODE.
#
# SOLUTION: Create your own new python code and copy this code and paste to you python file and edit config and path.
#
# =============================================================================================================================

import os
import json
import time

from flask import Flask, request, Response

from dq.base_scanner import BaseScanner
from my_d_scanner import MyDailyScanner


app = Flask(__name__)

cur_dir = os.getcwd()


@app.route('/')
def index():
    return 'Hello World ^^'

@app.route('/scanner/<model>/<info_spec>', methods=["GET"])
def scan(model, info_spec):
    response = None
    try:
        info = False
        if info_spec == 'full':
            info = True
        elif info_spec not in ['full', 'short']:
            raise Exception(f"Invalid value of 'info_spec': {info_spec}, 'info_spec' can be 'full' or 'short'")

        if model == 'SET100':
            dataset_path = f"{cur_dir.replace('/source', '')}/datasets/SET"
            columns_master = ['DATETIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
            datetime_format = '%m/%d/%Y'

            symbols = load_data(dataset_path, columns_master, datetime_format)

            scanner = MyDailyScanner(symbols)
            scanner.add_indi()
                        
            # start scanning
            scanned_symbols = scanner.scan(info=info)
            scanned_symbols = scanned_symbols.round(4) # แก้ตัวเลข 4 เป็นเลขอื่น เพื่อปัดเศษทศนิยม
            response = scanned_symbols.to_json(orient="records")

    except Exception as e:
        msg = f"Scan error: {e}"
        response = app.response_class(
            response=msg,
            status=500
        )
        pass

    return response

# ===============================================================================================

def load_data(dataset_path, columns_master, datetime_format):
    symbols = BaseScanner.load_data(dataset_path=dataset_path
                                    , columns_master=columns_master
                                    , datetime_format=datetime_format)
    return symbols
        

def start(config):
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    config = None
    
    start(config)


    