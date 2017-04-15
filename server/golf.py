import os
import sys
import subprocess

from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import collision.collision

import numpy as np

ids = set()


# (sighs)
## LEVEL DATA
# holes[i-1] is the (x,z) of ith hole
hole_halfwidth = 0.0777875/2
holes = [
    (0.6365875, 1.8684875),
    (-1.662, -6.1563),
    (-3.6925, 2.5416)
]

# start[i-1] is the (x,z) of ith course starting pos
start = [
    (0, 0),
    (0.865, -5.367),
    (-6.1293, 2.364)
]
## END LEVELDATA

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
        yield self.register(self.newGame, 
	        'com.forrestli.selfiegolf.pubsub.newGame')
	yield self.register(self.endGame,
	        'com.forrestli.selfiegolf.pubsub.endGame')
	self.games = {}

    def newGame(self, new_id):
        if new_id not in self.games:
	    self.games[new_id] = GolfGame(new_id, self)
	else:
	    return "no sorry someone else has that"
    
    def endGame(self, dead_id):
        if dead_id in self.games:
	    del self.games[dead_id]
	else:
	    return "That is not dead which can eternal lie, and with strange aeons even death may die"

    def onBoop(self, my_id):
        if my_id in self.games:
            self.games[my_id].onBoop()

    def onAccel(self, x, y, z, my_id):
        if my_id in self.games:
            self.games[my_id].onAccel(x, y, z)

    def onOrient(self, mag, true, my_id):
        if my_id in self.games:
            self.games[my_id].onOrient(mag, true)

    def onGyro(self, x, y, zi, my_id):
        if my_id in self.games:
            self.games[my_id].onGyro(x, y, zi)


class GolfGame:

    
    def __init__(self, my_id, session):
        self.my_id = my_id
	self.session = session
        #game state
        self.stationary = True
        self.about2hit = False
        self.theta = 0
        self.prevDtheta = 0
        self.DDtheta = 0
        self.orientation = 0
        self.disable_hits = False
        self.cur_level = 0
        self.strokes = 0
        self.hole_x, self.hole_z = holes[self.cur_level]
        self.x, self.z = start[self.cur_level]

    @inlineCallbacks
    def swing(self):
        self.strokes += 1
        yield self.session.publish('com.forrestli.selfiegolf.pubsub.strokes', self.strokes, self.my_id)

        v = self.prevDtheta * r
        path = collision.collision.path(self.x, self.z, v * np.cos(self.orientation), v * np.sin(self.orientation))
        for x, z in path:
            if z > self.hole_z-hole_halfwidth  and z < self.hole_z+hole_halfwidth and \
                    x > self.hole_x-hole_halfwidth and x < self.hole_x+hole_halfwidth:
                #subprocess.Popen(['play', '-q', '../golf_hole.py'])
                yield self.session.publish('com.forrestli.selfiegolf.hide_ball', self.my_id)
                # don't continue to perform swing
                self.disable_hits = True

                # sleep 1 sec for user experience
                yield sleep(1)

                # set game state
                self.cur_level = (self.cur_level + 1) % len(holes)
                self.hole_x, self.hole_z = holes[self.cur_level]
                self.x, self.z = start[self.cur_level]
                self.stationary = True
                yield self.session.publish('com.forrestli.selfiegolf.pubsub.ball', self.x, .1, self.z, self.stationary, self.my_id)

                self.strokes = 0
                yield self.session.publish('com.forrestli.selfiegolf.pubsub.strokes', self.strokes, self.my_id)

                # stupid "mutex"
                self.disable_hits = False

                yield self.session.publish('com.forrestli.selfiegolf.show_ball', self.my_id)

                return
            yield self.session.publish('com.forrestli.selfiegolf.pubsub.ball', x, .1, z, self.stationary, self.my_id)
            yield sleep(.01)
        self.stationary = True
        self.x = x
        self.z = z
        yield self.session.publish('com.forrestli.selfiegolf.pubsub.ball', x, .1, z, self.stationary, self.my_id)

    def onBoop(self):
        if not self.disable_hits:
            self.log.info("boop")
            self.about2hit = True

    def onAccel(self, x, y, z):
        #self.log.info('accel: {x} {y} {z}', x=x, y=y, z=z)
        guess = np.arcsin((y -  self.DDtheta * r)/9.8)
        if not(np.isnan(guess)):
            self.theta = weight * guess + unweight * self.theta

    def onOrient(self, mag, true):
        o = mag * np.pi / 180
        self.orientation = weight * o + unweight * self.orientation
        #self.log.info('orient: {mag} {true}', mag=mag, true=true)

    @inlineCallbacks
    def onGyro(self, x, y, z):
        self.orientation -= .3 * z * dt
        self.theta += x/dt
        self.DDtheta = (x - self.prevDtheta)/dt
        self.prevDtheta = x
        yield self.session.publish('com.forrestli.selfiegolf.pubsub.orientation', self.orientation, self.my_id)
        if(self.theta > 0 and self.about2hit):
            self.stationary = False
            self.about2hit = False
            self.swing()
        #self.log.info('gyro: {x} {y} {z}', x=x, y=y, z=z)
