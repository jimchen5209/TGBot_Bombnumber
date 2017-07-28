import sys
import asyncio
import random
import time
import telepot
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

"""
!!!Python3.5 above is required!!!
"""

TOKEN = '' #Insert Your Bot Token Here


cmax=999
cmin=1
class Player(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self._answer = random.randint(1,999)
        self._cmin=1
        self._cmax=999
    def _hint(self, answer, guess,cmin,cmax):
        if answer > guess:
            if cmin > guess:
                return '請給我'+str(self._cmin)+' - '+str(self._cmax)+'的數字'
            else:
                self._cmin = guess
                return str(self._cmin)+' - '+str(self._cmax)
        else:
            if cmax < guess:
                return '請給我'+str(self._cmin)+' - '+str(self._cmax)+'的數字'
            else:
                self._cmax = guess
                return str(self._cmin)+' - '+str(self._cmax)

    async def open(self, initial_msg, seed):
        content_type, chat_type, chat_id = telepot.glance(initial_msg)
        bot_me= await bot.getMe()
        username= bot_me['username'].replace(' ','')
        try:
            print('[EDIT][',initial_msg['edit_date'],']:',initial_msg['message_id'],'-->',initial_msg['text'])
        except:
            time.sleep(0)
        else:
            print('[Info] Ignoring message editing.')
            self.close()
            return
        if chat_type == 'private':
            try:
                reply_to = initial_msg['reply_to_message']['from']['id']
            except:
                if content_type == 'text':
                    try:
                        print('[Info][',initial_msg['message_id'],']',initial_msg['chat']['username'],'(',chat_id, ') :', initial_msg['text'])
                    except:
                        print('[Info][',initial_msg['message_id'],']',chat_id, ' :', initial_msg['text'])
                else:
                    try:
                        print('[Info][',initial_msg['message_id'],']',initial_msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                    except:
                        print('[Info][',initial_msg['message_id'],']',chat_id, ' sent a ', content_type)
            else:
                if content_type == 'text':
                    try:
                        print('[Info][',initial_msg['message_id'],'](Reply)',initial_msg['chat']['username'],'(',chat_id, ') :', initial_msg['text'])
                    except:
                        print('[Info][',initial_msg['message_id'],'](Reply)',chat_id, ' :', initial_msg['text'])
                else:
                    try:
                        print('[Info][',initial_msg['message_id'],'](Reply)',initial_msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                    except:
                        print('[Info][',initial_msg['message_id'],'](Reply)',chat_id, ' sent a ', content_type)
            if content_type == 'text':
                if initial_msg['text'] == '/start_game':
                    try:
                        print('[Info]',initial_msg['chat']['username'],'(',chat_id, ') has started a game with the bomb', self._answer)
                    except:
                        print('[Info]',chat_id, ' has started a game with the bomb', self._answer)
                    await self.sender.sendMessage('遊戲開始！請猜一個範圍內的數字')
                    await self.sender.sendMessage('當猜中數字時就會爆炸，你只有20秒')
                    await self.sender.sendMessage(str(self._cmin)+' - '+str(self._cmax))
                    return True  # prevent on_message() from being called on the initial message
                elif initial_msg['text'] == '/start':
                    await self.sender.sendMessage('歡迎使用炸彈數字')
                    await self.sender.sendMessage('使用 /start_game 開始一個遊戲')
                    await self.sender.sendMessage('一次回答的時間只有20秒')
                    await self.sender.sendMessage('當您猜中數字，就會爆炸')
                    await self.sender.sendMessage('遊戲中可使用 /stop 強制停止目前的遊戲')
                    self.close()
                    return
                else:
                    await self.sender.sendMessage('/start_game')
                    self.close()
                    return 
            else:
                await self.sender.sendMessage('/start_game')
                self.close()
                return
        elif chat_type == 'group' or chat_type == 'supergroup':
            try:
                reply_to = initial_msg['reply_to_message']['from']['id']
            except:
                if content_type == 'text':
                    try:
                        print('[Info][',initial_msg['message_id'],']',initial_msg['from']['username'],'(',initial_msg['from']['id'], ') in',initial_msg['chat']['title'],'(',chat_id, ') :', initial_msg['text'])
                    except:
                        print('[Info][',initial_msg['message_id'],']',initial_msg['from']['id'], ' in',initial_msg['chat']['title'],'(',chat_id, ') :', initial_msg['text'])
                elif content_type == 'new_chat_member':
                    if initial_msg['new_chat_member']['id'] == bot_me['id']:
                        try:
                            print('[Info][',initial_msg['message_id'],'] I have been joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['username'],'(',initial_msg['from']['id'],')')
                        except:
                            print('[Info][',initial_msg['message_id'],'] I have been joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['id'])
                    else:
                        try:
                            print('[Info][',initial_msg['message_id'],'] ',initial_msg['new_chat_member']['username'],' joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                        except:
                            print('[Info][',initial_msg['message_id'],'] ',initial_msg['new_chat_member']['id'],' joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                elif content_type == 'left_chat_member':
                    if initial_msg['left_chat_member']['id'] == bot_me['id']:
                        try:
                            print('[Info][',initial_msg['message_id'],'] I have been kicked from ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['username'],'(',initial_msg['from']['id'],')')
                        except:
                            print('[Info][',initial_msg['message_id'],'] I have been kicked from ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['id'])
                    else:
                        try:
                            print('[Info][',initial_msg['message_id'],'] ',initial_msg['left_chat_member']['username'],' left the ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                        except:
                            print('[Info][',initial_msg['message_id'],'] ',initial_msg['left_chat_member']['id'],' left the ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                else:
                    try:
                        print('[Info][',initial_msg['message_id'],']',initial_msg['from']['username'],'(',initial_msg['from']['id'], ') in',initial_msg['chat']['title'],'(',chat_id, ') sent a ', content_type)
                    except:
                        print('[Info][',initial_msg['message_id'],']', initial_msg['from']['id'], ' in',initial_msg['chat']['title'],'(',chat_id, ') sent a ', content_type)
            else:
                if reply_to == bot_me['id']:
                    if content_type == 'text':
                        try:
                            print('[Info][',initial_msg['message_id'],'] (Reply to me)',initial_msg['from']['username'],'(',initial_msg['from']['id'], ') in',initial_msg['chat']['title'],'(',chat_id, ') :',initial_msg['text'])
                        except:
                            print('[Info][',initial_msg['message_id'],'] (Reply to me)',initial_msg['from']['id'], ' in',initial_msg['chat']['title'],'(',chat_id, ') :',initial_msg['text'])
                    elif content_type == 'new_chat_member':
                        if initial_msg['new_chat_member']['id'] == bot_me['id']:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to me) I have been joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['username'],'(',initial_msg['from']['id'],')')
                            except:
                                print('[Info][',initial_msg['message_id'],'] (Reply to me) I have been joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['id'])
                        else:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to me)',initial_msg['new_chat_member']['username'],' joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                            except:
                                print('[Info][',initial_msg['message_id'],'] (Reply to me) ',initial_msg['new_chat_member']['id'],' joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                    elif content_type == 'left_chat_member':
                        if initial_msg['left_chat_member']['id'] == bot_me['id']:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to me) I have been kicked from ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['username'],'(',initial_msg['from']['id'],')')
                            except:
                                print('[Info][',initial_msg['message_id'],'] (Reply to me) I have been kicked from ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['id'])
                        else:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to me) ',initial_msg['left_chat_member']['username'],' left the ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                            except:
                                print('[Info][',initial_msg['message_id'],'] (Reply to me) ',initial_msg['left_chat_member']['id'],' left the ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                    else:
                        try:
                            print('[Info][',initial_msg['message_id'],'] (Reply to me)',initial_msg['from']['username'],'(',initial_msg['from']['id'], ') in',initial_msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                        except:
                            print('[Info][',initial_msg['message_id'],'] (Reply to me)',initial_msg['from']['id'], ' in',initial_msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                else:
                    if content_type == 'text':
                        try:
                            print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],')',initial_msg['from']['username'],'(',initial_msg['from']['id'], ') in',initial_msg['chat']['title'],'(',chat_id, ') :',initial_msg['text'])
                        except:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],')',initial_msg['from']['username'],'(',initial_msg['from']['id'], ') in',initial_msg['chat']['title'],'(',chat_id, ') :',initial_msg['text'])
                            except:
                                try:
                                    print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],')',initial_msg['from']['id'], ' in',initial_msg['chat']['title'],'(',chat_id, ') :',initial_msg['text'])
                                except:
                                    print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],')',initial_msg['from']['id'], ' in',initial_msg['chat']['title'],'(',chat_id, ') :',initial_msg['text'])
                    elif content_type == 'new_chat_member':
                        if initial_msg['new_chat_member']['id'] == bot_me['id']:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],') I have been joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['username'],'(',initial_msg['from']['id'],')')
                            except:
                                try:
                                    print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],') I have been joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['username'],'(',initial_msg['from']['id'],')')
                                except:
                                    try:
                                        print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],') I have been joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['id'])
                                    except:
                                        print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],') I have been joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['id'])
                        else:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],') ',initial_msg['new_chat_member']['username'],' joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                            except:
                                try:
                                    print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],') ',initial_msg['new_chat_member']['username'],' joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                                except:
                                    try:
                                        print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],') ',initial_msg['new_chat_member']['id'],' joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                                    except:
                                        print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],') ',initial_msg['new_chat_member']['id'],' joined a ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                    elif content_type == 'left_chat_member':
                        if initial_msg['left_chat_member']['id'] == bot_me['id']:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],') I have been kicked from ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['username'],'(',initial_msg['from']['id'],')')
                            except:
                                try:
                                    print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],') I have been kicked from ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['username'],'(',initial_msg['from']['id'],')')
                                except:
                                    try:
                                        print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],') I have been kicked from ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['id'])
                                    except:
                                        print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],') I have been kicked from ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,') by',initial_msg['from']['id'])
                        else:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],') ',initial_msg['left_chat_member']['username'],' left the ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                            except:
                                try:
                                    print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],') ',initial_msg['left_chat_member']['username'],' left the ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                                except:
                                    try:
                                        print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],') ',initial_msg['left_chat_member']['id'],' left the ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                                    except:
                                        print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],') ',initial_msg['left_chat_member']['id'],' left the ', chat_type,':',initial_msg['chat']['title'],'(',chat_id,')')
                    else:
                        try:
                            print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],')',initial_msg['from']['username'],'(',initial_msg['from']['id'], ') in',initial_msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                        except:
                            try:
                                print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],')',initial_msg['from']['username'],'(',initial_msg['from']['id'], ') in',initial_msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                            except:
                                try:
                                    print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['username'],')',initial_msg['from']['id'], ' in',initial_msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                                except:
                                    print('[Info][',initial_msg['message_id'],'] (Reply to ',initial_msg['reply_to_message']['from']['id'],')',initial_msg['from']['id'], ' in',initial_msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
            if content_type == 'text':
                
                if initial_msg['text'] == '/start_game' or initial_msg['text'] == '/start_game@'+username:
                    #await self.sender.sendMessage('Group MultiPlayer Coming Soon!')
                    try:
                        print('[Info]',initial_msg['from']['username'],'(',initial_msg['from']['id'], ') in',initial_msg['chat']['title'],'(',chat_id, ') has started a group game with the bomb', self._answer)
                    except:
                        print('[Info]',initial_msg['from']['id'], ' in',initial_msg['chat']['title'],'(',chat_id, ') has started a group game with the bomb', self._answer)
                    await self.sender.sendMessage('遊戲開始！請猜一個範圍內的數字',reply_to_message_id= initial_msg['message_id'])
                    await self.sender.sendMessage('當猜中數字時就會爆炸，你只有20秒')
                    markup = ForceReply()
                    await self.sender.sendMessage(str(self._cmin)+' - '+str(self._cmax), reply_markup=markup)
                    #await self.sender.sendMessage(str(self._cmin)+' - '+str(self._cmax) )
                    return True
                else:
                    self.close()
                    return
            elif content_type == 'new_chat_member':
                if initial_msg['new_chat_member']['id'] == bot_me['id']:
                    await self.sender.sendMessage('歡迎使用炸彈數字')
                    await self.sender.sendMessage('使用 /start_game 開始一個遊戲')
                    await self.sender.sendMessage('群組模式中，Bot只會受理回復他的信息')
                    await self.sender.sendMessage('一次回答的時間只有20秒')
                    await self.sender.sendMessage('當有人猜中數字，就會爆炸')
                self.close()
                return
            else:
                self.close()
                return
    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        bot_me= await bot.getMe()
        username= bot_me['username'].replace(' ','')
        try:
            print('[EDIT][',msg['edit_date'],']:',msg['message_id'],' -->',msg['text'])
        except:
            time.sleep(0)
        else:
            print('[Info] Ignoring message editing.')
            return
        if chat_type == 'private':
            try:
                reply_to = msg['reply_to_message']['from']['id']
            except:    
                if content_type != 'text':
                    try:
                        print('[Info][',msg['message_id'],']',msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                    except:
                        print('[Info][',chat_id, ' sent a ', content_type)
                    await self.sender.sendMessage('麻煩給我一個阿拉伯數字.')
                    return
                try:
                    print('[Info][',msg['message_id'],']',msg['chat']['username'],'(',chat_id, ') :', msg['text'])
                except:
                    print('[Info][',msg['message_id'],']',chat_id, ' :', msg['text'])
            else:
                if content_type != 'text':
                    try:
                        print('[Info][',msg['message_id'],'](Reply)',msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                    except:
                        print('[Info][',msg['message_id'],'](Reply)',chat_id, ' sent a ', content_type)
                    await self.sender.sendMessage('麻煩給我一個阿拉伯數字.')
                    return
                try:
                    print('[Info][',msg['message_id'],'](Reply)',msg['chat']['username'],'(',chat_id, ') :', msg['text'])
                except:
                    print('[Info][',msg['message_id'],'](Reply)',chat_id, ' :', msg['text'])
            if msg['text'] == '/stop':
                await self.sender.sendMessage('遊戲結束,炸彈是 %d' % self._answer)
                await self.sender.sendMessage('/start_game')
                try:
                    print('[Info]',msg['chat']['username'],'(',chat_id, ') has stopped his game.\n[Info] Game ended.')
                except:
                    print('[Info]',chat_id, ' has stopped his game.\n[Info] Game ended.')
                self.close()
            try:
               guess = int(msg['text'])
            except ValueError:
                await self.sender.sendMessage('麻煩給我一個阿拉伯數字.')
                return

            # check the guess against the answer ...
            if guess != self._answer:
                # give a descriptive hint
                hint = self._hint(self._answer, guess,self._cmin,self._cmax)
                await self.sender.sendMessage(hint)
            else:
                await self.sender.sendDocument('http://i.imgur.com/vjrcTIy.gif', caption='Boom!')
                #await self.sender.sendMessage('Boom!')
                await self.sender.sendMessage('遊戲結束，您引爆了炸彈')
                await self.sender.sendMessage('/start_game')
                try:
                    print('[Info]',msg['chat']['username'],'(',chat_id, ') has gotten the bomb and exploded.\n[Info] Game ended.')
                except:
                    print('[Info]',chat_id, ' has gotten the bomb and exploded.\n[Info] Game ended.')
                self.close()
        elif chat_type == 'group' or chat_type == 'supergroup':
            try:
                reply_to = msg['reply_to_message']['from']['id']
            except:
                if content_type != 'text':
                    if content_type == 'new_chat_member':
                        try:
                            print('[Info][',msg['message_id'],'] ',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                        except:
                            print('[Info][',msg['message_id'],'] ',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                    elif content_type == 'left_chat_member':
                        if msg['left_chat_member']['id'] == bot_me['id']:
                            try:
                                print('[Info][',msg['message_id'],'] I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                            except:
                                print('[Info][',msg['message_id'],'] I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                            print('[Info] Game ended.')
                            self.close()
                        else:
                            try:
                                print('[Info][',msg['message_id'],'] ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                            except:
                                print('[Info][',msg['message_id'],'] ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                    else:
                        try:
                            print('[Info][',msg['message_id'],']',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                        except:
                            print('[Info][',msg['message_id'],']',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                    return
                try:
                    print('[Info][',msg['message_id'],']',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                except:
                    print('[Info][',msg['message_id'],']',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                if msg['text'] == '/stop' or msg['text'] == '/stop@'+username:
                        await self.sender.sendMessage('遊戲結束,炸彈是 %d' % self._answer,reply_to_message_id= msg['message_id'])
                        await self.sender.sendMessage('/start_game', reply_markup=None)
                        try:
                            print('[Info]',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') has stopped the game.\n[Info] Game ended.')
                        except:
                            print('[Info]',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') has stopped the game.\n[Info] Game ended.')
                        self.close()
            else:
                if reply_to == bot_me['id']:
                    if content_type != 'text':
                        if content_type == 'new_chat_member':
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to me)',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                            except:
                                print('[Info][',msg['message_id'],'] (Reply to me)',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                        elif content_type == 'left_chat_member':
                            if msg['left_chat_member']['id'] == bot_me['id']:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to me) I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                                except:
                                    print('[Info][',msg['message_id'],'] (Reply to me) I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                                print('[Info] Game ended.')
                                self.close()
                            else:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to me) ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                except:
                                    print('[Info][',msg['message_id'],'] (Reply to me) ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                        else:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to me)',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                            except:
                                print('[Info][',msg['message_id'],'] (Reply to me)',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                            markup = ForceReply()
                            await self.sender.sendMessage('麻煩給我一個阿拉伯數字.',reply_to_message_id= msg['message_id'], reply_markup=markup)
                        return
                    try:
                        print('[Info][',msg['message_id'],'] (Reply to me)',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                    except:
                        print('[Info][',msg['message_id'],'] (Reply to me)',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                    if msg['text'] == '/stop' or msg['text'] == '/stop@'+username:
                        await self.sender.sendMessage('遊戲結束,炸彈是 %d' % self._answer,reply_to_message_id= msg['message_id'])
                        await self.sender.sendMessage('/start_game', reply_markup=None)
                        try:
                            print('[Info]',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') has stopped the game.\n[Info] Game ended.')
                        except:
                            print('[Info]',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') has stopped the game.\n[Info] Game ended.')
                        self.close()
                    try:
                       guess = int(msg['text'])
                    except ValueError:
                        markup = ForceReply()
                        await self.sender.sendMessage('麻煩給我一個阿拉伯數字.',reply_to_message_id= msg['message_id'], reply_markup=markup)
                        return

                    # check the guess against the answer ...
                    if guess != self._answer:
                        # give a descriptive hint
                        hint = self._hint(self._answer, guess,self._cmin,self._cmax)
                        markup = ForceReply()
                        await self.sender.sendMessage(hint,reply_to_message_id= msg['message_id'], reply_markup=markup)
                    else:
                        await self.sender.sendDocument('http://i.imgur.com/vjrcTIy.gif', caption='Boom!',reply_to_message_id= msg['message_id'])
                        #await self.sender.sendMessage('Boom!',reply_to_message_id= msg['message_id'])
                        await self.sender.sendMessage('遊戲結束，您引爆了炸彈',reply_to_message_id= msg['message_id'])
                        await self.sender.sendMessage('/start_game', reply_markup=None)
                        try:
                            print('[Info]',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') has gotten the bomb and exploded.\n[Info] Game ended.')
                        except:
                            print('[Info]',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') has gotten the bomb and exploded.\n[Info] Game ended.')
                        self.close()
                else:
                    if content_type != 'text':
                        if content_type == 'new_chat_member':
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                except:
                                    try:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                    except:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                        elif content_type == 'left_chat_member':
                            if msg['left_chat_member']['id'] == bot_me['id']:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                                except:
                                    try:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                                    except:
                                        try:
                                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                                        except:
                                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                                print('[Info] Game ended.')
                                self.close()
                            else:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                except:
                                    try:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                    except:
                                        try:
                                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                        except:
                                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                        else:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                                except:
                                    try:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                                    except:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                        return
                    try:
                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                    except:
                        try:
                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                        except:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                            except:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                    if msg['text'] == '/stop' or msg['text'] == '/stop@'+username:
                        await self.sender.sendMessage('遊戲結束,炸彈是 %d' % self._answer,reply_to_message_id= msg['message_id'])
                        await self.sender.sendMessage('/start_game', reply_markup=None)
                        try:
                            print('[Info]',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') has stopped the game.\n[Info] Game ended.')
                        except:
                            print('[Info]',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') has stopped the game.\n[Info] Game ended.')
                        self.close()
    async def on__idle(self, event):
        await self.sender.sendMessage('時間到. 炸彈是 %d' % self._answer)
        await self.sender.sendMessage('/start_game', reply_markup=None)
        print('[Info] Game ended due to ',event)
        self.close()
    async def on_close(self,chat_id):
        time.sleep(0)




bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Player, timeout=20),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('[Info] Bot has started')
print('[Info] Listening ...')

loop.run_forever()
