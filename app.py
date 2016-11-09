####################################################################
####################################################################
### http://remaire.chatango.com 			 					 ###
### http://tango-hyoo.chatango.com 								 ###
### If you would like help setting up your own bot, feel free to ###
### send me a personal message on chatango.                      ###
### --Many thanks for TryHardHusky and Poeticartist1--           ###
####################################################################  
  

# YOU WILL NEED THE CH.PY TO RUN THIS BOT!
# YOU CAN GET IT FROM HERE http://pastebin.com/MBwdSZsW
  
import ch
import random
import sys
import os
import re
import time
import json
import urllib
import traceback
import __future__

################################
lockdown = False
activated = True
################################

################################
##File Stuff##

blacklist = dict()
try:
  f = open("blacklist.txt", "r")
  blacklist = eval(f.read())
  f.close()
except:pass

mod = []
file = open("mod.txt", 'r')
for name in file.readlines():
  if len(name.strip()) > 0 :
    mod.append(name.strip())
print("NOTICE: Mod list loaded.")
file.close()

registered = []
file = open("registered.txt", 'r')
for name in file.readlines():
  if len(name.strip()) > 0 :
    registered.append(name.strip())
print("NOTICE: Registered Users loaded.")
file.close()

owner = []
file = open("owner.txt", 'r')
for name in file.readlines():
  if len(name.strip()) > 0 :
    owner.append(name.strip())
print("NOTICE: Your Ownership loaded.")
file.close()

rooms = []
file = open("rooms.txt", 'r')
for name in file.readlines():
  if len(name.strip()) > 0 :
    rooms.append(name.strip())
print("NOTICE: Room list loaded.")
file.close()

locks = []
file = open("locks.txt", 'r')
for name in file.readlines():
  if len(name.strip()) > 0 :
    locks.append(name.strip())
print("NOTICE: Locked Rooms loaded.")
file.close()

##End##
################################

#############################################################
##========================Variables========================##

botname = "MayuBot" #Put your bot name here

botpassword = "92725430" #Put your bot password here

cek_mods = dict() #Don't mess with this variable. This one is related with *mods command.

error = ("Expectation failed.")    #Error message

command_list = ['help','wl/register','uwl/unregister','bl/blacklist','chain','ubl/unblacklist','unchain','rank','setrank','pm','broadcast','say','reverse/rsay','find','multichat','ban','unban','join','leave','lock','unlock','rooms','save','mods','activate','restrict','lockdown','wake']

prefix = "~" ##You set the prefix here

##===========================End===========================##
#############################################################
  
#setting colors
  
class TestBot(ch.RoomManager):
  def onInit(self):
    self.setNameColor("FF9966")
    self.setFontColor("33CCFF")
    self.setFontFace("1")
    self.setFontSize(12)
    self.enableBg()  
    self.enableRecording()
    
  def saveAll(self):
    room = self._Room
    f = open("owner.txt", "w")
    f.write("\n".join(owner))
    f.close()
    f = open("mod.txt", "w")
    f.write("\n".join(mod))
    f.close()
    f = open("registered.txt", "w")
    f.write("\n".join(registered))
    f.close()
    f = open("blacklist.txt", "w")
    f.write("\n".join(blacklist))
    f.close()
    f = open("locks.txt", "w")
    f.write("\n".join(locks))
    f.close()
    f = open("rooms.txt", "w")
    f.write("\n".join(self.roomnames))
    f.close()



  def getAccess(self, room, user):
    vroom = room
    if user.name in owner and not user.name in blacklist: return 5
    elif user.name in mod and not user.name in blacklist: return 4
    elif user.name in registered and user.name in vroom.ownername and not user.name in blacklist: return 3
    elif user.name in registered and user.name in vroom.modnames and not user.name in blacklist: return 2
    elif user.name in registered and not user.name in vroom.ownername and not user.name in room.modnames and not user.name in blacklist: return 1
    elif user.name in blacklist: return -1
    else: return 0

