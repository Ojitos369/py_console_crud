import click
from clients.services import ClientService
from clients.models import Client
from tabulate import tabulate
from beautifultable import BeautifulTable

@click.group()
def clients():
    """Manages the clients lifecycle"""
    pass


@clients.command()
@click.option('-n', '--name',
            type = str,
            prompt = True,
            help = 'The client name'
)
@click.option('-c', '--company',
            type = str,
            prompt = True,
            help = 'The client company'
)
@click.option('-e', '--email',
            type = str,
            prompt = True,
            help = 'The client email'
)
@click.option('-p', '--position',
            type = str,
            prompt = True,
            help = 'The client position'
)
@click.pass_context
def create(ctx, name, company, email, position):
    """Create a new client"""
    client = Client(name, company, email, position)
    client_service = ClientService(ctx.obj['clients_table'])
    client_service.create_client(client)


@clients.command()
@click.pass_context
def read(ctx):
    """List all clients"""
    client_service = ClientService(ctx.obj['clients_table'])
    clients = client_service.read_clients()
    headers = ['ID', 'NAME', 'COMPANY', 'EMAIL', 'POSITION']
    clients = [[c['uid'], c['name'], c['company'], c['email'], c['position']] for c in clients]
    # Normal Mode
    #click.echo(f'ID  |  NAME  |  COMPANY  |  EMAIL  |  POSITION')
    #click.echo('*' * 100)
    #for client in clients:
        #click.echo(f'{client["uid"]}  |  {client["name"]}  |  {client["company"]}  |  {client["email"]}  |  {client["position"]}')
        
    # Tabulate Mode
    click.echo(tabulate(clients, headers=headers))
    
    # BeautifulTable Mode
    #table = BeautifulTable()
    #table.column_headers = headers
    #for client in clients:
        #table.append_row(client)
    #click.echo(table)
    click.echo('-' * 100)


@clients.command()
@click.option('-cid', '--client_id',
            type = str,
            prompt = True,
            help = 'The client id'
)
@click.pass_context
def update(ctx, client_id):
    """Update a client"""
    client_service = ClientService(ctx.obj['clients_table'])
    clients_list = client_service.read_clients()
    
    client = [c for c in clients_list if c['uid'] == client_id]
    
    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)
        click.echo('Client updated')
    else:
        click.echo('Client not found')


@clients.command()
@click.option('-cid', '--client_id',
            type = str,
            prompt = True,
            help = 'The client id'
)
@click.pass_context
def delete(ctx, client_id):
    """Delete a client"""
    client_service = ClientService(ctx.obj['clients_table'])
    clients_list = client_service.read_clients()
    
    client = [c for c in clients_list if c['uid'] == client_id]
    
    if client:
        client_service.delete_client(client_id)
        click.echo('Client deleted')
    else:
        click.echo('Client not found')


def _update_client_flow(client):
    click.echo('Leave empty if you dont want to modify the value')
    client.name = click.prompt('New name: ', type = str, default = client.name)
    client.company = click.prompt('New company: ', type = str, default = client.company)
    client.email = click.prompt('New email: ', type = str, default = client.email)
    client.position = click.prompt('New position: ', type = str, default = client.position)
    return client

all = clients

