# Coleta de dados de emails :incoming_envelope: :bar_chart:
### Script python para a coleta de dados de email.
Emails são uma fonte de informações muito importante de toda empresa, já que a troca de emails para tratar de diversos assuntos de négocios e rotina de trabalho é constante. Coletar e tratar esses dados é muito importante para gerar insights, relatórios para tomada de decisão.
### Pipline de dados:
1. O script interagi com o usuário para fazer login na conta de email, escolher a caixa de email a ser extraída, escolher o nome do arquivo que armazena os dados.
2. O script coleta os emails da caixa escolhida, analisa cada um dos emails e extrai as informações.
3. Salva os dados em arquivo csv.

### Dependências:
* imaplib 
*  email
* getpass
* sys
* pathlib2
* BeautifulSoup
* base64
* pandas

**OBS: O Script está setado para o servidor de email do gmail, mas pode ser usado em outros servidores imap.**
