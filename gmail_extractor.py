import imaplib 
from pathlib2 import Path
import email 
import getpass
import sys 
from getBody import get_email_body
import pandas as pd

class GMAIL_EXTRACTOR():

    def initializeVariables(self):
        self.usr = ""
        self.pwd = ""
        self.mail = object
        self.mailbox = ""
        self.mailCount = 0
        self.dataName = ""
        self.destFolder = Path.cwd() / 'dados'
        self.data = []
        self.ids = []
        self.idsList = []

    def getLogin(self):
        print("Por favor, insira seu login do Gmail.")
        self.usr = input("Email: ")
        self.pwd = getpass.getpass()


    def attemptLogin(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)

        if self.mail.login(self.usr, self.pwd):
           print('\n-----------------------------------------------------------------------------------------------\n')
           print("Logon SUCCESSFUL")
           print('\n-----------------------------------------------------------------------------------------------\n')
           self.dataName = input("Escolha um nome para o arquivo: ")
               
           return True
        else:
           print('\n-----------------------------------------------------------------------------------------------\n')
           print("Logon FAILED")
           return False
    
    def attemptLogout(self):
        self.mail.close()
        msgserver, _ = self.mail.logout()
        if(msgserver):
            print('\n-----------------------------------------------------------------------------------------------\n')
            print('Logout SUCCESSFUL')


    def selectMailbox(self):
        options = {}
        data = self.mail.list()
        data[1].pop(1)
        for count, folder in enumerate(data[1], start=1):
            _, name = folder.decode('utf-8').split(' "/" ')
            options[count] = name
    
        print('\n--- Escolha a caixa de e-mail ---\n')
        for key, value in options.items():
            print(f'{key} ---> {value}')
        
        option = int(input("Digite o número da caixa de e-mail: "))
        self.mailbox = options[option]

        bin_count = self.mail.select(self.mailbox)[1]
        self.mailCount = int(bin_count[0].decode("utf-8"))
        return True if self.mailCount > 0 else False

    def searchThroughMailbox(self):
        type, self.data = self.mail.search(None, "ALL")
        self.ids = self.data[0]
        self.idsList = self.ids.split()

    def checkIfUsersWantsToContinue(self):
        print('\n-----------------------------------------------------------------------------------------------\n')
        print("Foram encontados "+str(self.mailCount)+" emails na caixa "+self.mailbox+".")
        print('\n-----------------------------------------------------------------------------------------------\n')
        return True if input("Deseja continuar extraindo todos os e-mails em "+str(self.destFolder)+"? (y/N) ").lower().strip()[:1] == "y" else False
    
    
    def parseEmails(self):
        mailList = []
        emailInfoFilePath =  str(self.destFolder / self.dataName ) + '.csv'

        for anEmail in self.data[0].split():
            jsonOutput = {}
            type, self.data = self.mail.fetch(anEmail, '(UID RFC822)')
             # id do EMAIL
            raw = self.data[0][0]
            raw_str = raw.decode("utf-8")
            uid = raw_str.split()[2]
            jsonOutput['UID'] = uid

            # Assunto, remetente, data e corpo
            raw = self.data[0][1]
            try:
                raw_str = raw.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    raw_str = raw.decode("ISO-8859-1") # ANSI support
                except UnicodeDecodeError:
                    try:
                        raw_str = raw.decode("ascii") # ASCII ?
                    except UnicodeDecodeError:
                        pass

            msg = email.message_from_string(raw_str)
            
            jsonOutput['Assunto'] = msg['subject']
            jsonOutput['Remetente'] = msg['from']
            jsonOutput['Data'] = msg['date']
            
             # Body #
            jsonOutput['Corpo'] = get_email_body(msg) 
            
            mailList.append(jsonOutput)
            
        # Salvar dados 
        print(mailList)
        df = pd.DataFrame.from_records(mailList)
        df.to_csv(emailInfoFilePath, sep=';', index=False, encoding='utf-8')

        print('\n-----------------------------------------------------------------------------------------------\n')
        print("Extração concluída!")

    def __init__(self):
        self.initializeVariables()
        self.getLogin()
        if self.attemptLogin():
            not self.selectMailbox() and sys.exit()
        else:
            sys.exit()

        not self.checkIfUsersWantsToContinue() and sys.exit()
        self.searchThroughMailbox()
        self.parseEmails()
        self.attemptLogout()

if __name__ == "__main__":
    run = GMAIL_EXTRACTOR()
