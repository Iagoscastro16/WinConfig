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
        input("Digite qualquer tecla para sair... ")
    else:
        print(f"[Erro]{resultado.stderr}")

if isAdmin():
    print("Executnado como administrador")
    desativar_firewall()
else:
    print("Solicitando acesso como admin")
    ctypes.windll.shell32.ShellExecuteW(None,
                                    "runas",
                                    sys.executable,
                                    "".join(sys.argv),
                                    None,
                                    1)