from chatterbot import ChatBot

class botti:
    chatbot = ChatBot(
        'Ron Obvious',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")

    def Chatter(syote):

        return botti.chatbot.get_response(syote)
