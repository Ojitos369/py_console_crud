import csv
import os
from clients.models import Client


class ClientService:
    
    def __init__(self, table_name):
        self.table_name = table_name
        
    def create_client(self, client):
        with open(self.table_name, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerow(client.to_dict())
            

    def read_clients(self):
        with open(self.table_name, 'r') as f:
            reader = csv.DictReader(f, fieldnames = Client.schema())
            
            return list(reader)
    
    def update_client(self, updated_client):
        list_clients = self.read_clients()
        updated_clients = []
        
        for client in list_clients:
            if client['uid'] == updated_client.uid:
                updated_clients.append(updated_client.to_dict())
            else:
                updated_clients.append(client)
        
        self._save_to_disk(updated_clients)
        
    def delete_client(self, client_id):
        list_clients = self.read_clients()
        updated_clients = []
        
        for client in list_clients:
            if client['uid'] != client_id:
                updated_clients.append(client)
        
        self._save_to_disk(updated_clients)
        
    def _save_to_disk(self, clients):
        tmp_table_name = self.table_name + '.tmp'
        with open(tmp_table_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames = Client.schema())
            writer.writerows(clients)
        os.remove('.clients.csv')
        os.rename(tmp_table_name, self.table_name)
        
