from django.core.management.base import BaseCommand
from .LoadData import Get_Sync, Get_Async

class Command(BaseCommand):
    def handle(self, *args, **options):
        gs=Get_Sync()
        gas=Get_Async()
        if(gs.load_data() and gas.load_data()):
            print("Sync DB Successful")
            return
        print("Sync DB Failed")