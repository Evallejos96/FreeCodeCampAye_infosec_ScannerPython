import socket
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    # -------------------------------------------------
    # Validación de IP o Hostname
    # -------------------------------------------------
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        # Ver si es IP inválida o hostname inválido
        if is_ip(target):
            return "Error: Nombre de host no válido"
        else:
            return "Error: Dirección IP no válida"

    start_port, end_port = port_range

    # -------------------------------------------------
    # Escaneo de puertos
    # -------------------------------------------------
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    # Si no es verbose, retornar lista
    if not verbose:
        return open_ports

    # -------------------------------------------------
    # MODO VERBOSE
    # -------------------------------------------------
    # Si el target era IP, intento obtener hostname
    display_host = target
    if is_ip(target):
        try:
            display_host = socket.gethostbyaddr(ip)[0]
        except:
            display_host = target

    # Encabezado del output
    lines = []
    lines.append(f"Open ports for {display_host} ({ip})")
    lines.append("PORT     SERVICE")

    for port in open_ports:
        service = ports_and_services.get(port, "")
        lines.append(f"{port:<9}{service}")

    return "\n".join(lines)


# -------------------------------------------------
# Valida si el string es una IP válida
# -------------------------------------------------
def is_ip(value):
    parts = value.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit():
            return False
        if not 0 <= int(p) <= 255:
            return False
    return True
