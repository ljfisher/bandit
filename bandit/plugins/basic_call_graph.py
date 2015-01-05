import ast
import yaml
import logging
from pprint import pprint

import bandit
import bandit.core.utils as b_utils
from bandit.core.test_selector import *


logger = logging.getLogger()


class CallTracker():
    def __init__(self):
        self.calls = {}
        self.current_caller = None

    def enter_function(self, context):
        self.current_caller = context.call_function_name_qual
        logger.debug('entered {}()'.format(current_caller))
    
    def record_call(self, context):
        pprint(context._context)
        callee_name = context.call_function_name_qual
        caller_name = self.current_caller
        logger.debug('{} called {}'.format(caller_name, callee_name))
    
        if caller_name not in calls:
            self.calls[caller_name] = [callee_name]
        else:
            self.calls[caller_name].append(callee_name)

    def save(self, path):
        with open(path, 'w') as f:
            yaml.dump(calls, f)


calls = {}
current_caller = None

@checks_functions
def enter_function(context):
    global current_caller
    current_caller = context.call_function_name_qual
    logger.debug('entered {}()'.format(current_caller))

@checks_calls
def record_call(context):
    #pprint(context._context)
    callee_name = context.call_function_name_qual
    caller_name = current_caller
    logger.debug('{} called {}'.format(caller_name, callee_name))

    if caller_name not in calls:
        calls[current_caller] = set([callee_name])
    else:
        calls[current_caller].update([callee_name])

def finish():
    logger.debug('finish function')
    print "RUNNING MY FINISH FUNC"
    with open('/tmp/bandit.dumb_call_graph', 'w') as f:
        yaml.dump(calls, f)
   
