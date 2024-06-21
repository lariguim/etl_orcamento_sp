import requests

def get_exchange_rate_on_date():
    endpoint = "https://economia.awesomeapi.com.br/json/daily/USD-BRL/?start_date=20220622&end_date=20220622"
   
    try:
        response = requests.get(endpoint)
        data = response.json()
        
        if data:
            
            exchange_rate = float(data[0]['bid'])
            return exchange_rate
        else:
            print("Não foram encontrados dados de cotação para a data especificada.")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter a taxa de câmbio: {e}")
        return None


if __name__ == "__main__":
    exchange_rate = get_exchange_rate_on_date()
    if exchange_rate:
        print(f"Taxa de câmbio atual: {exchange_rate}")
