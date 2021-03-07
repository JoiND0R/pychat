import socket
import asyncore
import random
import pickle
import time
import sys, os
import json
import logging
from threading import Thread

BUFFERSIZE = 2048

def user(arr):
    if os.path.exists(name+'/data_file.json') == False:
        data_users = open(name+"/data_file.json", "w+")
        data_users.write("{}")
        data_users.close()
    if arr[0] == 'login':
        with open(name+"/data_file.json", "r") as read_file:
            data = json.load(read_file)
        if len(data.keys()) >= 0:
            if data.get(arr[2][0]):
                if data.get(arr[2][0]).get('password') == arr[2][1]:
                    MainServer.logs('LOGIN','пользователь авторизован')
                    conn.send((json.dumps(['setinfo',['id', data.get(arr[2][0]).get('id')],['nick', data.get(arr[2][0]).get('nick')],['auth', True],['room',name]]).encode()))
                    user(['add',arr[1],arr[2][0]])
                else:
                    MainServer.logs('LOGIN','пользователь ввёл неправильный пароль')
                    conn.send((json.dumps(['notify',['Авторизация'],['Неверный пароль'],['ERROR']]).encode()))
                

            else:
                MainServer.logs('LOGIN','создание пользователя')

                
                nick = arr[2][0]
                
                if len(arr[2][0]) > 20:
                    i = 0
                    nick = ''
                    for sim in arr[2][0]:
                        if i != 20:
                            nick = nick+sim
                            i = i + 1
                            
                if nick.lower() == 'server':
                    nick = nick+str(random.randint(0,999))
                

                if nick == 'gr4shin' or nick == 'joind0r':
                    admin = True
                    date = 'Я одмен какая вам разница?'
                else:
                    date = arr[2][2]
                    admin = False
                data[nick] ={
                    'id':arr[1],
                    'nick':nick,
                    'password':arr[2][1],
                    'admin':admin,
                    'promokod':'',
                    'date':date
                }
                        
                with open(name+"/data_file.json", "w") as write_file:
                    json.dump(data, write_file)
                conn.send((json.dumps(['setinfo',['id', data.get(nick).get('id')],['nick', data.get(nick).get('nick')],['auth', True],['room',name]]).encode()))
                conn.send((json.dumps(['notify',['Регистрация'],['Добро пожаловать '+str(nick)+'!'+"\nДля помощи пиши в чате /help"],['SUCCESS']]).encode()))
                user(['add',arr[1],arr[2][0]])
                
    if arr[0] == 'get_info':
        with open(name+"/data_file.json", "r") as read_file:
            data = json.load(read_file)
        return data
      
    if arr[0] == 'add':
      userid = arr[1]
      usernick = arr[2]
      users[userid] = [['id',userid],['nick',usernick]]

    if arr[0] == 'changepassword':
        with open(name+"/data_file.json", "r") as read_file:
                data = json.load(read_file)
        getinfo = user(['get_info'])
        for key in getinfo:
            if (getinfo[key])['id'] == arr[1]:
                data[(getinfo[key])['nick']] ={
                    'id':(getinfo[key])['id'],
                    'nick':(getinfo[key])['nick'],
                    'password':arr[2],
                    'admin':(getinfo[key])['admin'],
                    'promokod':(getinfo[key])['promokod'],
                    'date':(getinfo[key])['date']
                    }
                with open(name+"/data_file.json", "w") as write_file:
                    json.dump(data, write_file)
                return " пароль изменён!"
        
      
    if arr[0] == 'setadmin':
        users_get = user(['get_info'])
        if users_get.get(arr[1]):
            with open(name+"/data_file.json", "r") as read_file:
                data = json.load(read_file)
            if data[arr[1]]['admin'] == True:
                return " пытался добавить уже администратора "
            else:
                data[arr[1]] ={
                    'id':users_get[arr[1]]['id'],
                    'nick':users_get[arr[1]]['nick'],
                    'password':users_get[arr[1]]['password'],
                    'admin':True,
                    'promokod':users_get[arr[1]]['promokod'],
                    'date':users_get[arr[1]]['date']
                    }
                with open(name+"/data_file.json", "w") as write_file:
                    json.dump(data, write_file)
                return " добавил нового администратора "
        else:
            return ' пытался дать права администратора '
      
    if arr[0] == 'removeadmin':
      users_get = user(['get_info'])
      if users_get.get(arr[1]):
          with open(name+"/data_file.json", "r") as read_file:
              data = json.load(read_file)
          if data[arr[1]]['admin'] == False:
              return " пытался убрать права администратора у обычного простолюдина "
          else:
              data[arr[1]] ={
                  'id':users_get[arr[1]]['id'],
                  'nick':users_get[arr[1]]['nick'],
                  'password':users_get[arr[1]]['password'],
                  'admin':False,
                  'promokod':users_get[arr[1]]['promokod'],
                  'date':users_get[arr[1]]['date']
                  }
              with open(name+"/data_file.json", "w") as write_file:
                  json.dump(data, write_file)
              return " убрал с поста администратора "
      else:
          return ' пытался отобрать права администратора '  
          
    if arr[0] == 'promokod':
        if arr[1] == 'admin':
            users_promo = user(['get_info'])
            for key in users_promo:
                if (users_promo[key])['id'] == arr[2]:
                    nick = (users_promo[key])['nick']
                    break    
            user(['setadmin',nick])
            return " кому-то выпала ОПКА ЕБАТь"
        else:
            users_promo = user(['get_info'])
            with open(name+"/data_file.json", "r") as read_file:
                data = json.load(read_file)
            for key in data:
                if (data[key])['id'] == arr[2]:
                    nick = (data[key])['nick']
                    break    
            if data[nick]['promokod'] != "":
                return " попытки исчерпаны... [;c] "
            else:
                data[nick] ={
                    'id':data[nick]['id'],
                    'nick':data[nick]['nick'],
                    'password':data[nick]['password'],
                    'admin':data[nick]['admin'],
                    'promokod':arr[1],
                    'date':data[nick]['date']
                    }
                with open(name+"/data_file.json", "w") as write_file:
                    json.dump(data, write_file)
                return " кому-то выпало "+str(arr[1])
            
    if arr[0] == 'remove':
        if users.get(arr[1]):
            users.pop(arr[1])
            sendmess(['chat','Server',"пользователь покинул нас [ID"+str(arr[1])+"]"])
      
    if arr[0] == 'list':
      online = 'Онлайн: '
      for key in users:
        online = str(online)+' ID'+str(key) 
      return online 
    
