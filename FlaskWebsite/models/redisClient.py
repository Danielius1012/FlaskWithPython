import redis

class Client(object):
    """Client for Connecting to the database"""

    def __init__(self):
        # Constructor
        # Create connection to redis database
        self.__r = redis.StrictRedis( 
            host='<DB_NAME>.redis.cache.windows.net', 
            port=6380, 
            ssl=True, 
            charset="utf-8", 
            password='<PASSWORD>',
            decode_responses=True
        )
        self.__badwords = ['TITLE']

    def saveQuestion(self, title, question, answer):
        '''Saves a question in the database'''
        self.__r.set(title + ':question', question)
        self.__r.set(title + ':answer', answer)

    def getTitle(self):
        ''' get the current Title'''
        if(self.__r.exists('TITLE')):
            return self.__r.get('TITLE')
        else:
            title = self.getRandomTitle().split(':')[0]
            self.__r.set('TITLE', self.getRandomTitle())
            return title

    def resetTitle(self):
        '''reset title from the database to a random value'''
        self.__r.set('TITLE', self.getRandomTitle().split(':')[0])

    def getQuestion(self, title):
        ''' get a question with a specific title'''
        question = self.__r.get(title + ':question')
        return question

    def getRandomTitle(self):
        ''' gets a random key for a question '''
        title = self.__r.randomkey()
        while(title in self.__badwords):
            title = self.__r.randomkey()
        return title
        
    def getAnswer(self, title):
        '''Get an answer of a question based on the title'''
        answer = self.__r.get(title + ':answer')
        return answer

    def cleanDatabase(self):
        '''cleans the database '''
        self.__r.hgetall()