# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta 4
# Copyright 2015 tvalacarta@gmail.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
# This file is part of pelisalacarta 4.
#
# pelisalacarta 4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelisalacarta 4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pelisalacarta 4.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------
# Configuracion
# ------------------------------------------------------------

from core import config
from core.item import Item
from core import logger

DEBUG = True
CHANNELNAME = "configuracion"


def mainlist(item):
    logger.info("tvalacarta.channels.configuracion mainlist")

    itemlist = []
    itemlist.append(Item(channel=CHANNELNAME, title="Preferencias", action="settings", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="", action="", folder=False))

    itemlist.append(Item(channel=CHANNELNAME, title="Ajustes especiales", action="", folder=False))

    if not config.OLD_PLATFORM:
        itemlist.append(Item(channel="novedades", title="   Ajustes de la sección 'Novedades'", action="menu_opciones", folder=True))
        itemlist.append(Item(channel="buscador",  title="   Ajustes del buscador global", action="opciones", folder=True))

    if config.is_xbmc():
        itemlist.append(Item(channel=item.channel, action="updatebiblio",
                             title="   Buscar nuevos episodios y actualizar biblioteca", folder=False))

    itemlist.append(Item(channel=CHANNELNAME, title="   Comprobar actualizaciones", action="check_for_updates", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="   Añadir o Actualizar canal/conector desde una URL", action="menu_addchannels"))
    itemlist.append(Item(channel=item.channel, action="", title="", folder=False))

    if not config.OLD_PLATFORM:

        itemlist.append(Item(channel=CHANNELNAME, title="Ajustes por canales", action="", folder=False))

        itemlist.append(Item(channel="allpeliculas",  title="   Configuración del canal 'allpeliculas'", action="configuracion", folder=False))
        itemlist.append(Item(channel="cinefox",  title="   Configuración del canal 'cinefox'", action="configuracion", folder=False))
        itemlist.append(Item(channel="cinetux",  title="   Configuración del canal 'cinetux'", action="configuracion", folder=False))
        itemlist.append(Item(channel="descargasmix",  title="   Configuración del canal 'descargasmix'", action="configuracion", folder=False))
        itemlist.append(Item(channel="hdfull",  title="   Configuración del canal 'hdfull'", action="settingCanal", folder=False))
        itemlist.append(Item(channel="inkapelis",  title="   Configuración del canal 'inkapelis'", action="configuracion", folder=False))
        itemlist.append(Item(channel="megaforo",  title="   Configuración del canal 'megaforo'", action="settingCanal", folder=False))
        itemlist.append(Item(channel="megahd",  title="   Configuración del canal 'megahd'", action="settingCanal", folder=False))
        itemlist.append(Item(channel="oranline",  title="   Configuración del canal 'oranline'", action="configuracion", folder=False))
        itemlist.append(Item(channel="pelisdanko",  title="   Configuración del canal 'pelisdanko'", action="configuracion", folder=False))
        itemlist.append(Item(channel="pelispedia",  title="   Configuración del canal 'pelispedia'", action="configuracion", folder=False))
        itemlist.append(Item(channel="pordede",  title="   Configuración del canal 'pordede'", action="settingCanal", folder=False))
        itemlist.append(Item(channel="verseriesynovelas",  title="   Configuración del canal 'verseriesynovelas'", action="configuracion", folder=False))

    return itemlist


def check_for_updates(item):
    from core import updater
  
    try:
        version = updater.checkforupdates()
        if version:
            import xbmcgui
            yes_pressed = xbmcgui.Dialog().yesno( "Versión "+version+" disponible" , "¿Quieres instalarla?" )
      
            if yes_pressed:
                item = Item(version=version)
                updater.update(item)

    except:
        pass

def settings(item):
    config.open_settings()


def updatebiblio(item):
    logger.info("pelisalacarta.channels.ayuda updatebiblio")

    import library_service
    library_service.main()