#############################################  
##connecting and disconnecting crap##
  
  def onConnect(self, room):
    print("[+] Mad Hatter Connected to "+room.name)
    for i in cek_mods: #Di onJoin
      if len(cek_mods[i]) > 1:
        rmm, rmd = json.loads(cek_mods[i])
        self.getRoom(rmm).message("<br/>||<font color='#87ceeb'><b>OWNER</b></font>: <b>"+ (self.getRoom(rmd).ownername) +"</b> <br/>||<b>Mods</b>: "+", ".join(self.getRoom(rmd).modnames), True)
        self.leaveRoom(rmd)
        cek_mods.pop(i)
      return
    
  def onReconnect(self, room):
    print("[+] Mad Hatter Reconnected to "+room.name)
    
  def onDisconnect(self, room):
    print("[+] Mad Hatter Disconnected from "+room.name)
    
  def onBan(self, room, user, target):
    print(user.name+" got banned in "+room.name)
    
#  def onJoin(self, room, user):
#    print("[+] "+user.name+" joined "+room.name)
#    if not activated: return
#    if user.name in owner:
#      room.message("*Bows down to "+ user.name.title() +"*")
#      return
#    if self.getAccess(room, user) > 1 and not user.name in owner:
#      room.message("Good Day "+user.name+".")
#      return
#    if int(room.usercount) > 20:
#      return
#    if self.getAccess(room, user) == 1 or self.getAccess(room, user) == 0:
#      room.message(user.name+" has joined the room.")
#      return

  def onConnectFail(self, room):
    print("[ERR] Room Not Found")
    for i in cek_mods: #Di onJoin
      if len(cek_mods[i]) > 1:
        rmm, rmd = json.loads(cek_mods[i])
        self.getRoom(rmm).message("Such room doesn't exist")
        cek_mods.pop(i)
      return

  

##End##
#############################################

