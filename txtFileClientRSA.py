#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket,sys

# Clé publique
n=0x00a6e992a702c03e238c0b80f3766c0de8c30e4f4dd021da7e53b7b07d716e3082e23a74494e879e5fb76858a220db7820f72de7db615a5c51192b26e704ce4c1cc9c3eae3019ff48ffbcbd5ee941be1f8601e6b77662596b8783d08182b63af8b9c55d0ebc869b6c3576c0c4ea09aef3418e57e31ef86e6c6c866026e5274bef7
d=0x0f5f6bd65df67ec29f5f5fdd0c871f30d4e6387f9e2fc003ea89fc83513328dca521651c6b532a4efe8169c864e651c6177deee0d1b294d6134f5a21e4db6b3f056c989eed9f59785cfe161032e5e12ec2c9e9c2084eb3b6b6f8cd07740d4558852034dd78f906910829ca7bf5bd0e26e7ec8db94ec99f9c7db70f50bc110a41

Host = "localhost"
port = 9876

def readstrCipher(cipherHexStr):
  C = int(cipherHexStr, 16)
  D=pow(C, d, n)
  strdecode = D.to_bytes(128,byteorder='big').lstrip(b'\x00')
  strdecode = str(strdecode, 'utf-8')
  return strdecode
    
def recvstr(sfd):
  msg=sfd.readline().rstrip()
  #print("<= '%s'" % msg)
  return msg
def sendstr(sfd,out):
  #print("=> '%s'" % out)
  sfd.writelines(out+'\n')
  sfd.flush()
try:
  print("Connexion au serveur %s:%d ..." % (Host, port))
  socket=socket.socket()
  socket.connect((Host,port))
  sfd=socket.makefile('rw',encoding='utf-8')
  print("Connexion réussie !")
  prompt=recvstr(sfd)
  while True:
      file_name=input(prompt+"$ ")
      sendstr(sfd,file_name)
      if file_name == "@bye": break
    
      count= int(recvstr(sfd))
      print("Fichier '%s' :\n"%(file_name))
      for block in range(count):
        line = recvstr(sfd)
        print("BLOCK: %s\n"%line)
        line = readstrCipher(line)
        print("BLOCK Déchiffré: \n%s\n"%line)
      print("---------")
  print("Déconnexion")
  socket.close()
except OSError as err:
  print('Erreur:',err,file=sys.stderr)
