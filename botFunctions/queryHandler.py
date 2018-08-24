# -*- coding: utf-8 -*-
from botFunctions import *
import ast
import emojiList


def superAdminHandler(bot, types, call, status):
    superAdminList = detailsOfSuperAdmins()
    if not superAdminList:
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                  text="No Super Admins " + emojiList.failFaceIcon)
        adminWindow(bot, types, call.message, True)
        if status:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        title = "<b>Super Admin List</b>"
        markup = types.InlineKeyboardMarkup()
        for adminID in superAdminList:
            adminDetails = userDetailFormatter(adminID)
            if adminID[3] != '':
                markup.add(types.InlineKeyboardButton(text=adminDetails,
                                                      url='https://telegram.me/' + adminID[3] + '?start=XXXX'),
                           types.InlineKeyboardButton(text=emojiList.crossIcon,
                                                      callback_data="['superadmin'," + str(adminID[0]) + "]"))
            else:
                markup.add(types.InlineKeyboardButton(text=adminDetails, callback_data='noUserName'),
                           types.InlineKeyboardButton(text=emojiList.crossIcon,
                                                      callback_data="['superadmin'," + str(adminID[0]) + "]"))
        markup.add(types.InlineKeyboardButton(emojiList.backIcon, callback_data="backToHome"))
        if status:
            bot.edit_message_text(chat_id=call.message.chat.id, text=title, message_id=call.message.message_id,
                                  reply_markup=markup, parse_mode='HTML')
        else:
            bot.send_message(chat_id=call.message.chat.id, text=title, reply_markup=markup, parse_mode='HTML')


def removeSuperAdminQuery(bot, types, call):
    removeID = ast.literal_eval(call.data)[1]
    if removeFromSuperAdmin(removeID):
        successMessage = "Super Admin Successfully Deleted " + emojiList.successFaceIcon
    else:
        successMessage = "Super Admin Deletion Failed " + emojiList.failFaceIcon
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=successMessage)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    superAdminHandler(bot, types, call, False)


def allgroupsHandler(bot, types, call, status):
    title = "<b>All Groups</b>\n\n"
    markup = types.InlineKeyboardMarkup()
    allGroupCount = allgroupsDB().__len__()
    allBanedGroupCount = getBanGroups().__len__()
    title = title + emojiList.houseIcon + " All Group Count : " + str(allGroupCount) + "\n" \
            + emojiList.bannedGroupIcon + " All Banned Group Count : " + str(allBanedGroupCount)
    markup.add(types.InlineKeyboardButton(text="All Groups", callback_data="groups"),
               types.InlineKeyboardButton(text="All Banned Groups", callback_data="bannedgroups"))
    markup.add(types.InlineKeyboardButton(emojiList.backIcon, callback_data="backToHome"))
    if status:
        bot.edit_message_text(chat_id=call.message.chat.id, text=title, message_id=call.message.message_id,
                              reply_markup=markup, parse_mode='HTML')
    else:
        bot.send_message(chat_id=call.chat.id, text=title, reply_markup=markup,
                         parse_mode='HTML')


def bannedGroupHandler(bot, types, call, status):
    title = "<b>Banned Group List</b>"
    markup = types.InlineKeyboardMarkup()
    groupList = getBannedGroupIDTitle()
    if not groupList:
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                  text="No Banned Groups " + emojiList.failFaceIcon)
        allgroupsHandler(bot, types, call.message, False)
        if status:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        for groupID in groupList:
            markup.add(
                types.InlineKeyboardButton(text=groupID[1], callback_data="noGroupName"),
                types.InlineKeyboardButton(text=emojiList.crossIcon,
                                           callback_data="['sureRemoveBannedGroup'," + str(groupID[0]) + "]"))
        markup.add(types.InlineKeyboardButton(emojiList.backIcon, callback_data="backToAllGroup"))
        if status:
            bot.edit_message_text(chat_id=call.message.chat.id, text=title,
                                  message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')
        else:
            bot.send_message(chat_id=call.message.chat.id, text=title, reply_markup=markup,
                             parse_mode='HTML')


def removeBannedGroup(bot, types, call):
    removeID = ast.literal_eval(call.data)[1]
    if removeFromBanGroup(removeID):
        successMessage = "Banned Group Successfully Deleted " + emojiList.successFaceIcon
    else:
        successMessage = "Banned Group Deletion Failed " + emojiList.failFaceIcon
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=successMessage)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bannedGroupHandler(bot, types, call, False)


def groupHandler(bot, types, call, status):
    title = "<b>Group List</b>"
    markup = types.InlineKeyboardMarkup()
    groupList = getGroupIDTitle()
    if not groupList:
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                  text="No Groups " + emojiList.failFaceIcon)
        allgroupsHandler(bot, types, call.message, False)
        if status:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        for groupID in groupList:
            markup.add(
                types.InlineKeyboardButton(text=groupID[1], callback_data="['viewgroup'," + str(groupID[0]) + "]"))
        markup.add(types.InlineKeyboardButton(emojiList.backIcon, callback_data="backToAllGroup"))
        if status:
            bot.edit_message_text(chat_id=call.message.chat.id, text=title,
                                  message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')
        else:
            bot.send_message(chat_id=call.message.chat.id, text=title, reply_markup=markup,
                             parse_mode='HTML')


def removeGroup(bot, types, call):
    removeID = ast.literal_eval(call.data)[1]
    addToBanGroup(removeID)
    if removeFromGroup(removeID):
        successMessage = "Group Successfully Deleted " + emojiList.successFaceIcon
    else:
        successMessage = "Group Deletion Failed " + emojiList.failFaceIcon
    bot.send_message(chat_id=removeID,
                     text="Sorry, <b>Bot admin</b> has decided to <b>kick</b> me from this group " + emojiList.failFaceIcon,
                     parse_mode='HTML')
    bot.leave_chat(chat_id=removeID)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=successMessage)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    groupHandler(bot, types, call, False)


