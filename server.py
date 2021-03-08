import socket
import asyncore
import random
import pickle
import time
import sys, os
import json, re
import logging
from threading import Thread

BUFFERSIZE = 4096

enabled_commands = {
    'kick':{
        'enabled':False,
        },
    'say':{
        'enabled':True,
        },
    'erase':{
        'enabled':True,
        },
    'help':{
        'enabled':True,
        },
    'commands':{
        'enabled':True,
        },
    'we':{
        'enabled':True,
        },
    'setadmin':{
        'enabled':True,
        },
    'removeadmin':{
        'enabled':True,
        },
    'clear':{
        'enabled':True,
        },
    'time':{
        'enabled':True,
        },
    'music':{
        'enabled':True,
        },
    'connected':{
        'enabled':True,
        },
    'online':{
        'enabled':True,
        },
    'information':{
        'enabled':True,
        },
    'random':{
        'enabled':True,
        }
    }


    #
    #   КОМАНДЫ
    #
    
def command(user_socket, id, nick, type, arg = False):
    if enabled_commands.get(type) == None:
        user_socket.send(json.dumps(['toast',"Неизвестная команда, /help для помощи"]).encode())
        type = ''
        
    elif enabled_commands[type]['enabled'] == False:
        user_socket.send(json.dumps(['toast',"Команда отключена"]).encode())
        type = ''
        
    elif type == 'say' and enabled_commands[type]['enabled']:
        if len(arg) == 1:
            user_socket.send(json.dumps(['toast',"Примеры использование команды \n/say ВСЕ ГАНДОНЫ\n/say кто прочитал тот..."]).encode())
            
        admin = False
        sayUsers = user(['get_info'])
        for key in sayUsers:
            if (sayUsers[key])['id'] == id:
                admin = (sayUsers[key])['admin']
                break
            
        if admin and len(arg) > 1:
            for key in connected: # connected[key
                 try:
                     text = ' '.join(arg[1:])
                     connected[key].send(json.dumps(['say',text]).encode())
                 except Exception as e:
                     MainServer.logs('ERROR [say]',e)
                     remove.append(connected[key])
                     continue
    elif type == 'erase' and enabled_commands[type]['enabled']:
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                break
        if admin:
            sendmess(['chat',"УВЕДОМЛЕНИЕ","Сервер сейчас сбросится"])
            time.sleep(3)
            for key in connected: # connected[key]
                try:
                    connected[key].close()
                except Exception as e:
                    MainServer.logs('ERROR [say]',e)
                    connected.pop(key)
                    continue
                  
            os.remove(name+'/data_file.json')
            os.remove(name+'/chat.json')
            os.rmdir(name)
              
            os.system('cls||clear')  
            os.execv(sys.executable, [sys.executable] + sys.argv)

            sys.exit() 
    elif type == 'help' and enabled_commands[type]['enabled']:
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        help = "/time - Показать время \n/random ЧИСЛО ЧИСЛО \n/cp, /changepassword, /changepass - Смена пароля \n/info НИК - Информация о пользователе \n/online - онлайн \n/music URL - музыка всем \n/we ник сообщение"    
        if admin:
            help = str(help)+"\n/say - отправить уведомлние всем \n/erase - сбросить сервер \n/setadmin, /sa - дать админку \n/removeadmin, /ra - снять админку \n/clear - очистка чата \n/connected, /c - подключенные"
            
        user_socket.send(json.dumps(['toast',help]).encode())
        
    if type == 'commands' and enabled_commands[type]['enabled']:
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        help = ["/time","/random","/cp","/changepassword","/changepass","/info","/online","/music","/we"]    
        if admin:
            for item in ["/say","/erase","/setadmin","/sa","/removeadmin","/ra","/clear","/connected","/c"]:
                help.append(item)
            
        user_socket.send(json.dumps(['commands',help]).encode())
        
    if type == 'we' and enabled_commands[type]['enabled']:
        if len(arg) == 1:
            user_socket.send(json.dumps(['toast',"Примеры использование команды \n/we gr4shin Привет мой друк!"]).encode())
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        if len(arg) > 1:
            try:
                users = user(['get_info'])
                for key in users:
                    if (users[key])['id'] == id:
                        sender_nick = (users[key])['nick']
                        break
                for key in connected:
                    for user_key in users:
                        if (users[user_key])['id'] == key:
                            if developer == (users[user_key])['nick'] and sender_nick != developer and (users[cmd[1]])['nick'] != developer:
                                connected[(users[user_key])['id']].send((json.dumps(['toast',"["+str(sender_nick)+"] -> ["+str((users[arg[1]])['nick'])+"] "+str((' '.join(arg[2:])))]).encode()))
                            break    
                connected[int((users[arg[1]])['id'])].send((json.dumps(['toast',"["+str(sender_nick)+"] -> ["+str((users[arg[1]])['nick'])+"] "+str((' '.join(arg[2:])))]).encode()))
            except Exception as e:
                user_socket.send((json.dumps(['toast','Ошибка отправки '+str(e)]).encode()))
                
    if type == 'setadmin' and enabled_commands[type]['enabled']:
        if len(arg) == 1:
            self.send(json.dumps(['toast',"Примеры использование команды \n/sa gr4shin"]).encode())
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        if admin and len(arg) > 1:
            sendmess(['chat','Server',str(admin_nick)+user(['setadmin',arg[1]])+str(arg[1]),True])
            
    if type == 'removeadmin' and enabled_commands[type]['enabled']:
        if len(arg) == 1:
            self.send(json.dumps(['toast',"Примеры использование команды \n/ra gr4shin"]).encode())
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        if admin and len(arg) > 1:
            sendmess(['chat','Server',str(admin_nick)+user(['removeadmin',arg[1]])+str(arg[1]),True])
            
    if type == 'clear' and enabled_commands[type]['enabled']:
        users = user(['get_info'])
        for key in users:
            if (users[key])['id'] == id:
                admin = (users[key])['admin']
                admin_nick = (users[key])['nick']
                break
        if admin and len(arg) == 1:
            chat_main.clear()
            sendmess(['chat','Server',"Чат был очищен администратором "+str(admin_nick),True])
        if admin and len(arg) == 2:
            if len(chat_main) < int(arg[1]):
                chat_main.clear()
                sendmess(['chat','Server',"Чат был очищен администратором "+str(admin_nick),True])
            else:
                index = 0
                while int(arg[1]) > index:
                    chat_main.pop(-1)
                    index = index + 1
                sendmess(['chat','Server', str(arg[1])+" сообщений было очищено администратором "+str(admin_nick),True])
                
    if type == 'changepassword' and enabled_commands[type]['enabled']:
        if len(arg) == 1:
            user_socket.send(json.dumps(['toast',"Примеры использование команды \n/cp P@$Sw04d\n/changepass qwerty12Q"]).encode())
        if len(arg) > 1 and len(arg) < 3:
            user_socket.send((json.dumps(['notify',['Смена пароля'],[user(['changepassword',id,arg[1]])],['SUCCESS']]).encode()))
            
    if type == 'connected' and enabled_commands[type]['enabled']:
        if len(arg) == 1 and user(['get_info'])[nick]['admin']:
            connectedsend = []
            for key in connected:
                connectedsend.append("("+str(key)+") "+str(connected[key].getpeername())) 
            user_socket.send((json.dumps(['toast',"Подключенные пользователи: \n"+str("\n".join(connectedsend))]).encode()))
        
    if type == 'information' and enabled_commands[type]['enabled']:
        if len(arg) == 1:
            self.send(json.dumps(['toast',"Примеры использование команды \n/info gr4shin\n/info ivan322"]).encode())
        if len(arg) > 1 and len(arg) < 3:
            info = 'Информация о пользователе:'
            getinfo = user(['get_info'])
            for key in getinfo:
                if (getinfo[key])['nick'] == arg[1]:
                    info = info + "\n" + 'ID: ' + str(getinfo[key]['id']) + "\n" + 'Никнейм: ' + str(getinfo[key]['nick']) + "\n" + 'Администратор: ' + str(getinfo[key]['admin']) + "\n" + 'Дата регистрации: ' + str(getinfo[key]['date'])
                    break
            user_socket.send(json.dumps(['toast',info]).encode())
    
    if type == 'online' and enabled_commands[type]['enabled']:
        connectedsend = []
        users = user(['get_info'])
        for key in connected:
            for user_key in users:
                if (users[user_key])['id'] == key:
                    user_nick = (users[user_key])['nick']
                    break
            connectedsend.append(user_nick)
        user_socket.send((json.dumps(['toast',"Онлайн: \n"+str("\n".join(connectedsend))]).encode()))

      #elif cmd[0] == '/aliexpress':
       #   promokod = {0:"admin",1:"прекрасное нихуя",2:"прекрасное нихуя",3:"прекрасное нихуя",4:"прекрасное нихуя",5:"прекрасное нихуя"}
       #   import random
       #   kek = random.randint(0,5)
          
       #   sendmess([recievedData[0],'Server',user(['promokod',promokod.get(kek),id])])  
    if type == 'time' and enabled_commands[type]['enabled']:
        import datetime
        now = datetime.datetime.now()
        user_socket.send(json.dumps(['toast',str(now.strftime("%d.%m.%Y %H:%M"))]).encode())
        
    if type == 'random' and enabled_commands[type]['enabled']:
        if len(arg) == 1:
            user_socket.send(json.dumps(['toast',"Примеры использование команды \n/random 0 10\n/random 50 100"]).encode())
        if len(arg) == 3:
            import random
            try:
                int(arg[2])
                int(arg[1])
                user_socket.send(json.dumps(['toast','Случайное число: '+str(random.randint(int(arg[1]),int(arg[2])))]).encode())
            except Exception as e:
                user_socket.send(json.dumps(['toast',"Примеры использование команды \n/random 0 10\n/random 50 100 "]).encode())
        else:
            user_socket.send(json.dumps(['toast',"Примеры использование команды \n/random 0 10\n/random 50 100"]).encode())
            
    if type == 'music' and enabled_commands[type]['enabled']:
        if len(arg) == 1:
            user_socket.send(json.dumps(['toast',"Примеры использование команды \n/music URL.mp3"]).encode())
        if len(arg) == 2:
            sendmess(['chat','Server','Кто-то включил музыку'])
            for key in connected: # connected[key]
               try:
                   connected[key].send(json.dumps(['music',arg[1]]).encode())
               except Exception as e:
                   MainServer.logs('ERROR [say]',e)
                   connected.pop(key)
                   continue

                    
