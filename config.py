import subprocess
import ctypes
import os
import sys

def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False        


def desativar_firewall():
    resultado = subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "off"],
                   capture_output=True,
                   text=True
                )
    if resultado.returncode == 0:
        print("[OK]Firewall desativado com sucesso!")
    else:
        print(f"[Erro]{resultado.stderr}")
        print(resultado.stdout)

def ativar_descoberta_rede():
    ativResultado = subprocess.run(["powershell", "-Command", "netsh advfirewall firewall set rule group='Descoberta de rede' new enable=Yes"],
                                   capture_output=True,
                                   text=True)
    if ativResultado.returncode == 0:
        print("Descoberta da Rede ativada com sucesso")
    else:
        print(f"[Erro]{ativResultado.stderr}")
        print(f"[STDOUT]ativResultado.stdout")

if isAdmin():
    print("Executando como administrador")
    desativar_firewall()
    
    ativar_descoberta_rede()
    
    input("Digite qualquer tecla para sair... ")
else:
    print("Solicitando acesso como admin")
    ctypes.windll.shell32.ShellExecuteW(None,
                                    "runas",
                                    sys.executable,
                                    "".join(sys.argv),
                                    None,
                                    1)