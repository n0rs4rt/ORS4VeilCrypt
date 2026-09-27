import urllib.request, json

def consultar_update():
    version_actual = "v1.0.0"
    url = "https://api.github.com/repos/n0rs4rt/ORS4VeilCrypt/releases/latest"
    
    try:
        respuesta = urllib.request.urlopen(url)
    
        consulta = respuesta.read()
        datos = json.loads(consulta)
        version = str(datos["tag_name"])
        
        if version != version_actual:
            return True

        else:
            return False

    except:
        return False
    
