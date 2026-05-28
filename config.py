import subprocess
import ctypes
import sys
import os,socket
from datetime import datetime

def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False        
    



def escrever_log(status, mensagem=None):
    with open("config.log", "a") as arquivo:
        if mensagem != None:  
                arquivo.write(f"{status} = {mensagem}\n")
                
        else:
                arquivo.write(f"{status}\n")


def coletar_info_maquina():
    computador = socket.gethostname()
    escrever_log("computador", computador)
    
    user_ip = socket.gethostbyname(computador)
    escrever_log("IP", user_ip)

    usuario_logado = os.getlogin()
    escrever_log("Usuario", usuario_logado)

    data_atual = datetime.now()
    escrever_log("Data", data_atual)

    escrever_log("---")


def desativar_firewall():
    resultado = subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "off"],
                   capture_output=True,
                   text=True
                )
    if resultado.returncode == 0:
        print("[OK]Firewall desativado com sucesso!\n")
        escrever_log("firewall","Ok" )
    else:
        print(f"[Erro]{resultado.stderr}")
        print(resultado.stdout)
        escrever_log("firewall", "Erro")



def ativar_descoberta_rede():
    ativResultado = subprocess.run(["powershell", "-Command", "netsh advfirewall firewall set rule group='Descoberta de rede' new enable=Yes"],
                                   capture_output=True,
                                   text=True)
    if ativResultado.returncode == 0:
        print("Descoberta da Rede ativada com sucesso")
        escrever_log("descoberta", "Ok")
    else:
        print(f"[Erro]{ativResultado.stderr}")
        print(f"[STDOUT]{ativResultado.stdout}")
        escrever_log("descoberta", "Erro")



def compartilhaImpressora():
    comparImpress = subprocess.run(["Powershell", "-Command", "netsh advfirewall firewall set rule group='Compartilhamento de arquivo e impressora' new enable=yes"],
                                   capture_output=True,
                                   text=True,)
    
    if comparImpress.returncode == 0:
        print("Impressora compartilhada com sucesso")
        escrever_log("comp.impressora", "Ok")
    else:
        print(f"[Erro]{comparImpress.stderr}")
        print(f"[STDOUT]{comparImpress.stdout}")
        escrever_log("comp.impressora","Erro")

if isAdmin():
    print("Executando como administrador")

    coletar_info_maquina()

    desativar_firewall()
    
    ativar_descoberta_rede()

    compartilhaImpressora()

    input("Digite qualquer tecla para sair... ")

else:

    print("Solicitando acesso como admin")
    ctypes.windll.shell32.ShellExecuteW(None,
                                    "runas",
                                    sys.executable,
                                    "".join(sys.argv),
                                    None,
                                    1)