#############################################
##setting up commands##
  
  def onMessage(self, room, user, message):
   try:
    if user == self.user:
        return
    global activated
    global lockdown
    global prefix
    global owner
    global mod
    global registered
    try:
      if room.getLevel(self.user) > 0:
        print("[%s]\033[94m[MSG]\033[0m\033[31m[Rank %s]\033[0m\033[41m[%s][%s] %s: %s" % (time.strftime("%d/%m/%y- %H:%M:%S", time.localtime(time.time())), self.getAccess(room, user), room.name, message.ip, user.name.title(), message.body))
      else:
        print("[%s]\033[94m[MSG]\033[0m\033[31m[Rank %s]\033[0m\033[41m[%s][User_IP: Null] %s: %s" % (time.strftime("%d/%m/%y- %H:%M:%S", time.localtime(time.time())), self.getAccess(room, user), room.name, user.name.title(), message.body))
    except:
      pass
    if user.name.startswith("#") or user.name.startswith("!"):return
    if self.user == user: return
    if user.name in blacklist: return
    if self.getAccess(room, user) > 0:
      if not activated and self.getAccess(room, user) < 4: return #return, if not activated and user rank is less than 4.
      ##Persona | You design a good personality for your bot in this part
      if "hey" in message.body:
          room.message("Yesh, " +message.body)
      if "hello" == message.body.lower(): #for example if someone said "hello" in the chatroom
          room.message("Hello "+user.name.title()) #the bot will answer with "Hello User1Name"
      if "hi" == message.body.lower():
          room.message("Hi "+user.name.title())
      if "please kill it" == message.body:
        self.stop()
        
    ##Commands | You design great commands for your bot in this part
    if message.body[0] == prefix: #prefix usage in this line (for this case I use "*" as prefix)
        data = message.body[1:].split(" ", 1) #This part splits message body into [0]prefix and [1:]data ([1:] <- this means the message body's second character and after) and data will be split into 2 (cmd(data[0]), args(data[1])) which is very usefull. (Many thanks to TryHardHusky)
        if len(data) == 2: #If there are more than 1 data (This is where we will get args)
          cmd, args = data[0], data[1] #the first data (data[0]) will be the cmd (specified command) and the next data will be args (it doesn't matter how many word next to the cmd, It'd eventually be args)
        else: #If there is only 1 data (No args)
          cmd, args = data[0], "" #the arg will simply be "" (Empty)
        cmd == cmd.lower()

        ##Activating and Inactivating Bot
        if cmd == "shutdown":
          if self.getAccess(room, user) == 5:
            self.saveAll()
            room.message("Bye *waves*")
            self.setTimeout(3, self.stop, )
        if cmd == "activate":
          if self.getAccess(room, user) < 4: return
          activated = True
          room.message("[Activated]")

        if cmd == "restrict":
          if self.getAccess(room, user) < 4: return
          activated = False
          room.message("[Restricted]")

        if not activated and self.getAccess(room, user) < 5: return #Ignore user with rank lower than 5 when not activated
        if lockdown and self.getAccess(room, user) < 4: return #Ignore user with rank lower than 4 when in lockdown
        
        if cmd == "help": #Help command (It will show the bot's version, user's rank status, user's room level, and Available commands)
          version = "Example Version" #You set the bot's version manually in this line
          rank = 0
          moded = "no"
          rank = self.getAccess(room, user)
          if room.getLevel(user) > 0:
            moded = "yes"
          if rank > 1:
            room.message("<font color='#FF8C00'><b>"+self.user.name+"</b></font>(<font color='#B8860B'><b>"+version+"</b></font>)<br/>"+user.name.title()+" - [<font color='#FF0000'><b>Rank "+str(rank)+"</b></font>] - Moded [<b>"+moded+"</b>]<br/>cmds: use [%s] as prefix [%s]"% (prefix, ", ".join(command_list)), True)
          if rank == 0:
            moded = "Null"
            if room.getLevel(user) > 0:
              moded = "Moded"
            room.message("<font color='#FF8C00'><b>"+self.user.name+"</b></font>(<font color='#B8860B'><b>"+version+"</b></font>)<br/>"+user.name.title()+" - [<font color='#FF0000'><b>Unregistered</b></font>] - [<b>"+moded+"</b>]<br/>cmds: use [%s] as prefix [%s]"% (prefix, ", ".join(['help','wl','uwl'])), True)
          
        if self.getAccess(room, user) == 0 and cmd == "wl" or cmd == "register" or cmd == "reg": #First cmd for unwhitelisted user.
          if args == "":
            registered.append(user.name) #To put user.name in whitelist
            room.message("Done, You're now a Registered as player.")
          else:
            if args in registered:
              room.message(args.title()+" is already registered.")
              return
            if args in room.usernames:
              registered.append(args)
              room.message("Done, "+args.title()+" is now Registered.")
            else:
              room.message("I don't see "+args.title()+" here.")
          
        if self.getAccess(room, user) > 0 and cmd == "uwl" or cmd == "unregister" or cmd == "unreg":
          if user.name in registered:
            registered.remove(user.name)
          if user.name in mod:
            mod.remove(user.name)
          room.message("Success, You unregistered yourself.")
        
        if self.getAccess(room, user) < 1: return # This is to filter the command section | return, If user is not whitelisted.
        
##################################################################################################################
##=======================================  Commands for rank 2+  ===============================================##
        
        if cmd == "setrank" and self.getAccess(room, user) == 5:
          help_output = "Usage : ~setrank [usertarget] [number]<br/>Example : ~setrank gayman 1]"
          if args == "":
            room.message(help_output, True)
          if args != "":