def sendmess(arr, clear = False):
    
  userid = arr[1]
  nick = ''
  mess = arr[2]
  remove = []
  import datetime    
  now = datetime.datetime.now()   
  time = now.strftime("%H:%M")
  
  if userid == 'Server':
      nick = 'Server'
  
  users = user(['get_info'])

  for key in users:
      if (users[key])['id'] == userid:
          nick = (users[key])['nick']
          break
    
  for i in outgoing:
      try:
          i.send((json.dumps(['pong',userid]).encode()))
      except Exception as e:
          MainServer.logs('ERROR [pong]',e)
          remove.append(i)
          continue
  for r in remove:
          outgoing.remove(r)


  if len(chat_main) > 200:
      chat_main.clear()
      sendmess(['chat','Server',"Чат был сброшен из-за большого количества сообщений",True])
  
  chat_main.append([nick,mess,time])
    
  if os.path.exists(name+'/chat.json') == False:
      if os.path.exists(name) == False:
          os.mkdir(name)
  with open(name+"/chat.json", "r") as read_file:
      data = json.load(read_file)
  data['chat'] = chat_main
  with open(name+"/chat.json", "w") as data_chat:
      json.dump(data,data_chat)



          
  MainServer.logs('CHAT','['+str(nick)+'] '+str(mess))
  remove = []   
  for i in outgoing:
      try:
          i.send((json.dumps(['chat',chat_main]).encode()))
      except Exception as e:
          MainServer.logs('ERROR [chat]',e)
          remove.append(i)
          continue
  for r in remove:
      outgoing.remove(r)

