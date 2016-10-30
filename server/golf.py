import os
import sys

from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import collision.collision

def infiniteBounceGenerator():
    x, z = 0, 0
    while True:

        for x, z in collision.collision.path(x, z, 2, 2):
            yield x, z
        for _ in range(40):
            yield x, z


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


        b = infiniteBounceGenerator()
        while True:
            x, z = next(b)
            yield self.publish('com.forrestli.selfiegolf.pubsub.ball', x, .1, z, True)
            yield sleep(.01)



    #@inlineCallbacks
    def onAccel(self, x, y, z):
        self.log.info('accel: {x} {y} {z}', x=x, y=y, z=z)

    #@inlineCallbacks
    def onOrient(self, mag, true):
        self.log.info('orient: {mag} {true}', mag=mag, true=true)

    def onGyro(self, x, y, z):
        self.log.info('gyro: {x} {y} {z}', x=x, y=y, z=z)
