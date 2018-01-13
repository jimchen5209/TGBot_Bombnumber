import sys
import asyncio
import random
import time
import os
import io
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply


"""
$ python3.5 guessa.py <token>
"""
try:
    fs = open("./config.json", "r")
except:
    tp, val, tb = sys.exc_info()
    print("Errored when loading config.json:"+\
        str(val).split(',')[0].replace('(', '').replace("'", ""))
    programPause = input("Press any key to stop...\n")
    exit()

#load config
config = eval(fs.read())
fs.close()
TOKEN = config["TOKEN"]
Timeout = config['Timeout']
Debug = config["Debug"]
cmax = 999
cmin = 1
class Player(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self._answer = random.randint(1, 999)
        self._cmin = 1
        self._cmax = 999

    def _hint(self, answer, guess, cmin, cmax):
        if answer > guess:
            if cmin >= guess:
                return '請給我'+str(self._cmin)+' - '+str(self._cmax)+'之間的數字'
            else:
                self._cmin = guess
                return str(self._cmin)+' - '+str(self._cmax)
        else:
            if cmax <= guess:
                return '請給我'+str(self._cmin)+' - '+str(self._cmax)+'之間的數字'
            else:
                self._cmax = guess
                return str(self._cmin)+' - '+str(self._cmax)

    async def _logmsg(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        bot_me = await bot.getMe()
        #username = bot_me['username'].replace(' ', '')
        log("[Debug] Raw message:"+str(msg))
        dlog = "["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info]"
        flog = ""
        try:
            dlog = dlog+"[EDITED"+str(msg['edit_date'])+"]"
        except:
            time.sleep(0)
        try:
            fuser = await bot.getChatMember(chat_id, msg['from']['id'])
        except:
            fnick = "Channel Admin"
            fuserid = None
        else:
            fnick = fuser['user']['first_name']
            try:
                fnick = fnick + ' ' + fuser['user']['last_name']
            except:
                fnick = fnick
            try:
                fnick = fnick +"@"+ fuser['user']['username']
            except:
                fnick = fnick
            fuserid = str(fuser['user']['id'])
        if chat_type == 'private':
            dlog = dlog + "[Private]["+str(msg['message_id'])+"]"
            try:
                reply_to = msg['reply_to_message']['from']['id']
            except:
                dlog = dlog
            else:
                if reply_to == bot_me['id']:
                    dlog = dlog + "( Reply to my message "+\
                        str(msg['reply_to_message']['message_id'])+" )"
                else:
                    tuser = msg['reply_to_message']['from']['first_name']
                    try:
                        tuser = tuser + ' ' + msg['reply_to_message']['from']['last_name']
                    except:
                        tuser = tuser
                    try:
                        tuser = tuser + '@' + msg['reply_to_message']['from']['username']
                    except:
                        tuser = tuser
                    dlog = dlog + "( Reply to "+tuser+"'s message "+\
                        str(msg['reply_to_message']['message_id'])+" )"
            if content_type == 'text':
                dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) : " + msg['text']
            else:
                dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) sent a "+ content_type
            clog(dlog)
            flog = self._media_log(msg, content_type)
            if flog != None:
                clog(flog)
        elif chat_type == 'group' or chat_type == 'supergroup':
            dlog = dlog + "["+str(msg['message_id'])+"]"
            try:
                reply_to = msg['reply_to_message']['from']['id']
            except:
                dlog = dlog
            else:
                if reply_to == bot_me['id']:
                    dlog = dlog + "( Reply to my message "+\
                        str(msg['reply_to_message']['message_id'])+" )"
                else:
                    tuser = msg['reply_to_message']['from']['first_name']
                    try:
                        tuser = tuser + ' ' + msg['reply_to_message']['from']['last_name']
                    except:
                        tuser = tuser
                    try:
                        tuser = tuser + '@' + msg['reply_to_message']['from']['username']
                    except:
                        tuser = tuser
                    dlog = dlog + "( Reply to "+tuser+"'s message "+\
                        str(msg['reply_to_message']['message_id'])+" )"
            if content_type == 'text':
                dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+\
                    msg['chat']['title']+' ( '+str(chat_id)+ ' ): ' + msg['text']
            elif content_type == 'new_chat_member':
                if msg['new_chat_member']['id'] == bot_me['id']:
                    dlog = dlog+ ' I have been added to ' +msg['chat']['title']+\
                        ' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
                else:
                    tuser = msg['new_chat_member']['first_name']
                    try:
                        tuser = tuser + ' ' + msg['new_chat_member']['last_name']
                    except:
                        tuser = tuser
                    try:
                        tuser = tuser + '@' + msg['new_chat_member']['username']
                    except:
                        tuser = tuser
                    dlog = dlog+' '+ tuser +' joined the ' + chat_type+\
                         ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) '
            elif content_type == 'left_chat_member':
                if msg['left_chat_member']['id'] == bot_me['id']:
                    dlog = dlog+ ' I have been kicked from ' +msg['chat']['title']+\
                        ' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
                else:
                    tuser = msg['left_chat_member']['first_name']
                    try:
                        tuser = tuser + ' ' + msg['left_chat_member']['last_name']
                    except:
                        tuser = tuser
                    try:
                        tuser = tuser + '@' + msg['left_chat_member']['username']
                    except:
                        tuser = tuser
                    dlog = dlog+' '+ tuser +' left the ' + chat_type +\
                         ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) '
            elif content_type == 'pinned_message':
                tuser = msg['pinned_message']['from']['first_name']
                try:
                    tuser = tuser + ' ' + msg['pinned_message']['from']['last_name']
                except:
                    tuser = tuser
                try:
                    tuser = tuser + '@' + msg['pinned_message']['from']['username']
                except:
                    tuser = tuser
                tmpcontent_type, tmpchat_type, tmpchat_id = telepot.glance(msg['pinned_message'])
                if tmpcontent_type == 'text':
                    dlog = dlog + tuser + "'s message["+\
                        str(msg['pinned_message']['message_id'])+"] was pinned to "+\
                        msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + \
                            " ( "+fuserid+" ):\n"+msg['pinned_message']['text']
                else:
                    dlog = dlog + tuser + "'s message["+str(msg['pinned_message']['message_id'])+\
                        "] was pinned to "+msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+\
                         fnick + " ( "+fuserid+" )"
                    flog = self._media_log(msg, tmpcontent_type)
                    if flog != None:
                        clog(flog)
            elif content_type == 'new_chat_photo':
                dlog = dlog + "The photo of this "+chat_type+""+ ' '+msg['chat']['title']+\
                    ' ( '+str(chat_id)+ ' ) was changed by '+fnick + " ( "+fuserid+" )"
                flog = "[New Chat Photo]"
                photo_array = msg['new_chat_photo']
                photo_array.reverse()
                try:
                    flog = flog + "Caption = " +msg['caption'] +\
                        " ,FileID:"+ photo_array[0]['file_id']
                except:
                    flog = flog +"FileID:"+ photo_array[0]['file_id']
            elif content_type == 'delete_chat_photo':
                dlog = dlog + "The photo of this "+chat_type+ \
                    " was deleted by "+fnick + " ( "+fuserid+" )"
            elif content_type == 'new_chat_title':
                dlog = dlog + "The title of this "+chat_type+ \
                    " was changed to "+msg['new_chat_title']+" by "+fnick + " ( "+fuserid+" )"
            else:
                dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+msg['chat']['title']+\
                    ' ( '+str(chat_id)+ ' ) sent a '+ content_type
            clog(dlog)
            flog = self._media_log(msg, content_type)
            if flog != None:
                clog(flog)
        elif chat_type == 'channel':
            dlog = dlog + "["+str(msg['message_id'])+"]"
            try:
                reply_to = msg['reply_to_message']
            except:
                dlog = dlog
            else:
                dlog = dlog + "( Reply to "+\
                    str(msg['reply_to_message']['message_id'])+" )"
            if content_type == 'text':
                dlog = dlog+ ' ' + fnick
                if fuserid:
                    dlog = dlog + " ( "+fuserid+" )"
                dlog = dlog + " in channel "+msg['chat']['title']+\
                    ' ( '+str(chat_id)+ ' ): ' + msg['text']
            elif content_type == 'new_chat_photo':
                dlog = dlog + "The photo of this "+chat_type+""+ ' '+\
                    msg['chat']['title']+' ( '+str(chat_id)+ ' ) was changed by '+fnick
                if fuserid:
                    dlog = dlog+ " ( "+fuserid+" )"
                flog = "[New Chat Photo]"
                photo_array = msg['new_chat_photo']
                photo_array.reverse()
                try:
                    flog = flog + "Caption = " +msg['caption'] +\
                        " ,FileID:"+ photo_array[0]['file_id']
                except:
                    flog = flog +"FileID:"+ photo_array[0]['file_id']
            elif content_type == 'delete_chat_photo':
                dlog = dlog + "The photo of this "+chat_type+ " was deleted by "+fnick
                if fuserid:
                    dlog = dlog+ " ( "+fuserid+" )"
            elif content_type == 'new_chat_title':
                dlog = dlog + "The title of this "+chat_type+ \
                    " was changed to "+msg['new_chat_title']+" by "+fnick
                if fuserid:
                    dlog = dlog+ " ( "+fuserid+" )"
            else:
                dlog = dlog + ' ' + fnick
                if fuserid:
                    dlog = dlog + " ( "+fuserid+" )"
                dlog = dlog +" in channel"+msg['chat']['title']+\
                    ' ( '+str(chat_id)+ ' ) sent a '+ content_type
            clog(dlog)
            flog = self._media_log(msg, content_type)
            if flog != None:
                clog(flog)
    def _media_log(self, msg, content_type):
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array = msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
            except:
                flog = flog +"FileID:"+ msg['audio']['file_id']
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
            except:
                flog = flog +"FileID:"+ msg['document']['file_id']
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
            except:
                flog = flog +"FileID:"+ msg['video']['file_id']
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
            except:
                flog = flog +"FileID:"+ msg['voice']['file_id']
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
            except:
                flog = flog +"FileID:"+ msg['sticker']['file_id']
        else:
            flog = None
        return flog

    async def open(self, initial_msg, seed):
        await self._logmsg(initial_msg)
        content_type, chat_type, chat_id = telepot.glance(initial_msg)
        bot_me = await bot.getMe()
        username = bot_me['username'].replace(' ', '')
        try:
            print('[EDIT]['+str(initial_msg['edit_date'])+']:'+\
                str(initial_msg['message_id'])+'-->'+initial_msg['text'])
        except:
            time.sleep(0)
        else:
            self.close()
            return
        try:
            fuser = await bot.getChatMember(chat_id, initial_msg['from']['id'])
        except:
            fnick = "Channel Admin"
            fuserid = None
        else:
            fnick = fuser['user']['first_name']
            try:
                fnick = fnick + ' ' + fuser['user']['last_name']
            except:
                fnick = fnick
            try:
                fnick = fnick +"@"+ fuser['user']['username']
            except:
                fnick = fnick
            fuserid = str(fuser['user']['id'])
        if chat_type == 'private':
            if content_type == 'text':
                if initial_msg['text'] == '/start_game':
                    clog('[Info] '+fnick+'('+fuserid+\
                         ') has started a game with the bomb '+ str(self._answer))
                    dre = await self.sender.sendMessage('遊戲開始！請猜一個範圍內的數字')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('當猜中數字時就會爆炸，你只有 '+str(Timeout)+' 秒')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage(str(self._cmin)+' - '+str(self._cmax))
                    log("[Debug] Raw sent data:"+str(dre))
                    return True  # prevent on_message() from being called on the initial message
                elif initial_msg['text'] == '/start':
                    dre = await self.sender.sendMessage('歡迎使用炸彈數字')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('使用 /start_game 開始一個遊戲')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('一次回答的時間只有 '+str(Timeout)+' 秒')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('當您猜中數字，就會爆炸')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('遊戲中可使用 /stop 強制停止目前的遊戲')
                    log("[Debug] Raw sent data:"+str(dre))
                    self.close()
                    return
                else:
                    dre = await self.sender.sendMessage('/start_game')
                    log("[Debug] Raw sent data:"+str(dre))
                    self.close()
                    return
            else:
                await self.sender.sendMessage('/start_game')
                self.close()
                return
        elif chat_type == 'group' or chat_type == 'supergroup':
            if content_type == 'text':
                if initial_msg['text'] == '/start_game' or \
                    initial_msg['text'] == '/start_game@'+username:
                    clog('[Info] '+fnick+'('+fuserid+ ') in '+ initial_msg['chat']['title']+\
                        ' ('+str(chat_id)+ ') has started a group game with the bomb '+ \
                        str(self._answer))
                    dre = await self.sender.sendMessage('遊戲開始！請猜一個範圍內的數字', \
                        reply_to_message_id=initial_msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('當猜中數字時就會爆炸，你只有 '+str(Timeout)+' 秒')
                    log("[Debug] Raw sent data:"+str(dre))
                    markup = ForceReply()
                    dre = await self.sender.sendMessage(str(self._cmin)+' - '+str(self._cmax),\
                     reply_markup=markup)
                    log("[Debug] Raw sent data:"+str(dre))
                    return True
                else:
                    self.close()
                    return
            elif content_type == 'new_chat_member':
                if initial_msg['new_chat_member']['id'] == bot_me['id']:
                    dre = await self.sender.sendMessage('歡迎使用炸彈數字')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('使用 /start_game 開始一個遊戲')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('群組模式中，Bot只會受理回復他的信息')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('一次回答的時間只有 '+str(Timeout)+' 秒')
                    log("[Debug] Raw sent data:"+str(dre))
                    dre = await self.sender.sendMessage('當有人猜中數字，就會爆炸')
                    log("[Debug] Raw sent data:"+str(dre))
                self.close()
                return
            else:
                self.close()
                return
        return True  # prevent on_message() from being called on the initial message

    async def on_chat_message(self, msg):
        await self._logmsg(msg)
        content_type, chat_type, chat_id = telepot.glance(msg)
        bot_me = await bot.getMe()
        username = bot_me['username'].replace(' ', '')
        try:
            fuser = await bot.getChatMember(chat_id, msg['from']['id'])
        except:
            fnick = "Channel Admin"
            fuserid = None
        else:
            fnick = fuser['user']['first_name']
            try:
                fnick = fnick + ' ' + fuser['user']['last_name']
            except:
                fnick = fnick
            try:
                fnick = fnick +"@"+ fuser['user']['username']
            except:
                fnick = fnick
            fuserid = str(fuser['user']['id'])
        if chat_type == 'private':
            if content_type != 'text':
                dre = await self.sender.sendMessage('麻煩給我一個阿拉伯數字.')
                log("[Debug] Raw sent data:"+str(dre))
                return
            if msg['text'] == '/stop':
                dre = await self.sender.sendMessage('遊戲結束,炸彈是 %d' % self._answer)
                log("[Debug] Raw sent data:"+str(dre))
                dre = await self.sender.sendMessage('/start_game')
                log("[Debug] Raw sent data:"+str(dre))
                clog('[Info] '+fnick+' ('+fuserid+ ') has stopped the game.\n[Info] Game ended.')
                self.close()
            try:
                guess = int(msg['text'])
            except ValueError:
                dre = await self.sender.sendMessage('麻煩給我一個阿拉伯數字.')
                log("[Debug] Raw sent data:"+str(dre))
                return

            # check the guess against the answer ...
            if guess != self._answer:
                # give a descriptive hint
                hint = self._hint(self._answer, guess, self._cmin, self._cmax)
                dre = await self.sender.sendMessage(hint)
                log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = await self.sender.sendDocument(\
                    'http://i.imgur.com/vjrcTIy.gif', caption='Boom!')
                log("[Debug] Raw sent data:"+str(dre))
                dre = await self.sender.sendMessage('遊戲結束，您引爆了炸彈')
                log("[Debug] Raw sent data:"+str(dre))
                dre = await self.sender.sendMessage('/start_game')
                log("[Debug] Raw sent data:"+str(dre))
                clog('[Info] '+fnick+' ('+fuserid+\
                     ') has gotten the bomb and exploded.\n[Info] Game ended.')
                self.close()
        elif chat_type == 'group' or chat_type == 'supergroup':
            try:
                reply_to = msg['reply_to_message']['from']['id']
            except:
                if content_type != 'text':
                    if content_type == 'left_chat_member':
                        if msg['left_chat_member']['id'] == bot_me['id']:
                            clog('[Info] Game ended.')
                            self.close()
                else:
                    if msg['text'] == '/stop' or msg['text'] == '/stop@'+username:
                        markup = ForceReply()
                        dre = await self.sender.sendMessage(self._answer, reply_markup=markup)
                        log("[Debug] Raw sent data:"+str(dre))
                        msg_idf = telepot.message_identifier(dre)
                        await bot.deleteMessage(msg_idf)
                        dre = await self.sender.sendMessage('遊戲結束,炸彈是 %d' % self._answer,\
                            reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                        dre = await self.sender.sendMessage('/start_game', reply_markup=None)
                        log("[Debug] Raw sent data:"+str(dre))
                        clog('[Info] '+fnick+' ('+fuserid+ ') in '+msg['chat']['title']+\
                            ' ('+str(chat_id)+ ') has stopped the game.\n[Info] Game ended.')
                        self.close()
                return
            else:
                if reply_to == bot_me['id']:
                    if content_type != 'text':
                        if content_type == 'left_chat_member':
                            if msg['left_chat_member']['id'] == bot_me['id']:
                                clog('[Info] Game ended.')
                                self.close()
                        else:
                            markup = ForceReply()
                            dre = await self.sender.sendMessage('麻煩給我一個阿拉伯數字.',\
                                reply_to_message_id=msg['message_id'], reply_markup=markup)
                            log("[Debug] Raw sent data:"+str(dre))
                        return
                    if msg['text'] == '/stop' or msg['text'] == '/stop@'+username:
                        markup = ForceReply()
                        dre = await self.sender.sendMessage(self._answer, reply_markup=markup)
                        log("[Debug] Raw sent data:"+str(dre))
                        msg_idf = telepot.message_identifier(dre)
                        await bot.deleteMessage(msg_idf)
                        dre = await self.sender.sendMessage('遊戲結束,炸彈是 %d' % self._answer,
                                                            reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                        dre = await self.sender.sendMessage('/start_game', reply_markup=None)
                        log("[Debug] Raw sent data:"+str(dre))
                        clog('[Info] '+fnick+' ('+fuserid+ ') in '+msg['chat']['title']+\
                            ' ('+str(chat_id)+ ') has stopped the game.\n[Info] Game ended.')
                        self.close()
                    try:
                        guess = int(msg['text'])
                    except ValueError:
                        markup = ForceReply()
                        dre = await self.sender.sendMessage('麻煩給我一個阿拉伯數字.',\
                            reply_to_message_id=msg['message_id'], reply_markup=markup)
                        log("[Debug] Raw sent data:"+str(dre))
                        return

                    # check the guess against the answer ...
                    if guess != self._answer:
                        # give a descriptive hint
                        hint = self._hint(self._answer, guess, self._cmin, self._cmax)
                        markup = ForceReply()
                        dre = await self.sender.sendMessage(hint,\
                            reply_to_message_id=msg['message_id'], reply_markup=markup)
                        log("[Debug] Raw sent data:"+str(dre))
                    else:
                        markup = ForceReply()
                        dre = await self.sender.sendMessage(self._answer, reply_markup=markup)
                        log("[Debug] Raw sent data:"+str(dre))
                        msg_idf = telepot.message_identifier(dre)
                        await bot.deleteMessage(msg_idf)
                        dre = await self.sender.sendDocument('http://i.imgur.com/vjrcTIy.gif',\
                            caption='Boom!', reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                        dre = await self.sender.sendMessage('遊戲結束，您引爆了炸彈',\
                            reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                        dre = await self.sender.sendMessage('/start_game', reply_markup=None)
                        log("[Debug] Raw sent data:"+str(dre))
                        clog('[Info] '+fnick+' ('+fuserid+ ') in '+msg['chat']['title']+' ('+\
                            str(chat_id)+') has gotten the bomb and exploded.\n[Info] Game ended.')
                        self.close()
                else:
                    if content_type == 'text':
                        if msg['text'] == '/stop' or msg['text'] == '/stop@'+username:
                            markup = ForceReply()
                            dre = await self.sender.sendMessage(self._answer, reply_markup=markup)
                            log("[Debug] Raw sent data:"+str(dre))
                            msg_idf = telepot.message_identifier(dre)
                            await bot.deleteMessage(msg_idf)
                            dre = await self.sender.sendMessage('遊戲結束,炸彈是 %d' % self._answer,\
                                reply_to_message_id=msg['message_id'])
                            log("[Debug] Raw sent data:"+str(dre))
                            dre = await self.sender.sendMessage('/start_game', reply_markup=None)
                            log("[Debug] Raw sent data:"+str(dre))
                            clog('[Info] '+fnick+' ('+fuserid+ ') in '+msg['chat']['title']+\
                                ' ('+str(chat_id)+ ') has stopped the game.\n[Info] Game ended.')
                            self.close()

    async def on__idle(self, event):
        dre = await self.sender.sendMessage('時間到. 炸彈是 %d' % self._answer)
        dre = await self.sender.sendMessage('/start_game', reply_markup=None)
        clog('[Info] The game of '+str(event['_idle']['source']['id'])+\
            ' has expired.\n[Info] Game ended.')
        self.close()
    async def on_close(self, chat_id):
        time.sleep(0)

def clog(text):
    print(text)
    log(text)
    return

def log(text):
    if text[0:7] == "[Debug]":
        if Debug == True:
            logger = io.open(logpath+"-debug.log","a",encoding='utf8')
            logger.write("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"]"+text+"\n")
            logger.close()
        return
    logger= io.open(logpath+".log", "a", encoding='utf8')
    logger.write(text+"\n")
    logger.close()
    return

if os.path.isdir("./logs") == False:
    os.mkdir("./logs")
logpath = "./logs/"+time.strftime("%Y-%m-%d-%H-%M-%S").replace("'", "")
log("[Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
log("[Debug][Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
log("[Debug] Bot's TOKEN is "+TOKEN)
bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Player, timeout=Timeout),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info] Bot has started")
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info] Listening ...")

loop.run_forever()
