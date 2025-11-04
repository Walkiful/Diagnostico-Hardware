import psutil
import platform
from datetime import datetime

def get_size(bytes, suffix="B"):
    """Converte bytes em KB, MB, GB etc."""
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def gerar_relatorios():
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    relatorio_txt = "diagnostico.txt"
    relatorio_html = "diagnostico.html"

    # Coleta de dados
    sistema = platform.system()
    versao = platform.version()
    arquitetura = platform.machine()
    processador = platform.processor()
    cpu_fisica = psutil.cpu_count(logical=False)
    cpu_logica = psutil.cpu_count(logical=True)
    uso_cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    interfaces = psutil.net_if_addrs()

    # Gera relatório TXT
    with open(relatorio_txt, "w", encoding="utf-8") as f:
        f.write("==== RELATÓRIO DE DIAGNÓSTICO DE HARDWARE ====\n")
        f.write(f"Data e hora: {data_atual}\n")
        f.write(f"Sistema: {sistema} {platform.release()}\n")
        f.write(f"Versão: {versao}\n")
        f.write(f"Arquitetura: {arquitetura}\n")
        f.write(f"Processador: {processador}\n\n")
        f.write("---- CPU ----\n")
        f.write(f"Núcleos físicos: {cpu_fisica}\n")
        f.write(f"Núcleos lógicos: {cpu_logica}\n")
        f.write(f"Uso atual da CPU: {uso_cpu}%\n\n")
        f.write("---- MEMÓRIA ----\n")
        f.write(f"Total: {get_size(mem.total)}\n")
        f.write(f"Disponível: {get_size(mem.available)}\n")
        f.write(f"Uso: {mem.percent}%\n\n")
        f.write("---- DISCO ----\n")
        f.write(f"Tamanho total: {get_size(disco.total)}\n")
        f.write(f"Uso: {disco.percent}%\n\n")
        f.write("---- REDE ----\n")
        for interface, enderecos in interfaces.items():
            f.write(f"Interface: {interface}\n")
            for e in enderecos:
                if e.family.name == 'AF_INET':
                    f.write(f"  IP: {e.address}\n")
                elif e.family.name == 'AF_PACKET':
                    f.write(f"  MAC: {e.address}\n")
            f.write("\n")
        f.write("==== FIM DO RELATÓRIO ====\n")

    # Gera relatório HTML
    with open(relatorio_html, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Diagnóstico de Hardware</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background-color: #0e1117;
    color: #d1d5db;
    padding: 20px;
}}
h1 {{ color: #38bdf8; }}
h2 {{ color: #a855f7; }}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}}
td, th {{
    border: 1px solid #374151;
    padding: 8px;
}}
th {{
    background-color: #1f2937;
}}
</style>
</head>
<body>
<h1>Relatório de Diagnóstico de Hardware</h1>
<p><b>Data e hora:</b> {data_atual}</p>
<h2>CPU</h2>
<table>
<tr><th>Propriedade</th><th>Valor</th></tr>
<tr><td>Processador</td><td>{processador}</td></tr>
<tr><td>Núcleos físicos</td><td>{cpu_fisica}</td></tr>
<tr><td>Núcleos lógicos</td><td>{cpu_logica}</td></tr>
<tr><td>Uso atual</td><td>{uso_cpu}%</td></tr>
</table>

<h2>Memória</h2>
<table>
<tr><td>Total</td><td>{get_size(mem.total)}</td></tr>
<tr><td>Disponível</td><td>{get_size(mem.available)}</td></tr>
<tr><td>Uso</td><td>{mem.percent}%</td></tr>
</table>

<h2>Disco</h2>
<table>
<tr><td>Total</td><td>{get_size(disco.total)}</td></tr>
<tr><td>Uso</td><td>{disco.percent}%</td></tr>
</table>

<h2>Rede</h2>
<table>
<tr><th>Interface</th><th>Endereços</th></tr>""")
        for interface, enderecos in interfaces.items():
            f.write(f"<tr><td>{interface}</td><td>")
            for e in enderecos:
                if e.family.name == 'AF_INET':
                    f.write(f"IP: {e.address}<br>")
                elif e.family.name == 'AF_PACKET':
                    f.write(f"MAC: {e.address}<br>")
            f.write("</td></tr>")
        f.write("""
</table>
</body>
</html>""")

    print("✅ Relatórios gerados com sucesso:")
    print(f"   - {relatorio_txt}")
    print(f"   - {relatorio_html}")

if __name__ == "__main__":
    gerar_relatorios()
