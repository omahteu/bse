from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from selenium import webdriver
from dotenv import load_dotenv
from email import encoders
from time import sleep
import smtplib
import json
import re
import os

load_dotenv()
inicio = 1
fim = 10
pgdw = '\ue00f'
url = os.getenv('URL')
titulo = os.getenv('TITLE')
mail = os.getenv('MAIL')



def send_email(remetente, destinatario, senha, assunto, corpo, anexo):
    # Configurações
    email_from = str(remetente).lower()
    email_to = str(destinatario).lower()
    senha = senha

    # Criando a mensagem
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = assunto
    corpo_email = corpo
    msg.attach(MIMEText(corpo_email, 'plain'))

    # Adicionando o anexo
    nome_arquivo = anexo
    caminho_arquivo = './curriculo.pdf'
    with open(caminho_arquivo, 'rb') as arquivo:
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload(arquivo.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename=nome_arquivo)
        msg.attach(payload)

    # Enviando o email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_from, senha)
    texto = msg.as_string()
    server.sendmail(email_from, email_to, texto)
    server.quit()



def registros(titulo, email):
    # Crie um dicionário com suas variáveis
    novo_dado = {'enviado': {'titulo': titulo, 'email': email}}

    # Nome do arquivo JSON
    nome_arquivo = 'meu_arquivo.json'

    # Tente ler o arquivo JSON existente e adicionar os novos dados
    try:
        with open(nome_arquivo, 'r') as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver vazio, crie um novo dicionário
        dados = []

    # Adicione o novo dado aos dados existentes
    dados.append(novo_dado)

    # Escreva os dados de volta ao arquivo JSON
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)





def verifica_registro(titulo, email):
    # Nome do arquivo JSON
    nome_arquivo = 'registros.json'

    # Tente ler o arquivo JSON existente
    try:
        with open(nome_arquivo, 'r') as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver vazio, retorne False
        return False

    # Verifique se o título e o email já existem nos dados
    for registro in dados:
        if registro['enviado']['titulo'] == titulo and registro['enviado']['email'] == email:
            return True

    # Se o título e o email não foram encontrados, retorne False
    return False





aprovados = []

driver = webdriver.Edge()

driver.get(url)

try:
    
    ActionChains(driver)\
        .send_keys(pgdw)\
        .perform()
    
    sleep(1)
        
    for i in range(inicio, fim+1):
        obj = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div/div[1]/div[2]/div/article[{i}]/div[2]/span')
        
        sleep(3)

        if obj.text == "ACTIVE":
            
            sleep(2)
            
            obj.click()
            
            sleep(2)
            
            ActionChains(driver)\
                .send_keys('\ue015')\
                .perform()
                
            sleep(1)
            
            titulo = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/main/div/div[2]/section/a/h2').text
            

            
            email = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/main/div/div[2]/section/address/section/dl/div[2]/dd/a').text
            
            
            
            regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            emails = re.findall(regex_email, email)
            
            if emails:
                
                dados = (titulo, emails[0])

                aprovados.append(dados)
                
                
                registros(titulo, emails[0])
                
                sleep(1)
            
            sleep(5)

    sleep(2)

    driver.quit()
except NoSuchElementException:
    print("Falha nos Componentes")
except ElementClickInterceptedException:
    print("Falha no Scroll")
finally:
    # print(aprovados)
    # send_email()
    driver.quit()
