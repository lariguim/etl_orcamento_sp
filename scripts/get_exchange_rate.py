import requests



def get_exchange_rate_on_date():
    endpoint = f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/?start_date=20220622&end_date=20220622"
   
    try:
        response = requests.get(endpoint)
        data = response.json()
        
        if data:
            # Extrai a taxa de câmbio do primeiro (e único) registro
            exchange_rate = float(data[0]['bid'])
            return exchange_rate
        else:
            print("Não foram encontrados dados de cotação para a data especificada.")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter a taxa de câmbio: {e}")
        return None


