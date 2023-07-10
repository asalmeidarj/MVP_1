def formatDatetimeISO8601(date):
    ano = date.year
    mes = date.month
    dia = date.day
    mes = f"0{mes}" if mes < 10 else mes
    dia = f"0{dia}" if dia < 10 else dia

    horas = date.hour
    minutos = date.minute
    segundos = date.second
    minutos = f"0{minutos}" if minutos < 10 else minutos
    segundos = f"0{segundos}" if segundos < 10 else segundos

    return f"{ano}-{mes}-{dia}T{horas}:{minutos}:{segundos}-03:00"

def formatDatetime(date):
    ano = date.year
    mes = date.month
    dia = date.day
    mes = f"0{mes}" if mes < 10 else mes
    dia = f"0{dia}" if dia < 10 else dia

    return f"{ano}-{mes}-{dia}"