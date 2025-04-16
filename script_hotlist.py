import requests
import csv
import time

#Começar populando os arquivos cpf.csv e cnpj.csv com os dados a serem consultados
# Configurações
R6_URL = "http://api.resolucao6.com.br/v1/fraudevidence/search"

#Para gerar o token usar a API de login do R6
HEADERS_R6 = {
    "Authorization": "Bearer ...",
    "Content-Type": "application/json"
}

def read_document(path):
    documents = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            national_registration = row.get("value")
            if national_registration:
                documents.append(national_registration.strip())
    return documents

def search_r6(doc):
    payload = {"searchData": {"cpf":doc}}
    try:
        response = requests.post(R6_URL, headers=HEADERS_R6, json=payload)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        for item in results:
            if item.get("role") in [1, 2]:
                return True
        return False
    except Exception as e:
        print(f"[R6] Erro com {doc}: {e}")
        return "Erro"
    
def search_r6_cnpj(doc):
    payload = {"searchData": {"cnpj":doc}}
    try:
        response = requests.post(R6_URL, headers=HEADERS_R6, json=payload)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        for item in results:
            if item.get("role") in [1, 2]:
                return True
        return False
    except Exception as e:
        print(f"[R6] Erro com {doc}: {e}")
        return "Erro"

def process_documents(docs):
    results = []
    for doc in docs:
        print(f"Consultando {doc}...")
        r6_flag = search_r6(doc)
        append_row_to_csv(doc, r6_flag, "cpfresult.csv")
    return results

def process_documents_cnpj(docs):
    results = []
    for doc in docs:
        print(f"Consultando {doc}...")
        r6_flag = search_r6_cnpj(doc)
        append_row_to_csv(doc, r6_flag, "cnpjresultfinal.csv")
    return results
            
def create_csv_with_header(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Documento", "R6"])

def append_row_to_csv(documento, r6_value, path):
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([documento, r6_value])
        
# --- Execução ---
if __name__ == "__main__":
    #Leitura dos arquivos iniciais com os dados a serem pesquisados
    cpf = read_document("cpferro.csv")
    cnpj = read_document("cnpjerro.csv")
    #Depois da primeira execução remover essas duas linhas que criam o arquivo inicial para não sobrescrever
    create_csv_with_header("cpfresult.csv")
    create_csv_with_header("cnpjresultfinal.csv")
    
    #Processamento dos dados e inclusão do resultado no arquivo
    results_cpf = process_documents(cpf)
    results_cnpj = process_documents_cnpj(cnpj)
    print("Processamento concluído.")