#           try:
            args = args.lower()
            target, rank = args.split(" ", 1)
            target = str(target)
            rank = int(rank)
            available_rank = [-1,0,1,4,5]
            if not rank in available_rank:
              room.message("Type a propper rank number.")
              return
            if rank == 1:
              if target in registered:
                room.message(target.title()+" is already a Player.")
                return
              if target in blacklist:
                blacklist.pop(target)
              if target in owner:
                owner.remove(target)
              if target in mod:
                mod.remove(target)
              registered.append(target)
              room.message(target.title()+"'s rank is set to: "+str(rank)+" [Player]")
            if rank == 4:
              if target in mod:
                room.message(target.title()+" is already a Moderator.")
                return
              if target in blacklist:
                blacklist.pop(target)
              if target in owner:
                owner.remove(target)
              if target in registered:
                registered.remove(target)
              mod.append(target)
              room.message(target.title()+"'s rank is set to: "+str(rank)+" [Moderator]")
            if rank == 5:
              if not user.name == "tsuid": return #put your name there (if user.name == "yourname" and user.name == "anothername":) To prevent other Owners(in this case is Co-Owners) to set user's rank to Co-Owner.
              if target in owner:
                room.message(target.title()+" is already a Co-Owner.")
                return
              if target in blacklist:
                blacklist.pop(target)
              if target in registered:
                registered.remove(target)
              if target in mod:
                mod.remove(target)
              owner.append(target)
              room.message(target.title()+"'s rank is set to: "+str(rank)+" [Owner]")
            if rank == 0:
              if not user.name == "tsuid": return #put your name there (if user.name == "yourname" and user.name == "anothername":) To prevent your account(s) from being unwhitelisted by your Co-Owner.
              if target in owner:
                owner.remove(target)
              if target in blacklist:
                blacklist.pop(target)
              if target in registered:
                registered.remove(target)
              if target in mod:
                mod.remove(target)
              room.message(target.title()+"'s rank is set to: "+str(rank))
            if rank == -1:
              if target == "tsuid": return #put your name there (if target == "yourname" and target == "anothername":) To prevent your account(s) from being blacklisted.
              if target in blacklist:
                room.message(target.title()+" is already blacklisted.<br/>Reason: %s"% blacklist[target])
                return
              blacklist.update({target:"Annoying reason."})
              room.message(target.title()+"'s rank is set to: "+str(rank)+" [Fugitive]")
