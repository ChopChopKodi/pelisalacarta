import os.path
import re
import base64

try:
    from python_libtorrent import get_libtorrent
    lt = get_libtorrent()
except Exception, e:
    import libtorrent as lt

class Cache(object):
    CACHE_DIR='.cache'
    def __init__(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        self.path=os.path.join(path, Cache.CACHE_DIR)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)


    def _tname(self, info_hash):
        return os.path.join(self.path, info_hash.upper()+'.torrent')

    def _rname(self, info_hash):
        return os.path.join(self.path, info_hash.upper()+'.resume')

    def save_resume(self,info_hash,data):
        with open(self._rname(info_hash),'wb') as f:
            f.write(data)

    def get_resume(self, url=None, info_hash=None):
        if url:
            info_hash=self._index.get(url)
        if not info_hash:
            return
        rname=self._rname(info_hash)
        if os.access(rname,os.R_OK):
            with open(rname, 'rb') as f:
                return f.read()

    def file_complete(self, torrent):
        info_hash=str(torrent.info_hash())
        nt=lt.create_torrent(torrent)
        tname=self._tname(info_hash)
        with open(tname, 'wb') as f:
            f.write(lt.bencode(nt.generate()))



    def get_torrent(self, url=None, info_hash=None):
        if url:
            info_hash=self._index.get(url)
        if not info_hash:
            return
        tname=self._tname(info_hash)
        if os.access(tname,os.R_OK):
            return tname

    magnet_re=re.compile('xt=urn:btih:([0-9A-Za-z]+)')
    hexa_chars=re.compile('^[0-9A-F]+$')
    @staticmethod
    def hash_from_magnet(m):
        res=Cache.magnet_re.search(m)
        if res:
            ih=res.group(1).upper()
            if len(ih)==40 and Cache.hexa_chars.match(ih):
                return res.group(1).upper()
            elif len(ih)==32:
                s=base64.b32decode(ih)
                return "".join("{:02X}".format(ord(c)) for c in s)
            else:
                raise ValueError('Not BT magnet link')

        else:
            raise ValueError('Not BT magnet link')

