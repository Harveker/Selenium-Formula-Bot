import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# 1. Configuração para leitura do CSV local
google_drive_csv_url = "D:/Repositorio/python/Selenium-Formula-Bot/mapsscraper.csv"  # Caminho correto do CSV
chacaras_data = pd.read_csv(google_drive_csv_url)
print(chacaras_data.head())

# 2. Configurar o WebDriver do Edge
edge_driver_path = "D:/Repositorio/python/Selenium-Formula-Bot/msedgedriver.exe"  # Atualize com o caminho correto
options = Options()
options.add_argument("--start-maximized")

# Configurar o serviço e inicializar o WebDriver
service = Service(edge_driver_path)
driver = webdriver.Edge(service=service, options=options)

# 3. Acessar o WhatsApp Web
driver.get("https://web.whatsapp.com/")
print("Escaneie o QR Code para logar no WhatsApp Web")

# 4. Iterar pelos contatos do CSV e enviar mensagens personalizadas
for _, row in chacaras_data.iterrows():
    # Dados da linha atual
    nome_chacara = row.get("Nome", "Chácara")  # Substitua pelo nome da coluna no CSV
    numero = row.get("Telefone", None)  # Número com DDI

    # Verificar se o número não é nulo e é uma string antes de aplicar o strip()
    if isinstance(numero, str):
        numero = numero.strip()
    elif isinstance(numero, float) and pd.notna(numero):
        numero = str(int(numero))  # Converte de float para string se for número válido
    
    # Mensagem personalizada
    mensagem = (
        f"Olá tudo bem? Faço parte do grupo da Fórmula UTFPR, somos um grupo de competição de carros da Universidade Tecnológica do Paraná, "
        f"e para competir precisamos de estadia de uma semana em Piracicaba. Pesquisando, acabamos achando a chácara de vocês, {nome_chacara}.\n\n"
        f"Nossa equipe é formada por cerca de 40 pessoas (pode variar muito até a competição). Se a chácara de vocês tem suporte de estadia por uma semana "
        f"para essa quantidade de pessoas, vocês poderiam nos dar um orçamento? Caso vocês não consigam, saberiam alguma outra chácara desse porte?\n\n"
        f"Estaremos por aí entre os dias 27 de julho de 2025 até o dia 03 de agosto de 2025."
    )

    # Enviar a mensagem pelo WhatsApp Web
    try:
        if numero:
            driver.get(f"https://wa.me/{numero}?text={mensagem}")
            time.sleep(6)  # Aguarde a página carregar completamente

            # Usar WebDriverWait para aguardar a presença do botão de enviar
            send_button = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Iniciar conversa']"))
            )
            send_button.click()
                    # Aguardar até a página carregar, checando a pagina de app vai aparecer.
            send_button = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='usar o WhatsApp Web']"))
            )
            send_button.click()

            print(f"Mensagem enviada para {nome_chacara} ({numero})")
            
            # Aguardar tempo aleatório entre 10 e 20 segundos
            delay = random.randint(10, 20)
            print(f"Aguardando {delay} segundos antes de enviar a próxima mensagem...")
            time.sleep(delay)
        else:
            print(f"Número inválido ou ausente para {nome_chacara}. Pulando...")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {nome_chacara} ({numero}): {e}")
        print("Tentando novamente...")
        time.sleep(5)  # Aguardar um tempo antes de tentar novamente

# Fechar o navegador ao final
driver.quit()