class MainServer(asyncore.dispatcher):
  def logs(type,text):
    print('# [Server]'+'['+str(type)+'] '+str(text))
      
  def __init__(self,serverAddr ,port):
    asyncore.dispatcher.__init__(self)
    
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
    
    self.socket.bind((serverAddr, port))
    self.listen(10)
    MainServer.logs('INFO','Cервер успешно запущен')
    sendmess(['chat','Server','ping'])  
    
  def handle_accept(self):
    global conn, name
    playerid = random.randint(1, 100)
    conn, addr = self.accept()
    outgoing.append(conn)
    nick = 'ID'+str(playerid)
    MainServer.logs('INFO','[id'+str(playerid)+'] пользователь подключился')
    sendmess(['chat','Server',"пользователь присоединлся к нам [ID"+str(playerid)+"]"])
    conn.send((json.dumps(['setinfo',['id', playerid],['nick', nick],['auth', False],['room',name]]).encode()))
    SecondaryServer(conn)
    
  def exit(self):
      self.socket.close()
        
class SecondaryServer(asyncore.dispatcher_with_send):
  def handle_read(self):
    recievedData = self.recv(BUFFERSIZE)
    try:
      recievedData = json.loads((recievedData).decode())
    except Exception as e:
      MainServer.logs('ERROR in CONNECT','Потеряна связь с пользователем... '+str(e)+' ('+str(recievedData)+')')
      recievedData = ['disconnect','']
      
    if recievedData[0] == 'login':
        user(recievedData)
      
    elif recievedData[0] == 'disconnect':
      self.close()
      user(['remove',recievedData[1]])
      MainServer.logs('INFO','[id'+str(recievedData[1])+'] пользователь отключился')
      sendmess(['chat','Server',"пользователь покинул нас [ID"+str(recievedData[1])+"]"])
      
    elif recievedData[0] == 'ping':
      self.send(json.dumps(['ping',recievedData[2]]).encode())
      
    elif recievedData[0] == 'chat':
      id = recievedData[1]
      cmd = recievedData[2].split()

      # УВЕДОМЛЕНИЕ
      
      if cmd[0] == '/say':
          if len(cmd) == 1:
              self.send(json.dumps(['toast',"Примеры использование команды \n/say ВСЕ ГАНДОНЫ\n/say кто прочитал тот..."]).encode())
          users = user(['get_info'])
          for key in users:
              if (users[key])['id'] == id:
                  admin = (users[key])['admin']
                  break
          if admin and len(cmd) > 1:
              for i in outgoing:
                  try:
                      text = ' '.join(cmd[1:]) 
                      i.send(json.dumps(['say',text]).encode())
                  except Exception as e:
                      MainServer.logs('ERROR [say]',e)
                      remove.append(i)
                      continue

      # РЕСТАРТ СЕРВА
      
      elif cmd[0] == '/erase':
          users = user(['get_info'])
          for key in users:
              if (users[key])['id'] == id:
                  admin = (users[key])['admin']
                  break
          if admin:
              sendmess([recievedData[0],"УВЕДОМЛЕНИЕ","Сервер сейчас сбросится"])
              time.sleep(3)
              
              remove = []
              for i in outgoing:
                  try:
                      i.close()
                      remove.append(i)
                  except Exception as e:
                      MainServer.logs('ERROR [erase]',e)
                      remove.append(i)
                      continue
              for r in remove:
                  outgoing.remove(r)
                  
              os.remove(name+'/data_file.json')
              os.remove(name+'/chat.json')
              os.rmdir(name)
              
              os.system('cls||clear')  
              os.execv(sys.executable, [sys.executable] + sys.argv)

              global ms
              ms.exit()
              sys.exit()    

      # ПОМОЩЬ
                      
      elif cmd[0] == '/help':
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        help = "/time - Показать время \n/random ЧИСЛО ЧИСЛО \n/cp, /changepassword, /changepass - Смена пароля \n/info НИК - Информация о пользователе \n/online - онлайн \n/music URL - музыка всем"    
        if admin:
            help = str(help)+"\n/say - отправить уведомлние всем \n/erase - сбросить сервер \n/setadmin, /sa - дать админку \n/removeadmin, /ra - снять админку \n/clear - очистка чата"
            
        self.send(json.dumps(['toast',help]).encode())

      # ЛИЧНЫЕ СООБЩЕНИЯ  
        
      elif cmd[0] == '/we':
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        if admin and len(cmd) > 1:
            sendmess([recievedData[0],'Server',str(admin_nick)+user(['setadmin',cmd[1]])+str(cmd[1]),True])

      # АДМИНКА  
        
      elif cmd[0] == '/setadmin' or cmd[0] == '/sa':
        if len(cmd) == 1:
            self.send(json.dumps(['toast',"Примеры использование команды \n/sa gr4shin"]).encode())
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        if admin and len(cmd) > 1:
            sendmess([recievedData[0],'Server',str(admin_nick)+user(['setadmin',cmd[1]])+str(cmd[1]),True])

      elif cmd[0] == '/removeadmin' or cmd[0] == '/ra':
        if len(cmd) == 1:
            self.send(json.dumps(['toast',"Примеры использование команды \n/ra gr4shin"]).encode())
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        if admin and len(cmd) > 1:
            sendmess([recievedData[0],'Server',str(admin_nick)+user(['removeadmin',cmd[1]])+str(cmd[1]),True])

      # ОЧИСТКА ЧАТА
      
      elif cmd[0] == '/clear':
          users = user(['get_info'])
          for key in users:
              if (users[key])['id'] == id:
                  admin = (users[key])['admin']
                  admin_nick = (users[key])['nick']
                  break
          if admin and len(cmd) == 1:
              chat_main.clear()
              sendmess([recievedData[0],'Server',"Чат был очищен администратором "+str(admin_nick),True])
          if admin and len(cmd) == 2:
              if len(chat_main) < int(cmd[1]):
                  chat_main.clear()
                  sendmess([recievedData[0],'Server',"Чат был очищен администратором "+str(admin_nick),True])
              else:
                  index = 0
                  while int(cmd[1]) > index:
                      chat_main.pop(-1)
                      index = index + 1
                  sendmess([recievedData[0],'Server', str(cmd[1])+" сообщений было очищено администратором "+str(admin_nick),True])

      # СМЕНА ПАРОЛЯ
          
      elif cmd[0] == '/cp' or cmd[0] == '/changepass' or cmd[0] == '/changepassword':
          if len(cmd) == 1:
              self.send(json.dumps(['toast',"Примеры использование команды \n/cp P@$Sw04d\n/changepass qwerty12Q"]).encode())
          if len(cmd) > 1 and len(cmd) < 3:
              self.send((json.dumps(['notify',['Смена пароля'],[user(['changepassword',id,cmd[1]])],['SUCCESS']]).encode()))

      # ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ
      
      elif cmd[0] == '/info' or cmd[0] == '/information' or cmd[0] == '/getinfo':
          if len(cmd) == 1:
              self.send(json.dumps(['toast',"Примеры использование команды \n/info gr4shin\n/info ivan322"]).encode())
          if len(cmd) > 1 and len(cmd) < 3:
              info = 'Информация о пользователе:'
              getinfo = user(['get_info'])
              for key in getinfo:
                  if (getinfo[key])['nick'] == cmd[1]:
                      info = info + "\n" + 'ID: ' + str(getinfo[key]['id']) + "\n" + 'Никнейм: ' + str(getinfo[key]['nick']) + "\n" + 'Администратор: ' + str(getinfo[key]['admin']) + "\n" + 'Дата регистрации: ' + str(getinfo[key]['date'])
                    
                      
                      break
              sendmess(recievedData)
              sendmess([recievedData[0],'Server',info])

      # ОНЛАЙН
      
      elif cmd[0] == '/online':
        online = user(['list'])
        sendmess([recievedData[0],'Server',online])

      elif cmd[0] == '/aliexpress':
          
          promokod = {0:"admin",1:"прекрасное нихуя",2:"прекрасное нихуя",3:"прекрасное нихуя",4:"прекрасное нихуя",5:"прекрасное нихуя"}
          import random
          kek = random.randint(0,5)
          
          sendmess([recievedData[0],'Server',user(['promokod',promokod.get(kek),id])])  

      # ВРЕМЯ
      
      elif cmd[0] == '/time':
          import datetime
          now = datetime.datetime.now()
          sendmess(recievedData)
          sendmess([recievedData[0],'Server',now.strftime("%d.%m.%Y %H:%M")])
        
      # РАНДОМ
      
      elif cmd[0] == '/random':
          if len(cmd) == 1:
              self.send(json.dumps(['toast',"Примеры использование команды \n/random 0 10\n/random 50 100"]).encode())
          if len(cmd) == 3:
              import random
              sendmess(recievedData)
              sendmess([recievedData[0],'Server',random.randint(int(cmd[1]),int(cmd[2]))])
              
      # Музыка
      
      elif cmd[0] == '/music':
          if len(cmd) == 1:
              self.send(json.dumps(['toast',"Примеры использование команды \n/music URL.mp3"]).encode())
          if len(cmd) == 2:
              sendmess([recievedData[0],'Server','Кто-то включил музыку'])
              for i in outgoing:
                  try:
                      text = ' '.join(cmd[1:]) 
                      i.send(json.dumps(['music',cmd[1]]).encode())
                  except Exception as e:
                      MainServer.logs('ERROR [music]',e)
                      remove.append(i)
                      continue
            

      else:
        sendmess(recievedData)
      
    else:
      MainServer.logs('WARNING','пришла другая информация: '+str(recievedData))