def user(arr,socket_user = False):
    if os.path.exists(name+'/data_file.json') == False:
        data_users = open(name+"/data_file.json", "w+")
        data_users.write("{}")
        data_users.close()
    if arr[0] == 'login':
        with open(name+"/data_file.json", "r") as read_file:
            data = json.load(read_file)
        if len(data.keys()) >= 0:
            nick = arr[2][0]
            nick = nick.replace(" ","")
            nick = re.sub(r'[^A-zА-я0-9]','',nick)
            if data.get(nick):
                if data.get(nick).get('password') == arr[2][1]:
                    MainServer.logs('LOGIN','пользователь авторизован')
                    connected.pop(arr[1])
                    connected[data.get(nick).get('id')] = conn
                    conn.send((json.dumps(['setinfo',['id', data.get(nick).get('id')],['nick', data.get(nick).get('nick')],['auth', True],['room',name]]).encode()))
                    user(['add',arr[1],arr[2][0]])
                else:
                    MainServer.logs('LOGIN','пользователь ввёл неправильный пароль')
                    conn.send((json.dumps(['notify',['Авторизация'],['Неверный пароль'],['ERROR']]).encode()))
                

            else:
                
                MainServer.logs('LOGIN','создание пользователя')
                
                nick = arr[2][0]
                nick = nick.replace(" ","")
                nick = re.sub(r'[^A-zА-я0-9]','',nick)
                
                if len(nick) > 20:
                    i = 0
                    nick = ''
                    for sim in nick:
                        if i != 20:
                            nick = nick+sim
                            i = i + 1
                            
                if nick.lower() == 'server':
                    nick = nick+str(random.randint(0,999))
                    
                if nick.lower() == '':
                    nick = "ID"+str(random.randint(0,999))
                    
                if nick == developer:
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
                    'date':(getinfo[key])['date']
                    }
                with open(name+"data_file.json", "w") as write_file:
                    json.dump(data, write_file)
                return " пароль изменён!"
        
      
    if arr[0] == 'setadmin':
        users_get = user(['get_info'])
        if users_get.get(arr[1]):
            with open(name+"/data_file.json", "r") as read_file:
                data = json.load(read_file)
            if data[arr[1]]['admin'] == True:
                return " пытался добавить уже администратора "
            elif developer == data[arr[1]]['nick']:
                return " блять я девелопа, какого хуя ты делаешь? "
            else:
                data[arr[1]] ={
                    'id':users_get[arr[1]]['id'],
                    'nick':users_get[arr[1]]['nick'],
                    'password':users_get[arr[1]]['password'],
                    'admin':True,
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
          elif developer == data[arr[1]]['nick']:
              return " пытался убрать права администратора у САМОГО ЛУЧШЕГО "
          else:
              data[arr[1]] ={
                  'id':users_get[arr[1]]['id'],
                  'nick':users_get[arr[1]]['nick'],
                  'password':users_get[arr[1]]['password'],
                  'admin':False,
                  'date':users_get[arr[1]]['date']
                  }
              with open(name+"/data_file.json", "w") as write_file:
                  json.dump(data, write_file)
              return " убрал с поста администратора "
      else:
          return ' пытался отобрать права администратора '  
          
      
    if arr[0] == 'remove':
        if users.get(arr[1]):
            users.pop(arr[1])
      
    if arr[0] == 'list':
      online = 'Онлайн: '
      for key in users:
        online = str(online)+' ID'+str(key) 
      return online 


        
def sendmess(arr, clear = False):
    
  userid = arr[1]
  nick = ''
  admin = ''
  mess = arr[2]
  remove = []
  old_mess = []
  
  import datetime    
  now = datetime.datetime.now()   
  time = now.strftime("%H:%M")
  
  if userid == 'Server':
      nick = 'Server'
  
  users = user(['get_info'])

  for key in users:
      if (users[key])['id'] == userid:
          nick = (users[key])['nick']
          if (users[key])['admin']:
              admin = " (a)"
          break
  for key in connected: # connected[key]
      try:
          connected[key].send((json.dumps(['pong',userid]).encode()))
      except 1 as e:
          MainServer.logs('ERROR [say]',e)
          connected.pop(key)
          continue

  if len(chat_main) > 200:
      chat_main.clear()
      sendmess(['chat','Server',"Чат был сброшен из-за большого количества сообщений",True]) 
  if len(mess) > 200:
      old_mess = mess
      mess = mess[:200]
  chat_main.append([nick,mess,str(time)+str(admin)])
  if len(old_mess) > 200:
      sendmess([arr[0],arr[1],old_mess[200::]])
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
  for key in connected: # connected[key]
      try:
          connected[key].send((json.dumps(['chat',chat_main]).encode()))
      except Exception as e:
          MainServer.logs('ERROR [say]',e)
          connected.pop(key)
          continue


    ####################################################################
    #
    #   ПАРАМЕТРЫ СЕРВЕРА
    #
    ####################################################################
    
class MainServer(asyncore.dispatcher):
  def __init__(self,serverAddr ,port):
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
    self.socket.bind((serverAddr, port))
    self.listen(10)
    MainServer.logs('INFO',''+str(serverAddr) + ":" + str(port)+' сервер '+'запущен')
    #sendmess(['chat','Server','ping'])  
    
  def handle_accept(self):
    global conn
    playerid = random.randint(1, 100)

    conn, addr = self.accept()
    connected[playerid] = conn
    #outgoing.append(conn)

    #MainServer.logs('INFO','[id'+str(playerid)+'] пользователь подключился')
    try:
        conn.send((json.dumps(['setinfo',['id', playerid],['nick', playerid],['auth', False]]).encode()))
    except Exception as e:
        MainServer.logs('ERROR','Потеряна связь с пользователем... '+str(e)+' ('+str(recievedData)+')')
        conn.close()
    SecondaryServer(conn)
    
  def logs(type,text):
    print('# [Server]'+'['+str(type)+'] '+str(text))
        
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
        user(recievedData,self)
      
    elif recievedData[0] == 'disconnect':
      self.close()
      connected.pop(recievedData[1])
      user(['remove',recievedData[1]])
      MainServer.logs('INFO','[id'+str(recievedData[1])+'] пользователь отключился')
      sendmess(['chat','Server',"пользователь покинул нас [ID"+str(recievedData[1])+"]"])
      
    elif recievedData[0] == 'ping':
      self.send(json.dumps(['ping',recievedData[2]]).encode())
      
    elif recievedData[0] == 'chat':
      id = recievedData[1]
      users = user(['get_info'])
      for key in users:
          if (users[key])['id'] == id:
              nick = (users[key])['nick']
              break
      cmd = recievedData[2].split()

      # УВЕДОМЛЕНИЕ
      if cmd[0] == '/say':
          command(self,id,nick,'say',cmd)
 
      # РЕСТАРТ СЕРВА
      elif cmd[0] == '/erase':
          command(self,id,nick,'erase',cmd)
             
      # ПОМОЩЬ              
      elif cmd[0] == '/help':
          command(self,id,nick,'help',cmd)

      # Доступные команды          
      elif cmd[0] == '/commands':
          command(self,id,nick,'commands',cmd)

      # ЛИЧНЫЕ СООБЩЕНИЯ  
      elif cmd[0] == '/we':
          command(self,id,nick,'we',cmd)
            
      # АДМИНКА  
      elif cmd[0] == '/setadmin' or cmd[0] == '/sa':
          command(self,id,nick,'setadmin',cmd)
      elif cmd[0] == '/removeadmin' or cmd[0] == '/ra': 
          command(self,id,nick,'removeadmin',cmd)   

      # ОЧИСТКА ЧАТА
      elif cmd[0] == '/clear':
          command(self,id,nick,'clear',cmd)   

      # СМЕНА ПАРОЛЯ
      elif cmd[0] == '/cp' or cmd[0] == '/changepass' or cmd[0] == '/changepassword':
          command(self,id,nick,'changepassword',cmd)
          
      # Подключенные
      elif cmd[0] == '/connected' or cmd[0] == '/c':
          command(self,id,nick,'connected',cmd)
                  
      # Кик
      elif cmd[0] == '/kick':
          command(self,id,nick,'kick',cmd)
          #if commands[cmd[0]]['enabled'] == False:
          #    self.send((json.dumps(['toast','Временно отключена']).encode()))
          #if len(cmd) == 2 and user(['get_info'])[nick]['admin'] and commands[cmd[0]]['enabled']:
          #    if (user(['get_info'])).get(cmd[1]) and connected[user(['get_info'])[nick]['id']]:
          ##        kick_id = (user(['get_info']))[cmd[1]]['id']
          #        connected[kick_id].close()
          #        connected.pop(kick_id)
              

      # ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ     
      elif cmd[0] == '/info' or cmd[0] == '/information' or cmd[0] == '/getinfo':
          command(self,id,nick,'information',cmd)

      # ОНЛАЙН   
      elif cmd[0] == '/online':
          command(self,id,nick,'online',cmd)

      # ВРЕМЯ     
      elif cmd[0] == '/time':
          sendmess(recievedData)
          command(self,id,nick,'time',cmd)         
        
      # РАНДОМ      
      elif cmd[0] == '/random':
          command(self,id,nick,'random',cmd)
              
      # Музыка      
      elif cmd[0] == '/music':
          command(self,id,nick,'music',cmd)
        
      else:
        if str(cmd[0])[0] == '/':
            command(self,id,nick,'uknw',cmd)   
        else:
            sendmess(recievedData)
      
    else:
      MainServer.logs('WARNING','пришла другая информация: '+str(recievedData))



    #
    #    Запуск сервера
    #

try:
  global serverAddr, ms, name
  connected = {}
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
  MainServer.logs('ERROR in Server',e)
finally:
  MainServer.logs('INFO','остановлен.')
  input('Press ENTER to close...')
