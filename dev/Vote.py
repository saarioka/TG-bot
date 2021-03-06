import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import per_inline_from_id, create_open, pave_event_space

"""
$ python3.5 inline.py <token>
It demonstrates answering inline query and getting chosen inline results.
"""

class Votee(telepot.helper.InlineUserHandler, telepot.helper.AnswererMixin):

    def on_inline_query(self, msg):
        def compute_answer():
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)
            articles = [{'type': 'article','id': 'abc', 'title': query_string, 'message_text': query_string}]
            return articles

        self.answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        from pprint import pprint
        pprint(msg)
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)

