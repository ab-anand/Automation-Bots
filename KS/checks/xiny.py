fetched = ['909-246-5391', '', 'DOL 01/08/2018\r',
           'Address: 4138 Mission Blvd Space 58, Montclair, CA 91763\r']

body = ['Hi i am ram,\r', '\r', '\r', '\r', 'Please send someone to sign:\r', '\r', '\r', '\r', 'Maria Reyes\r', '\r',
        'Ph: 909-246-5391 (SPANISH)\r', '\r',
        'Address: 4138 Mission Blvd Space 58, Montclair, CA 91763\r',
        '\r', 'DOL 01/08/2018\r', '\r', '\r', '\r', 'Thank you\r', '']
f2 = ['704-724-4697', '', '11833 Spring Laurel DR Charlotte, NC 28215']

b2 =  ['11833 Spring Laurel DR\r', '\r', 'Charlotte, NC 28215\r', '\r', '\r', '\r', '\r', 'The client is a referral from our chiro- she is there now about to have her\r',
       'appointment. Please reach out in the next hour!\r', '\r', '\r', '\r', 'Respectfully,\r', '']
def remaining_msg(msg, fetched):
    '''
    to return a list of the message
    lines that hasn't been printed yetq
    '''

    # msg = msg.split('\n')
    remains = []  # to contain the remaining body
    # print remains
    #msg = [x.strip() for x in msg]
    #fetched = [x.strip() for x in fetched]
    # print 'fetched ', fetched
    for fline in fetched:
        for line in msg:
            if line.find(fline) != -1:
                # print 'line: ', line
                remains.append(line)
                break
    #print 'remains1 ', remains
    
    for line in msg:
        for fline in fetched:
            if fline.find(line) != -1:
                # print 'line: ', line
                remains.append(line)
                break


    #print 'remains2 ', remains
    #print '\n', msg
    for line in remains:
        try:
            msg.remove(line)
        except:
            pass
    return msg

#print remaining_msg(body, fetched)
print remaining_msg(b2, f2)
#print fetched[3] in body
