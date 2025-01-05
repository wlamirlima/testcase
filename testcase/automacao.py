import requests
import pandas as pd
from openpyxl import Workbook

def get_users():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter usuários: {e}")
        return []

def get_posts(user_id):
    try:
        response = requests.get(f'https://jsonplaceholder.typicode.com/posts?userId={user_id}')
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter posts para o usuário {user_id}: {e}")
        return []

def calculate_average_character_count(posts):
    if not posts:
        return 0
    total_characters = sum(len(post['body']) for post in posts)
    return total_characters / len(posts)

def generate_report(users):
    data = []
    for user in users:
        posts = get_posts(user['id'])
        avg_char_count = calculate_average_character_count(posts)
        data.append({
            'ID do Usuário': user['id'],
            'Nome do Usuário': user['name'],
            'Quantidade de Posts': len(posts),
            'Média de Caracteres dos Posts': avg_char_count
        })
    
    if data:  
        df = pd.DataFrame(data)
        df.to_excel('relatorio_usuarios.xlsx', index=False)
        print("Relatório gerado com sucesso!")
    else:
        print("Nenhum dado disponível para gerar o relatório.")

def send_email():
    try:
        response = requests.post('https://jsonplaceholder.typicode.com/send-email', json={
            'recipient': 'user@example.com',
            'subject': 'Relatório de Posts de Usuários',
            'body': 'Relatório gerado com sucesso!'
        })
        response.raise_for_status()  
        print("Relatório enviado com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar e-mail: {e}")
        
def main():
    users = get_users()  
    if users:  
        generate_report(users)
        send_email()
    else:
        print("Não foi possível obter dados de usuários. O processo será encerrado.")

if __name__ == '__main__':
    main()
