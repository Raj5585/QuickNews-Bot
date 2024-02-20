from qrlib.QRComponent import QRComponent
from qrlib.QRStorageBucket import QRStorageBucket
from qrlib.QREnv import QREnv
from qrlib.QRUtils import display
import pandas as pd


class Storage(QRComponent):
    def __init__(self):
        super().__init__()
        self.bucket = QRStorageBucket("teststore")

    def get_excel_list(self):
        try:
            for item in self.bucket.list_all_files():
                name = item['file_display_name']
                if '/' in name:
                    continue
                if not name.endswith('.csv'):
                    self.move_file(item,"Error")
                    continue
            
                self.bucket.download_file(item)
                exceldf = pd.read_excel(f"{QREnv.DEFAULT_STORAGE_LOCATION}\\{item['file_display_name']}")
                display(" ------------file downloaded--------------")
        except Exception as e:
            self.run_item.logger.info("Reading excel error, moving to Error")
            raise e

    

    