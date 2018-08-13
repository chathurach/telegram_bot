# -*- coding: utf-8 -*-
import re
import ast
import botFunctions
import configuration
import emojiList

def setupFullName(name):
    firstName = name.first_name if name.first_name!=None else ''
    lastName = " " + name.last_name if name.last_name!=None else ''
    userName = " " + name.username if name.username!=None else ''
    fullName = firstName + lastName + userName
    return fullName

def getName(name):
    if(name.username == None):
        if(name.last_name!=None):
            return name.first_name + " " + name.last_name
        return name.first_name
    else:
        return '@' + name.username

def exceptionHandling(message, bot, types, name):
    inline = types.InlineKeyboardMarkup()
    START = types.InlineKeyboardButton(text='START', callback_data='START')
    inline.row(START)
    bot.send_message(message.chat.id, text='Agent ' + getName(name) +' Click the START button to Activate the @'+str(configuration.botUsername) + " " + emojiList.successFaceIcon, reply_markup=inline)

def allCheck(text):
    search = re.findall(r"\B@all\b", text, re.I)
    if(len(search)>0):
        return True
    else:
        return False

def checkAdmin(bot, chatID, userID):
    for chat in bot.get_chat_administrators(chatID):
        if(chat.user.id==userID and chat.user.is_bot==False):
            return True
    if(isUserSuperAdmin(userID)):
        return True
    return False

def isUserSuperAdmin(userID):
    if(userID==configuration.admin):
        return True
    for admin in botFunctions.getAdmin():
        if(admin==str(userID)):
            return True
    return False

def mentionedList(groupID, text):
    mentionedList = []
    listAT = re.findall(r'[@]\w*\b', text)
    listAT = list(set(listAT))
    if(len(listAT)>0):
        for uname in listAT:
            username = re.split(r'[@]', uname)[1]
            userID = botFunctions.getMentionedUser(groupID, username.lower())
            if userID != '':
                mentionedList.append(userID)
    listSUB = re.split('\W+', text)
    listSUB = list(set(listSUB))
    if (len(listSUB) > 0):
        for subname in listSUB:
            userID = botFunctions.getSubscribeUser(subname.lower())
            if(len(userID)>0):
                for uID in userID:
                    mentionedList.append(uID)
    mentionedList = list(set(mentionedList))
    finalMentionedUsers = []
    for getAllUsers in botFunctions.getAllUsers(groupID):
        for mentionUsers in mentionedList:
            if(str(getAllUsers)==str(mentionUsers)):
                finalMentionedUsers.append(mentionUsers)
    return finalMentionedUsers

def isBotAdmin(bot, message):
    for getID in bot.get_chat_administrators(message.chat.id):
        if(getID.user.id==configuration.botID):
            if(getID.can_delete_messages):
                return True
    return False

def stringToBoolean(text):
    if(text=='True'):
        return True
    else:
        return False

# def updateGroupID(message):
#     for IDTitle in botFunctions.getGroupIDTitle():
#         if(str(message.chat.id) == IDTitle[0]):
#             botFunctions.updateGroupTitle(message.chat.id, message.chat.title)
#             return
#         if(message.chat.title==IDTitle[1]):
#             botFunctions.updateGroupID(message)

def autoAddDetails(message, bot, types):
    botFunctions.addToUser(message.chat.id, message.from_user.id)
    if (botFunctions.addToAllUser(message.from_user) == 'success'):
        for admin in bot.get_chat_administrators(chat_id=message.chat.id):
            try:
                bot.send_message(chat_id=admin.user.id, text='<b>Tell</b> ' + getName(message.from_user) + ' <b>to START me in privately. This is important, otherwise I cannot send message to</b> '+ getName(message.from_user) + " " + emojiList.failFaceIcon,  parse_mode='HTML')
            except:
                print('Cannot send message to admin')
        exceptionHandling(message, bot, types, message.from_user)
        return
    botFunctions.updateToAllUser(message.from_user)

def formatUserData(user):
    firstName = ''
    lastName = ''
    userName = ''

    if(user.first_name != '' and user.first_name != None):
        firstName = user.first_name
    if (user.last_name != '' and user.last_name != None):
        lastName = user.last_name
    if (user.username != '' and user.username != None):
        userName = user.username.lower()

    return firstName, lastName, userName

def groupAndSuperAdmin(bot, message):
    adminID = botFunctions.getAdmin()
    adminID.append(str(configuration.admin))
    allUsersID = botFunctions.getAllUsers(message.chat.id)
    return list(set([i for i in adminID if i in allUsersID] + [str(k.user.id) for k in bot.get_chat_administrators(message.chat.id) if k.user.is_bot == False]))

def userDetailFormatter(detail):
    userDetails = detail[1]
    if (detail[2] != ''):
        userDetails = userDetails + detail[2]
    if (detail[3] != ''):
        userDetails = userDetails + ' ---> @' + detail[3]
    return userDetails

def jsonUserDetailFormatter(detail):
    userDetails = detail[1]
    if (detail[2] != None):
        userDetails = userDetails + detail[2]
    if (detail[3] != None):
        userDetails = userDetails + ' (@' + detail[3] + ')'
    return userDetails

def sureOrNot(bot, types, call):
    searchID = ast.literal_eval(call.data)[1]
    if(call.data.startswith("['superadmin'")):
        groupOrUser = "Super Admin"
        userGroupDetails = userDetailFormatter(botFunctions.detailsOfUser(searchID))
        callBackDetails = "['removesuperadmin',"+str(searchID)+"]"
    else:
        groupOrUser = "Group"
        userGroupDetails = botFunctions.detailsOfGroup(searchID)
        callBackDetails = "['removegroup',"+str(searchID)+"]"
    message = """<b>Are you sure want to remove this """+groupOrUser+"""?</b>
""" + userGroupDetails + """
"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Yes", callback_data=callBackDetails), types.InlineKeyboardButton("No", callback_data="no"))
    bot.send_message(chat_id=call.message.chat.id, text=message, reply_markup=markup, parse_mode='HTML')

def memberInTheGroup(bot, groupID, userID):
    try:
        bot.get_chat_member(chat_id=groupID, user_id=userID)
        return True
    except Exception as inst:
        if(re.split(r"USER_ID_INVALID", str(inst))):
            botFunctions.leftOfKikMember(groupID, userID)
            return False
        else:
            return True

def checkGroupStatus(bot, message):
     groupIDList = botFunctions.allgroupsDB()
     if(not str(message.chat.id) in groupIDList):
         adminMessage = "<b>Found a group which is not in the DataBase</b>" + emojiList.exclamationMarkIcon + "\n\nGroup Title : <b>" + message.chat.title + "</b> (" + str(
             message.chat.id) + ")\nGroup Members Count : " + str((bot.get_chat_members_count(
             chat_id=message.chat.id)) - 1) + "\nGroup Type : " + message.chat.type + "\nCreator & Admins : \n\n"

         for admin in bot.get_chat_administrators(chat_id=message.chat.id):
             adminMessage = adminMessage + setupFullName(admin.user) + ' - ' + admin.status + '\n'

         bot.send_message(chat_id=message.chat.id,
                          text="We <b>cannot find</b> any <b>data</b> related to this Bot <b>in</b> the <b>DataBase</b>. " + emojiList.failFaceIcon + " It will be <b>reported</b> to creator of this Bot\n\nThank You " + emojiList.successFaceIcon,
                          parse_mode='HTML')
         bot.leave_chat(chat_id=message.chat.id)

         bot.send_message(chat_id=configuration.admin, text=adminMessage, parse_mode='HTML')
         botFunctions.kikBotDB(message.chat.id)
         return