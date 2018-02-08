from chatterbot import ChatBot


class botti:
    chatbot = ChatBot(
        'Ron Obvious',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")

    def run():

        # Get a response to an input statement
        loop = "true"
        while loop == "true":
            syote = input("Sano jotain")
            if syote =='lopeta':
                loop = 'false'
            else: print(botti.chatbot.get_response(syote))
botti.run()