def viewGroupInfo(bot, types, call, passID):
    if passID == '':
        groupID = ast.literal_eval(call.data)[1]
    else:
        groupID = passID
    markup = types.InlineKeyboardMarkup()
    if isBotCanDeleteMessage(bot, groupID):
        markup.add(types.InlineKeyboardButton("Sticker Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('stickerPermission', groupID)) + "', 'Sticker Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission('stickerPermission',
                                                                                                    groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('stickerPermission',
                                                                   groupID)) + ", 'stickerPermission', 'Sticker']"))

        markup.add(types.InlineKeyboardButton("HHH Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('hhhPermission', groupID)) + "', 'HHH Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission('hhhPermission',
                                                                                                    groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('hhhPermission',
                                                                   groupID)) + ", 'hhhPermission', 'HHH']"))

        markup.add(types.InlineKeyboardButton("Photo Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('photoPermission', groupID)) + "', 'Photo Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission('photoPermission',
                                                                                                    groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('photoPermission',
                                                                   groupID)) + ", 'photoPermission', 'Photo']"))

        markup.add(types.InlineKeyboardButton("Audio Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('audioPermission', groupID)) + "', 'Audio Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission('audioPermission',
                                                                                                    groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('audioPermission',
                                                                   groupID)) + ", 'audioPermission', 'Audio']"))

        markup.add(types.InlineKeyboardButton("Video Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('videoPermission', groupID)) + "', 'Video Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission('videoPermission',
                                                                                                    groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('videoPermission',
                                                                   groupID)) + ", 'videoPermission', 'Video']"))

        markup.add(types.InlineKeyboardButton("Document Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('documentPermission', groupID)) + "', 'Document Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission(
                           'documentPermission',
                           groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('documentPermission',
                                                                   groupID)) + ", 'documentPermission', 'Document']"))

        markup.add(types.InlineKeyboardButton("Text Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('textPermission', groupID)) + "', 'Text Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission('textPermission',
                                                                                                    groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('textPermission',
                                                                   groupID)) + ", 'textPermission', 'Text']"))

        markup.add(types.InlineKeyboardButton("Location Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('locationPermission', groupID)) + "', 'Location Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission(
                           'locationPermission',
                           groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('locationPermission',
                                                                   groupID)) + ", 'locationPermission', 'Location']"))

        markup.add(types.InlineKeyboardButton("Contact Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('contactPermission', groupID)) + "', 'Contact Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission('contactPermission',
                                                                                                    groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('contactPermission',
                                                                   groupID)) + ", 'contactPermission', 'Contact']"))

        markup.add(types.InlineKeyboardButton("Voice Permission", callback_data="['permission','" + str(
            getStatusOfGroupPermission('voicePermission', groupID)) + "', 'Voice Permission' ]"),
                   types.InlineKeyboardButton(
                       text=emojiList.permissionTrueIcon if getStatusOfGroupPermission('voicePermission',
                                                                                                    groupID) else emojiList.permissionFalseIcon,
                       callback_data="['cp', " + str(groupID) + ", " + str(
                           getStatusOfGroupPermission('voicePermission',
                                                                   groupID)) + ", 'voicePermission', 'Voice']"))

    markup.add(types.InlineKeyboardButton(emojiList.backIcon, callback_data="groups"),
               types.InlineKeyboardButton(text=emojiList.crossIcon, callback_data="['group'," + str(groupID) + "]"))
    bot.edit_message_text(chat_id=call.message.chat.id, text=structureGroupDetails(bot, groupID),
                          message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')


def changePermissionStatus(bot, types, call):
    groupID = ast.literal_eval(call.data)[1]
    permissionStatus = ast.literal_eval(call.data)[2]
    permissionColumn = ast.literal_eval(call.data)[3]
    permissionName = ast.literal_eval(call.data)[4]
    if permissionStatus:
        if changePermissionInGroups('False', permissionColumn, groupID):
            viewGroupInfo(bot, types, call, groupID)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text=permissionName + " Permission successfully disable " + emojiList.successFaceIcon)

        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Failed to disable " + permissionName + " permission " + emojiList.successFaceIcon)
    else:
        if changePermissionInGroups('True', permissionColumn, groupID):
            viewGroupInfo(bot, types, call, groupID)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text=permissionName + " Permission Successfully enable " + emojiList.successFaceIcon)
        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Failed to enable " + permissionName + " permission" + emojiList.successFaceIcon)


def displayPermissionStatus(bot, call):
    permissionStatus = ast.literal_eval(call.data)[1]
    permissionName = ast.literal_eval(call.data)[2]
    if permissionStatus == 'True':
        text = "Click " + emojiList.permissionTrueIcon + " to disable " + permissionName
    else:
        text = "Click " + emojiList.permissionFalseIcon + " to enable " + permissionName
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=text)