#           except:
#             room.message(help_output, True)

        if cmd == "lockdown": #This is to lock commands for user with rank lower than 4
          if self.getAccess(room, user) < 4: return
          if lockdown: return
          room.message("Command is Locked.")
          lockdown = True

        if cmd == "wake": #This is to unlock the command lockdown
          if self.getAccess(room, user) < 4: return
          if not lockdown: return
          room.message("Command is unlocked.")
          lockdown = False
          
        if cmd == "bl" or cmd == "blacklist":
          if args == "":
            if len(blacklist) < 0:
              room.message("Blacklist: None")
              return
            black_users = ["#redperson"]
            for i in blacklist:
              black_users.append(i)
            room.message("Blacklist: %s."% (", ".join(black_users)))
          if len(args.split(" ")) > 0:
            if len(args.split(" ", 1)) == 2:
              target, reason = args.split(" ", 1)
              target = target.lower()
            if len(args.split(" ", 1)) == 1:
              target = args.lower()
          if self.getAccess(room, ch.User(target)) == 5: return #to prevent owner and co-owners from blacklisted
          if self.getAccess(room, ch.User(target)) >=4 and self.getAccess(room, user) == 4: #To prevent bot moderators from banning another moderator or even owners
            room.message("You don't have the permission to do that")
            return
          if target in blacklist:
            room.message(target.title()+"'s status: Blacklisted<br/>Reason: <i>%s</i>"% (blacklist[args]), True)
          if target not in blacklist and len(args) > 1:
            if self.getAccess(room, user) < 4: return
            if len(reason) < 10:
              room.message("Reason is too short. put minimal 10 characters.")
              return
            blacklist.update({str(target):str(reason)})
            room.message(target.title()+" is blacklisted.<br/>"+user.name.title()+"'s Reason: "+reason, True)
            
        if cmd == "unblacklist" or cmd == "ubl":
          if self.getAccess(room, user) < 4: return
          if args == "": return
          args = args.lower()
          if args not in blacklist:
            room.message(args.title()+" is not blacklisted.")
            return
          if args in mod and self.getAccess(room, user) < 5:
            room.message("You don't have permission to unblacklist that user.")
            return
          blacklist.pop(args)
          room.message(args.title()+" is unblacklisted.")
            
        if cmd == "unchain":
          if self.getAccess(room, user) < 4: return
          if args == "": return
          args = args.lower()
          if args not in blacklist:
            room.message(args.title()+" is not chained.")
            return
          if args in mod and self.getAccess(room, user) < 5:
            room.message("You don't have permission to unchain that user.")
            return
          blacklist.pop(args)
          room.message(args.title()+" is unchained.")
            
        if cmd == "chain":
          if args == "":
            if len(blacklist) < 0:
              room.message("Chained: None")
              return
            black_users = ["#esperguy"]
            for i in blacklist:
              black_users.append(i)
            room.message("Chained: %s."% (", ".join(black_users)))
          if len(args.split(" ")) > 0:
            if len(args.split(" ", 1)) == 2:
              target, reason = args.split(" ", 1)
              target = target.lower()
            if len(args.split(" ", 1)) == 1:
              target = args.lower()
          if target in blacklist and len(args) == 1:
            room.message(target.title()+"'s status: Chained<br/>Reason: <i>%s</i>"% (blacklist[args]), True)
          if target not in blacklist and len(args) > 1:
            if self.getAccess(room, user) < 4: return
            if len(reason) < 10:
              room.message("Reason is too short. put minimal 10 characters.")
              return
            blacklist.update({target:reason})
            room.message(target.title()+" is Chained.<br/>"+user.name.title()+"'s Reason: <i>%s</i>"% (reason), True)


        if cmd == "lock":
          if self.getAccess(room, user) < 2:
            room.message("No.")
            return
          if args in locks:
            room.message("It's locked already.")
            return
          if args in self.roomnames:
            if self.getAccess(room, user) > 3:
              locks.append(args)
              room.message("locked <b>%s</b>" % args, True)
            else: room.message("You don't have permission to do that.")
          if args == "":
            if room.name in locks:
              room.message("It's locked already.")
              return
            locks.append(room.name)
            room.message("locked <b>%s</b>" % room.name, True)
          if args not in self.roomnames:
            if args == "": return
            room.message("I haven't joined %s."% args)
            return

        if cmd == "unlock":
          if self.getAccess(room, user) < 2: return
          if args in self.roomnames:
            if args in locks:
              if self.getAccess(room, user) > 3:
                locks.remove(args)
                room.message("unlocked <b>%s</b>" % args, True)
              else: room.message("You don't have permission to do that.")
            else:
              room.message("It's not even locked.")
              return
          if args == "":
            if room.name in locks:
              locks.remove(room.name)
              room.message("unlocked <b>%s</b>" % room.name, True)
            else:
              room.message("It's not even locked.")
              return
          if args not in self.roomnames:
            if args == "": return
            room.message("I haven't joined %s"% args)
            return

        if cmd == "ban":
          if room.getLevel(user) > 0:
            if room.getLevel(self.user) > 0:
              room.banUser(ch.User(args))
              room.message(args.title()+" is banned")
            else:
              room.message("I'm not even a mod here")
          else:
            room.message("You don't have permission")
            
        if cmd == "unban":
          if args == "": return
          args = args.lower()
          if room.getLevel(user) > 0:
            if room.getLevel(self.user) > 0:
              if ch.User(args) not in room.getBanlist():
                room.message(args.title()+" is not even banned.")
                return
              room.unban(ch.User(args))
              room.message(args.title()+" is unbanned")
            else:
              room.message("I'm not even a mod here")
          else:
            room.message("You don't have permission")

        if cmd == "broadcast":
            if self.getAccess(room, user) > 3:
                for room in self.rooms:
                    room.message("Broadcast from - <b>"+user.name + "</b>: "+args, True)
            else:
                room.message("You don't have permission.")
      	

        if cmd == "join": #This command is free for all registered user (rank 1+) to use
          if args == "": return
          if args in self.roomnames:
            room.message("I'm there already.")
          else:
            self.joinRoom(args)
            room.message("*Joins "+args.title()+"*")
        
        if cmd == "leave":
          if self.getAccess(room, user) > 1:
            if args == "":
              room.message("Okay, I'm leaving this room.")
              self.setTimeout(2, self.leaveRoom, room.name)
            else:
              if self.getAccess(room, user) < 4: return
              self.leaveRoom(args)
              room.message("I'm leaving "+args.title())
          else:
            room.message("You don't have permission.")
            
        if cmd == "save" and self.getAccess(room, user) >= 4:
          self.saveAll()
          room.message("Database has been saved.")
          
        if (cmd == "eval") and self.getAccess(room, user) == 5: #DO NOT MESS WITH THIS COMMAND IF YOU DON'T KNOW WHAT YOU'RE DOING (This is a vital command)
          ret = eval(args)
          if ret == None:
            room.message("Done.")
            return
          room.message(str(ret))


