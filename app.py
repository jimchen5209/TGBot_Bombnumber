import sys
import asyncio
import random
import telepot
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space

"""
$ python3.5 guessa.py <token>

Guess a number:

1. Send the bot anything to start a game.
2. The bot randomly picks an integer between 0-99.
3. You make a guess.
4. The bot tells you to go higher or lower.
5. Repeat step 3 and 4, until guess is correct.
"""
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
        if content_type == 'text':
            print('[Info]',chat_id, ':', initial_msg['text'])
            if initial_msg['text'] == '/start':
                print('[Info]',chat_id, 'has started a game with the bomb', self._answer)
                await self.sender.sendMessage('遊戲開始！請猜一個範圍內的數字')
                await self.sender.sendMessage('當猜中數字時就會爆炸')
                await self.sender.sendMessage(str(self._cmin)+' - '+str(self._cmax))
                return True  # prevent on_message() from being called on the initial message
            else:
                await self.sender.sendMessage('/start')
                self.close()
                return 
        else:
            print('[Info]',chat_id, ' sent a ', content_type)
            await self.sender.sendMessage('/start')
            self.close()
            return 
        
    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            print('[Info]',chat_id, 'sent a ', content_type)
            await self.sender.sendMessage('麻煩給我一個數字.')
            return
        print('[Info]',chat_id, ':', msg['text'])
        if msg['text'] == '/stop':
            await self.sender.sendMessage('遊戲結束,炸彈是 %d' % self._answer)
            await self.sender.sendMessage('/start')
            print('[Info]',chat_id,'has stopped his game.\n[Info] Game ended.')
            self.close()
        try:
           guess = int(msg['text'])
        except ValueError:
            await self.sender.sendMessage('麻煩給我一個數字.')
            return

        # check the guess against the answer ...
        if guess != self._answer:
            # give a descriptive hint
            hint = self._hint(self._answer, guess,self._cmin,self._cmax)
            await self.sender.sendMessage(hint)
        else:
            await self.sender.sendMessage('Boom!')
            await self.sender.sendMessage('遊戲結束，您引爆了炸彈')
            await self.sender.sendMessage('/start')
            print('[Info]',chat_id,'has gotten the bomb and exploded.\n[Info] Game ended.')
            self.close()

    async def on__idle(self, event):
        await self.sender.sendMessage('時間到. 炸彈是 %d' % self._answer)
        await self.sender.sendMessage('/start')
        print('[Info] Game ended due to ',event)
        self.close()
    async def on_close(self,chat_id):
        print('')


TOKEN = '335402407:AAEs0t5a3KyOCQTXS2DdYMlP135bbvr_vnM'

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Player, timeout=20),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
