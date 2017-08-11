# -*- coding: UTF-8 -*-
from cleverwrap import CleverWrap
from fbchat import log, Client
import sms_sender as ss
import sys
# Subclass fbchat.Client and override required methods
cw="NULL"
client="NULL"
flag=0
msg_cnt=0
terminated=set([])
all_users=set([])
disabled=False
prev=""
while True:
    flag=0
    client=""
    cw="NULL"
    msg_cnt=0
    try:
        class EchoBot(Client):
            def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
                while(True):
                    try:
                        self.markAsDelivered(author_id, thread_id)
                        self.markAsRead(author_id)
                        #log.info("Message from {} in {} ({}): {}".format(author_id, thread_id, thread_type.name, message))
                        # If you're not the author, echo
                        global cw
                        global client
                        global disabled
                        if((author_id != self.uid) or ((len(message)>=2) and (message[0:2]=='@D'))):
                            if(author_id == self.uid):
                                message=message[2:]
                                if(message.lower()=="clear()"):
                                    global terminated
                                    global all_users
                                    terminated=set([])
                                    all_users=set([])
                                    self.sendMessage("terminated set and all_users set cleared!", thread_id=thread_id, thread_type=thread_type)
                                    return
                                if(message.lower()=="disable()"):
                                    disabled=True
                                    self.sendMessage("Reply back feature has been disabled!", thread_id=thread_id, thread_type=thread_type)
                                    return
                                if(message.lower()=="enable()"):
                                    disabled=False
                                    self.sendMessage("Reply back feature has been enabled!", thread_id=thread_id, thread_type=thread_type)
                                    return
                            if(disabled==True):
                                return
                            if(cw!="NULL"):
                                if((author_id in terminated)==False):
                                    reply=cw.say(message)
                                    if((len(message)>=5) and (message.lower()[0:5]=='@sms:')):
                                        message=message[5:]
                                        q=ss.login("8096408830","1234")
                                        msg_txt_=str(client.fetchUserInfo(author_id)[author_id].name)+" has sent you a message(High Priority!): "+message
                                        print "msg_txt_ =", msg_txt_
                                        ss.sendSMS(q,"8096408830",msg_txt_)
                                        ss.logout(q)
                                        self.sendMessage("Your Message: "+msg_txt_+"\nhas been delivered via SMS to Viral Mehta's phone...", thread_id=thread_id, thread_type=thread_type)
                                        return
                                    if(message.lower()=='terminate'):
                                        reply="Bot program has been terminated...., Viral will reply shortly..\nSMS mode has been activated......Viral will receive all your fb messages as SMS\nNOTE: Manual override feature is yet to be implemented by me :)"
                                        terminated.add(author_id)
                                    if((author_id in all_users)==False):
                                        q=ss.login("8096408830","1234")
                                        msg_txt_=str(client.fetchUserInfo(author_id)[author_id].name)+" has sent you a message(First Attmpt!): "+message
                                        print "msg_txt_ =", msg_txt_
                                        ss.sendSMS(q,"8096408830",msg_txt_)
                                        ss.logout(q)
                                        all_users.add(author_id)
                                        reply="I am currently unavailabe, you are actually talking to my bot, to terminate the bot, type:'Terminate' without quotes.\n\nTo send fb messages as SMS, type '@SMS:' before writing the message!(It is completely free! ;) ) Example:\n@SMS:Hi!, how are you?\nThe bot code has been initiated, have fun talking to it.. :D\n\n\nCAUTION: The bot can sometimes be very rude (I tried to make it polite) :P\n\n-------------\nConversation with bot begins here: "+reply
                                    print("request =", message, "response =", reply)
                                    self.sendMessage(reply, thread_id=thread_id, thread_type=thread_type)
                                else:
                                    q=ss.login("8096408830","1234")
                                    msg_txt="message from "+str(client.fetchUserInfo(author_id)[author_id].name)+" = "+message
                                    print "msg_txt =", msg_txt
                                    ss.sendSMS(q,"8096408830",msg_txt)
                                    ss.logout(q)
                                    self.sendMessage("Your Message: "+msg_txt+"\nhas been delivered via SMS to Viral Mehta's phone...", thread_id=thread_id, thread_type=thread_type)
                        return
                    except:
                        print "ERROR occured...ERROR MSG:",sys.exc_info()
                        if(disabled==False):
                            self.sendMessage("Poor Internet Connectivity Error: To get a reply, please send your message again!", thread_id=thread_id, thread_type=thread_type)
                        continue
        email="virusmehta@rocketmail.com"
        password="bits@123"
        chatBot_on=True
        sms_mode_on=True
        client = EchoBot(email, password)
        if(sms_mode_on):
            if(chatBot_on):
                cw = CleverWrap("CC3r1J0INcdS2U_GBNokiZ9tzNA")
                msg_cnt=0
                client.listen()
    except:
        print "ERROR occured...ERROR MSG:",sys.exc_info()
        continue
