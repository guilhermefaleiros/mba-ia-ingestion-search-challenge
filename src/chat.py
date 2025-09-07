from search import search_documents

def main():
    print("Chat Digite 'sair' para encerrar\n")
    
    while True:
        try:
            pergunta = input("Faça sua pergunta:\n\nPERGUNTA: ")
            
            if pergunta.lower() in ['sair', 'exit', 'quit']:
                print("\n Encerrando o chat...")
                break
            
            if not pergunta.strip():
                print("Por favor, digite uma pergunta válida.\n")
                continue
            
            resposta = search_documents(pergunta)
            
            print(f"RESPOSTA: {resposta}\n")
            print("---\n")
            
        except KeyboardInterrupt:
            print("\n\n Encerrando o chat...")
            break
        except Exception as e:
            print(f" Erro: {e}\n")

if __name__ == "__main__":
    main()