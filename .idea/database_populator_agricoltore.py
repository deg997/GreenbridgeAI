import random
import string
import requests
from geopy.geocoders import Nominatim
from random import uniform
from random import randint
from faker import Faker
from datetime import datetime, timedelta

fake=Faker('it_IT')
certificati=['ISO 14001', 'FairTrade', 'Certificazione bio', 'GlobalG.A.P.', 'Carbon Trust Standard']

def genera_coordinate_italia():
    # Genera casualmente coordinate geografiche in Italia
    lat = uniform(35.5, 47.0)  # Latitudine approssimativa dell'Italia
    lon = uniform(6, 18.5)   # Longitudine approssimativa dell'Italia
    return lat, lon

def coordinate_a_indirizzo(lat, lon):
    # Utilizza Nominatim per ottenere l'indirizzo testuale dalle coordinate
    geolocator = Nominatim(user_agent="database_populator.py")
    location = geolocator.reverse((lat, lon), language='it')

    # Estrai e restituisci l'indirizzo
    address = location.address if location else "Indirizzo non disponibile"
    return address

def genera_indirizzo():
    lat, lon = genera_coordinate_italia()
    indirizzo = coordinate_a_indirizzo(lat, lon)
    return indirizzo

def is_dati_validi(agricoltore_data):
    # Aggiungi qui i tuoi criteri di validazione
    if 'Italia' in agricoltore_data['indirizzo_bottega'] and len(agricoltore_data['indirizzo_bottega']) > len('Italia') and len(agricoltore_data['nome_bottega'])<=30:
        return True
    # Aggiungi altri criteri se necessario

    return False

def genera_mediumlob():
    dati_binari_casuali = bytes(''.join(random.choices(string.ascii_letters + string.digits, k=1024)), 'utf-8')
    return dati_binari_casuali

def generate_portafoglio():
    portafoglio_data = {
        'credito': 0    #se si vuole simulare: random.randint(0, 5000)
    }

    return portafoglio_data

def generate_agricoltore():
    while True:
        agricoltore_data = {
            'nome': fake.first_name(),
            'email': fake.email(),
            'pwd': fake.password(length=16),
            'nome_bottega': fake.company(),
            'indirizzo_bottega': genera_indirizzo()
        }

        if is_dati_validi(agricoltore_data):
            return agricoltore_data

def generate_certificato():
    oggi=datetime.now()
    data_casuale=oggi + timedelta(days=random.randint(0, 365))

    certificato_data = {
        'nome': random.choice(certificati),
        'data_scadenza': data_casuale,
        'scansione': genera_mediumlob()
    }

    return certificato_data

num_agricoltori=2

for _ in range(num_agricoltori):
    portafoglio_data=generate_portafoglio()
    agricoltore_data=generate_agricoltore()
    certificato_data=generate_certificato()

    print("INSERT INTO portafoglio (credito) VALUES({});".format(portafoglio_data['credito']))
    print("""SET @portafoglio_id=LAST_INSERT_ID();""")
    print("""INSERT INTO agricoltore (nome, email, pwd, nome_bottega, indirizzo_bottega, id_portafoglio) VALUES (\""""+agricoltore_data['nome']+"""\", \""""+agricoltore_data['email']+"""\", \""""+agricoltore_data['pwd']+"""\", \""""+agricoltore_data['nome_bottega']+"""\", \""""+agricoltore_data['indirizzo_bottega']+"""\", @portafoglio_id);""")
    print("""SET @agricoltore_id=LAST_INSERT_ID();""")
    print("""INSERT INTO certificato (nome, data_scadenza, scansione, id_agricoltore) VALUES (\""""+certificato_data['nome']+"""\", \"{}\", \"{}\", @agricoltore_id);""".format(certificato_data['data_scadenza'].strftime('%d-%m-%Y'), certificato_data['scansione']))
