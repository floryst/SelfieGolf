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

dt = .04
r = 1.2
weight = .01
unweight = .99

class Golf(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        yield self.subscribe(self.onAccel,
                'com.forrestli.selfiegolf.pubsub.accel')
        #yield self.subscribe(self.onOrient,
        #        'com.forrestli.selfiegolf.pubsub.orient')
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
        self.z = 0

        # TODO don't hardcode this
        self.hole_z = 1.8684875
        self.hole_x = 0.6365875
        self.hole_width2 = 0.0777875/2

    @inlineCallbacks
    def swing(self):
        v = self.prevDtheta * r
        path = collision.collision.path(self.x, self.z, v * np.cos(self.orientation), v * np.sin(self.orientation))
        for x, z in path:
            if z > self.hole_z-self.hole_width2 and z < self.hole_z+self.hole_width2 and \
                    x > self.hole_x-self.hole_width2 and x < self.hole_x+self.hole_width2:
                # TODO have fireworks or something here
                pass
            yield self.publish('com.forrestli.selfiegolf.pubsub.ball', x, .1, z, self.stationary)
            yield sleep(.01)
        self.stationary = True
        self.x = x
        self.z = z
        yield self.publish('com.forrestli.selfiegolf.pubsub.ball', x, .1, z, self.stationary)

    def onBoop(self, msg):
        self.log.info("boop")
        self.about2hit = True

    def onAccel(self, x, y, z):
        self.log.info('accel: {x} {y} {z}', x=x, y=y, z=z)
        guess = np.arcsin((y -  self.DDtheta * r)/9.8)
        if not(np.isnan(guess)):
            self.theta = weight * guess + unweight * self.theta

    def onOrient(self, mag, true):
        o = mag * np.pi / 180
        self.orientation = weight * o + unweight * self.orientation
        self.log.info('orient: {mag} {true}', mag=mag, true=true)

    @inlineCallbacks
    def onGyro(self, x, y, z):
        self.orientation -= z * dt
        self.theta += x/dt
        self.DDtheta = (x - self.prevDtheta)/dt
        self.prevDtheta = x
        yield self.publish('com.forrestli.selfiegolf.pubsub.orientation', self.orientation)
        if(self.theta > 0 and self.about2hit):
            self.stationary = False
            self.about2hit = False
            self.swing()
        self.log.info('gyro: {x} {y} {z}', x=x, y=y, z=z)
