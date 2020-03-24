import discord
from AlphaVantage.AlphaParser import AlphaParser

class DiscordBot:
    def __init__(self,token,alpha, alpaca):
        client = discord.Client()
        print('bot ready to go')
        self.alpha = alpha
        self.alpaca = alpaca
        self.wlist = None
        self.userSettings = {}

        @client.event
        async def on_ready():
            print(f'{client.user} is a very bad bot')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            print(message.content)
            msg = ''
            input = message.content.split()
            if not isinstance(message.channel,discord.DMChannel):
            # messages in server
                print("message in guild!")
                if '672484881208442894' in message.content:
                    # bot is mentioned
                    print("I have been summoned")
                    msg += self.respondMention()
            else:
                # messages in dm
                # this is where we parse user messages
                if 'help' in input:
                    msg = self.help()
                elif 'data' in input:
                    # for now we will just return SMA
                    msg = self.getdata()
                elif 'watchlist' in input:
                    if 'create' in input:
                        slist = ' '.join(input[input.index('create')+1:])  #joins string in list
                        print('creating watchlist for ', slist)
                        msg = self.createWatchlist(slist)
                    elif 'view' in input:
                        newname = ' '.join(input[input.index('view')+1:])
                        if newname == 'all':
                            msg = self.viewAllWatchlists()
                        else:
                            msg = self.viewWatchlist(newname)
                        # msg = self.viewWatchlist()    
                    elif 'delete' in input:
                        dname = ' '.join(input[input.index('delete')+1:])
                        msg = self.deleteWatchlist(dname)
                #add 1 symbol to watchlist
                elif 'add' in input:
                    watchlistid = input[input.index('add')+1]
                    print("watchlist: " + watchlistid)
                    symbol = ' '.join(input[input.index(watchlistid)+1:])
                    print("symbol: " + symbol)
                    msg = self.addSymbol(watchlistid, symbol)
                elif 'remove' in input:
                    watchlistid = input[input.index('remove')+1]
                    print("watchlist: " + watchlistid)
                    symbol = ' '.join(input[input.index(watchlistid)+1:])
                    print("symbol: " + symbol)
                    msg = self.removeSymbol(watchlistid, symbol)

                else:
                    msg = 'how can I help? (type \'help\' to see options)'
            if msg:
                await message.channel.send(msg)

        client.run(token)

    def help(self):
        helpmenu = 'options:\n'
        helpmenu += '\t-watchlist:\n'
        helpmenu += '\t\t-create [inputs: \'symbol_0\',\'symbol_1\', ..]\n'
        helpmenu += '\t\t example: watchlist create MSFT TSLA\n'
        helpmenu += '\t\t-view\n'
        helpmenu += '\t\t\t view all\n'
        helpmenu += '\t\t\t returns the name of all watchlists\n'
        helpmenu += '\t\t\t [watchlist name]\n'
        helpmenu += '\t\t\t returns specified watchlist\n'
        helpmenu += '\t\t-delete\n'
        helpmenu += '\t\t example: watchlist delete [watchlistname]'
        return helpmenu

    def respondMention(self):
        return 'type --help in my dm for more info!\n'

    def getdata(self):
        d = self.alpha.getSMAvalue()
        d = d[list(d.keys())[1]]
        d = d[list(d.keys())[0]]
        return d

    def createWatchlist(self, watchlist):
        try:
            self.alpaca.createWatchlist(watchlist)
        except:
            print('something messed up')
        return "watchlist successfully created!"
    
    def deleteWatchlist(self,watchlist):
        self.alpaca.deleteWatchlist(watchlist)
        return "success!"

    def viewAllWatchlists(self):
        nameslist = self.alpaca.getAllWatchlists()
        return ', '.join(nameslist)

    def viewWatchlist(self,name):
        if name not in self.alpaca.watchlists.keys():
            return 'please provide a valid watchlist name!'
        wlist = self.alpaca.viewWatchlist(name)
        returnstring = ''
        for k,v in wlist.items():
            if k == 'id' or k == 'account_id':
                continue
            if k == 'assets':
                returnstring += k + ':\n'
                for item in v:
                    for k,v in item.items():
                        if k == 'id':
                            continue
                        returnstring += '\t' + k + ': ' + str(v) + '\n'
                    returnstring += '\t----------------------\n'
            returnstring += k + ': ' + str(v) + '\n'

        return returnstring

    def addSymbol(self,name,ticker):
        try: 
            self.alpaca.addSymbol(name, ticker)
        except:
            print("addsymbol failed")
        return "supposedly added symbol " + ticker + " to " + name

    def removeSymbol(self,name,ticker):
        try: 
            self.alpaca.removeSymbol(name, ticker)
        except:
            print("removesymbol failed")
        return "supposedly removed symbol " + ticker + " from " + name