##=======================================  Commands for rank 2+  ===============================================##
##=============================================== End ==========================================================##
##################################################################################################################


        if cmd == ("say"):
            if args:
              room.message(args)
            else:
              room.message("What to say ?")
              
        if cmd == "reverse" or cmd == "rsay": #Reversed arguments
          if args:
            room.message(args[::-1])
          else:
            room.message("Fook off"[::-1])


        elif cmd == "cmds":
          if self.getAccess(room, user) < 1: return
          room.message("some commands you can use, with [%s] as prefix [%s]"% (prefix, ", ".join(command_list)))


        if cmd == "pm" and len(args) > 1:
            name, msg = args.split(" ", 1)
            self.pm.message(ch.User(name.lower()), msg+" - from "+user.name)
            room.message('Sent to <font size="15"><font color="#FF9966"><b>%s</b></font></font>' % name, True)

       ##Checking levels and ranks stuff   
        elif cmd == "level":
          if args == "":
            level = room.getLevel(user)
            if level == 1:
              title = "Moderator"
            if level == 2:
              title = "OWNER"
            if level == 0:
              title = "Slave"
            room.message("Your room level is: %s [%s]" %(level,title))
          else:
            level = room.getLevel(ch.User(args))
            if level == 1:
              title = "Moderator"
            if level == 2:
              title = "OWNER"
            if level == 0:
              title = "Slave"
            room.message("%s's room level is: %s [%s]" %(args.title(), level, title))

  
        elif cmd == "rank":
          if args == "":
            rank = self.getAccess(room, user)
            if rank == 1:
              title = "Player"
              room.message("Your rank is: <font color='#7cfc00'><b>%s</b></font> [<font color='#7cfc00'>%s</font>]" % (rank, title), True)
            if rank == 2:
              title = "Room Mod"
              room.message("Your rank is: <font color='#7cfc00'><b>%s</b></font> [<font color='#7cfc00'>%s</font>]" % (rank, title), True)
            if rank == 3:
              title = "Room Admin"
              room.message("Your rank is: <font color='#7cfc00'><b>%s</b></font> [<font color='#7cfc00'>%s</font>]" % (rank, title), True)
            if rank == 4:
              title = "Moderator"
              room.message("Your rank is: <font color='#0000ff'><b>%s</b></font> [<font color='#fffaf0'><b>%s</b></font>]" % (rank, title), True)
            if rank == 5:
              title = "Owner"
              room.message("Your rank is: <font color='#c0c0c0'><b>%s</b></font> [<font color='#87ceeb'><b>%s</b></font>]" % (rank, title), True)
          else:
              rank = self.getAccess(room, ch.User(args))
              if rank == 0:
                room.message(args+" is unregistered.")
              if rank == 1:
                title = "Player"
                room.message(args+"'s rank is: <font color='#7cfc00'><b>%s</b></font> [<font color='#7cfc00'>%s</font>]" % (rank, title), True)
              if rank == 2:
                title = "Room Mod"
                room.message(args+"'s rank is: <font color='#7cfc00'><b>%s</b></font> [<font color='#7cfc00'>%s</font>]" % (rank, title), True)
              if rank == 3:
                title = "Room Admin"
                room.message(args+"'s rank is: <font color='#7cfc00'><b>%s</b></font> [<font color='#7cfc00'>%s</font>]" % (rank, title), True)
              if rank == 4:
                title = "Moderator"
                room.message(args+"'s rank is: <font color='#0000ff'><b>%s</b></font> [<font color='#fffaf0'><b>%s</b></font>]" % (rank, title), True)
              if rank == 5:
                title = "Owner"
                room.message(args + "'s rank is: <font color='#c0c0c0'><b>%s</b></font> [<font color='#87ceeb'><b>%s</b></font>]" % (rank, title), True)
                
        
        elif cmd == "mods":
          args = args.lower()
          if args == "":
            room.message("<br/>||<font color='#87ceeb'><b>OWNER</b></font>: <u>"+ (room.ownername) +"</u> <br/>||<b>Mods</b>: "+", ".join(room.modnames), True)
            return
          if args in self.roomnames:
              modask = self.getRoom(args).modnames
              owner = self.getRoom(args).ownername
              room.message("<br/>||<font color='#87ceeb'><b>OWNER</b></font>: <u>"+ (owner) +"</u> <br/>||<b>Mods</b>: "+", ".join(modask), True)
          else:
             self.joinRoom(args)
             cek_mods[user.name] = json.dumps([room.name,args])
  

        ##Some certain commands for rank 1+

        
        if cmd == ("find") and len(args) > 0:
          name = args.split()[0].lower()
          if not ch.User(name).roomnames:
            room.message("dont see them. ^^")
          else:
            room.message("%s is curently in <b>%s</b> >_>" % (args, ", ".join(ch.User(name).roomnames)), True)
        if cmd == "multichat":
          room.message("http://ch.pew.im/chat/?"+args)
        if cmd == "rooms":
          room.message("||i'm in : <b>%s</b> ||" % (", ".join(self.roomnames)), True)



   except Exception as e:
         try:
          et, ev, tb = sys.exc_info()
          lineno = tb.tb_lineno
          fn = tb.tb_frame.f_code.co_filename
          room.message("[Error] %s Line %i - %s"% (fn, lineno, str(e)))
          return
         except:
          room.message("Undescribeable error detected !!")
          return

  
  def onUserCountChange(self, room):
    print(room.name+" - Current Users: " + str(room.usercount))

#  def onLeave(self, room, user):
#    print("[+] "+user.name+" left "+room.name)
#    if room.usercount >= 20:
#      return
#    room.message(user.name+" has left the room.")

  def onFloodWarning(self, room):
    room.reconnect()
    room.setSilent(True)
    self.setTimeout(15, room.setSilent, False)
    self.setTimeout(16, room.message, "I'm back.")
    print("[+] Reconnecting...")

  def onMessageDelete(self, room, user, msg):
    print("MESSAGE DELETED: " + user.name + ": " + msg.body)
  
  def onPMMessage(self, pm, user, body):
    print("PM - "+user.name+": "+body)
    pm.message(user, "I'm a Bot Created by 0rx. Please PM my owner instead!")

def hexc(e):
  et, ev, tb = sys.exc_info()
  if not tb: print(str(e))
  while tb:
    lineno = tb.tb_lineno
    fn = tb.tb_frame.f_code.co_filename
    tb = tb.tb_next
  print("(%s:%i) %s" % (fn, lineno, str(e)))
  
if __name__ == "__main__":
   try:
     os.system("clear")
     TestBot.easy_start(rooms, botname, botpassword)
   except KeyboardInterrupt:
     print("Console initiated a kill.")
   except Exception as e:
     hexc(e)
