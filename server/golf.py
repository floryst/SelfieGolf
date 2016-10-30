import os
import sys

from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import collision.collision

import numpy as np

def infiniteBounceGenerator():
    x, z = 0, 0
    while True:

        for x, z in collision.collision.path(x, z, 2, 2):
            yield x, z
        for _ in range(40):
            yield x, z

dt = .02
r = 1.2
weight = .01
unweight = .99

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
        yield self.subscribe(self.onBoop,
                'com.forrestli.selfiegolf.pubsub.boop')

        #game state
        self.stationary = True
        self.about2hit = False
        self.theta = 0
        self.prevDtheta = 0
        self.DDtheta = 0
        self.orientation = 0

        self.x = 0
        self.y = 0


        while True:
            x, z = next(b)
            yield self.publish('com.forrestli.selfiegolf.pubsub.ball', x, .1, z, self.stationary)
            yield sleep(.01)


    def onBoop(self, msg):
        self.log.info("boop")
        self.about2hit = True
    #@inlineCallbacks
    def onAccel(self, x, y, z):
        self.log.info('accel: {x} {y} {z}', x=x, y=y, z=z)
        guess = np.arcsin((x -  self.DDtheta * r)/9.8)
        if not(np.isnan(guess)):
            x = weight * guess + unweight * x
    #@inlineCallbacks
    def onOrient(self, mag, true):
        self.log.info('orient: {mag} {true}', mag=mag, true=true)

    def onGyro(self, x, y, z):
        self.log.info('gyro: {x} {y} {z}', x=x, y=y, z=z)