def menu_addchannels(item):
    logger.info("pelisalacarta.channels.configuracion menu_addchannels")
    itemlist = []
    itemlist.append(Item(channel=CHANNELNAME, title="# Copia de seguridad automática en caso de sobrescritura", action="", text_color="green"))
    itemlist.append(Item(channel=CHANNELNAME, title="Añadir o actualizar canal", action="addchannel", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Añadir o actualizar conector", action="addchannel", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Mostrar ruta de carpeta para copias de seguridad", action="backups", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Eliminar copias de seguridad guardadas", action="backups", folder=False))

    return itemlist


def addchannel(item):
    from platformcode import platformtools
    from core import filetools
    import time, os
    logger.info("pelisalacarta.channels.configuracion addchannel")
    
    tecleado = platformtools.dialog_input("", "Introduzca la URL")
    if not tecleado:
        return
    logger.info("pelisalacarta.channels.configuracion url=%s" % tecleado)

    local_folder = config.get_runtime_path()
    if "canal" in item.title:
        local_folder = filetools.join(local_folder, 'channels')
        folder_to_extract = "channels"
        info_accion = "canal"
    else:
        local_folder = filetools.join(local_folder, 'servers')
        folder_to_extract = "servers"
        info_accion = "conector"

    # Detecta si es un enlace a un .py o .xml (pensado sobre todo para enlaces de github)
    try:
        extension = tecleado.rsplit(".",1)[1]
    except:
        extension = ""

    files = []
    zip = False
    if extension == "py" or extension == "xml":
        filename = tecleado.rsplit("/",1)[1]
        localfilename = filetools.join(local_folder, filename)
        files.append([tecleado, localfilename, filename])
    else:
        import re
        from core import scrapertools
        # Comprueba si la url apunta a una carpeta completa (channels o servers) de github
        if re.search(r'https://github.com/[^\s]+/'+folder_to_extract, tecleado):
            try:
                data = scrapertools.downloadpage(tecleado)
                matches = scrapertools.find_multiple_matches(data, '<td class="content">.*?href="([^"]+)".*?title="([^"]+)"')
                for url, filename in matches:
                    url = "https://raw.githubusercontent.com" + url.replace("/blob/", "/")
                    localfilename = filetools.join(local_folder, filename)
                    files.append([url, localfilename, filename])
            except:
                import traceback
                logger.info("Detalle del error: %s" % traceback.format_exc())
                platformtools.dialog_ok("Error", "La url no es correcta o no está disponible")
                return
        else:
            filename = 'new%s.zip' % info_accion
            localfilename = filetools.join(config.get_data_path(), filename)
            files.append([tecleado, localfilename, filename])
            zip = True

    logger.info("pelisalacarta.channels.configuracion localfilename=%s" % localfilename)
    logger.info("pelisalacarta.channels.configuracion descarga fichero...")
    
    try:
        if len(files) > 1:
            lista_opciones = ["No", "Sí", "Sí (Sobrescribir todos)"]
            overwrite_all = False
        from core import downloadtools
        for url, localfilename, filename in files:
            result = downloadtools.downloadfile(url, localfilename, continuar=False)
            if result == -3:
                if len(files) == 1:
                    dyesno = platformtools.dialog_yesno("El archivo ya existe", "Ya existe el %s %s." \
                                                        " ¿Desea sobrescribirlo?" % (info_accion, filename))
                else:
                    if not overwrite_all:
                        dyesno = platformtools.dialog_select("El archivo %s ya existe, ¿desea sobrescribirlo?"
                                                             % filename, lista_opciones)
                    else:
                        dyesno = 1
                # Diálogo cancelado
                if dyesno == -1:
                    return
                # Caso de carpeta github, opción sobrescribir todos
                elif dyesno == 2:
                    overwrite_all = True
                elif dyesno:
                    hora_folder = "Copia seguridad [%s]" % time.strftime("%d-%m_%H-%M", time.localtime())
                    backup = filetools.join(config.get_data_path(), 'backups', hora_folder, folder_to_extract)
                    if not filetools.exists(backup):
                        os.makedirs(backup)
                    import shutil
                    shutil.copy2(localfilename, filetools.join(backup, filename))
                    result = downloadtools.downloadfile(url, localfilename, continuar=True)
                else:
                    if len(files) == 1:
                        return
                    else:
                        continue
    except:
        import traceback
        logger.info("Detalle del error: %s" % traceback.format_exc())
        return


    if zip:
        try:
            # Lo descomprime
            logger.info("pelisalacarta.channels.configuracion descomprime fichero...")
            from core import ziptools
            unzipper = ziptools.ziptools()
            logger.info("pelisalacarta.channels.configuracion destpathname=%s" % local_folder)
            unzipper.extract(localfilename, local_folder, folder_to_extract, True, True)
        except:
            import traceback
            logger.info("Detalle del error: %s" % traceback.format_exc())
            # Borra el zip descargado
            filetools.remove(localfilename)
            platformtools.dialog_ok("Error", "Se ha producido un error extrayendo el archivo")
            return
		
        # Borra el zip descargado
        logger.info("pelisalacarta.channels.configuracion borra fichero...")
        filetools.remove(localfilename)
        logger.info("pelisalacarta.channels.configuracion ...fichero borrado")

    platformtools.dialog_ok("Éxito", "Actualización/Instalación realizada correctamente")


def backups(item):
    from platformcode import platformtools
    from core import filetools
    logger.info("pelisalacarta.channel.configuracion backups")

    ruta = filetools.join(config.get_data_path(), 'backups')
    ruta_split = ""
    if "ruta" in item.title:
        heading = "Ruta de copias de seguridad"
        if not filetools.exists(ruta):
            folders = "Carpeta no creada"
        else:
            folders = str(len(filetools.listdir(ruta))) + " copia/s de seguridad guardadas"
        if len(ruta) > 55:
            ruta_split = ruta[55:]
            ruta = ruta[:55]
        platformtools.dialog_ok(heading, ruta, ruta_split, folders)
    else:
        if not filetools.exists(ruta):
            platformtools.dialog_ok("La carpeta no existe", "No hay copias de seguridad guardadas")
        else:
            dyesno = platformtools.dialog_yesno("Las copias de seguridad se eliminarán", "¿Está seguro?")
            if dyesno:
                import shutil
                shutil.rmtree(ruta, ignore_errors=True)