try:
  global serverAddr, ms, name
  outgoing = []  
  users = {}
  developer = 'gr4shin'
  chat_main = []  
  MainServer.logs('INFO','Запуск...')
  if len(sys.argv) == 2:
      name = sys.argv[1]
  else:
      name = "local"
  if len(sys.argv) == 3:
      serverAddr = sys.argv[2]
      name = sys.argv[1]
  else:
      serverAddr = "127.0.0.1"
  if len(sys.argv) == 4:
      port = int(sys.argv[3])
      serverAddr = sys.argv[2]
      name = sys.argv[1]
  else:
      port = 4321
  if os.path.exists(name+'/data_file.json') == False:
      if os.path.exists(name) == False:
          os.mkdir(name)
      data_users = open(name+"/data_file.json", "w+")
      data_users.write("{}")
      data_users.close()
      
  if os.path.exists(name+'/chat.json') == False:
      if os.path.exists(name) == False:
          os.mkdir(name) 
      with open(name+"/chat.json", "w") as data_chat:
          json.dump({"chat":[]},data_chat)
      chat = {"chat":[]}
  else:
      try:
          MainServer.logs('INFO','Загрузка чата')
          with open(name+"/chat.json", "r") as read_file:
              chat = json.load(read_file)
              chat_main = chat['chat']
      except OSError as e:
          MainServer.logs('ERROR [load chat]',e)
  ms = MainServer(serverAddr,port)
  MainServer.logs('INFO','Данные для подключений ' + str(serverAddr)+":"+str(port))
  asyncore.loop()
except OSError as e:
  MainServer.logs('ERROR',e)
finally:
  MainServer.logs('INFO','остановлен.')
  input('Press ENTER to close...')
