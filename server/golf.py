import os
import sys

from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

class Golf(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        yield self.subscribe(self.onAccel,
                'com.forrestli.selfiegolf.pubsub.accel')
        yield self.subscribe(self.onOrient,
                'com.forrestli.selfiegolf.pubsub.orient')
        yield self.subscribe(self.onGyro,
                'com.forrestli.selfiegolf.pubsub.gyro')


    #@inlineCallbacks
    def onAccel(self, x, y, z):
        self.log.info('accel: {x} {y} {z}', x=x, y=y, z=z)

    #@inlineCallbacks
    def onOrient(self, mag, true):
        self.log.info('orient: {mag} {true}', mag=mag, true=true)

    def onGyro(self, x, y, z):
        self.log.info('gyro: {x} {y} {z}', x=x, y=y, z=z)
