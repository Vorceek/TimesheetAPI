def usuario_tem_grupo(usuario, grupos):
    return any(usuario.groups.filter(name=grupo).exists() for grupo in grupos)
