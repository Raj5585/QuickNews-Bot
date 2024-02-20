from functools import total_ordering
from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from ratopati_component import Ratopati
from postgres_component import Database
from nagarik_component import Nagarik
from EkantipurComponent import Ekantipur
from RepublicaComponent import RepublicaComponent
from HimalayanTimes_component import Himalayan
from annapurna_component import AnnapurnaComponent
from KtmPost_Component import KtmPost
from mailcomponent import sendMail
from qrlib.QRUtils import display

import json

# from storagebucket import Storage


class DefaultProcess(QRProcess):

    def __init__(self):
        super().__init__()
        # self.default_component = DefaultComponent()
        # self.register(self.default_component)
        self.ratopati_component = Ratopati()
        self.nagarik_component = Nagarik()
        self.ekantipur_component = Ekantipur()
        self.Republica_Component = RepublicaComponent()
        self.Annapurna_component = AnnapurnaComponent()
        self.Himalayan_component = Himalayan()
        self.ktmpost_component = KtmPost()
        self.postgres_component = Database()
        self.mailcomponent = sendMail()
        # self.storage_buckets = Storage()
        self.register(self.ratopati_component)
        self.register(self.nagarik_component)
        self.register(self.ekantipur_component)
        self.register(self.Republica_Component)
        self.register(self.Himalayan_component)
        self.register(self.Annapurna_component)
        self.register(self.ktmpost_component)
        self.register(self.postgres_component)
        self.register(self.mailcomponent)
        # self.register(self.storage_buckets)

    @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):
        self.postgres_component.connection()
        # self.storage_buckets.get_excel_list()

    @run_item(is_ticket=False, post_success=False)
    def before_run_item(self, *args, **kwargs):

        pass

    @run_item(is_ticket=True)
    def execute_run_item(
        self,
        *args,
        **kwargs,
    ):

        Ratopati_data = self.ratopati_component.scrape()
        ekantipur_data = self.ekantipur_component.scrape()
        Himalayan_data = self.Himalayan_component.scrape()
        Nagarik_data = self.nagarik_component.scrape()
        Republica_data = self.Republica_Component.scrape()
        Annapurna_data = self.Annapurna_component.scrape()
        # ktmpost_dat = self.ktmpost_component.scrape()

        display(Ratopati_data)
        display(ekantipur_data)
        display(Himalayan_data)
        display(Nagarik_data)
        display(Republica_data)
        display(Annapurna_data)

        self.postgres_component.sendtodb(newslst=Ratopati_data)
        self.postgres_component.sendtodb(newslst=ekantipur_data)
        self.postgres_component.sendtodb(newslst=Himalayan_data)
        self.postgres_component.sendtodb(newslst=Nagarik_data)
        self.postgres_component.sendtodb(newslst=Republica_data)
        self.postgres_component.sendtodb(newslst=Annapurna_data)

    @run_item(is_ticket=False, post_success=False)
    def after_run_item(self, *args, **kwargs):
        pass

    @run_item(is_ticket=False, post_success=False)
    def after_run(self, *args, **kwargs):
        result = self.postgres_component.fetchData()
        display(
            "------------------------------------------------------------[ RESULT ]---------------------------------------------------------"
        )
        total_news = 0
        for each in result:
            display(json.dumps(each, indent=4, ensure_ascii=False))
            total_news = total_news + 1
        display(
            f"""
-------------------------------------------------------------------------------------------------------------------------------
                            TOTAL NEWS : {total_news}
-------------------------------------------------------------------------------------------------------------------------------
            """
        )
        # self.mailcomponent.send(lst=result)
        self.postgres_component.closeDb()

    def execute_run(self):
        pass
