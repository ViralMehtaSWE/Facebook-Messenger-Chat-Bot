import way2sms
def login(username,password):
    q=way2sms.sms(username,password)
    return q
def sendSMS(q, mobile_number_to_send, message):
    n=q.msgSentToday()
    if(n<100):
        q.send(mobile_number_to_send,message)
    else:
        print "ERROR: Daily SMS Limit Reached"
def logout(q):
    q.logout()
