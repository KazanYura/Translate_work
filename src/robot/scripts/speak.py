#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
import random


class Speaker(object):
    country_dict = {"Ukraine": "Kyiv", "Russia": "Moscow", "USA": "Washington"}

    def __init__(self):
        self.soundc = SoundClient()

    def intro(self):
        rospy.sleep(1)
        self.soundc.say('Hello master. I am Geobot. '
                        'If you want to start game,just say hello. ')
        rospy.sleep(10)

    def game(self):
        country = random.choice(self.country_dict.keys())
        self.soundc.say("The capital of " + country + " is?")
        rospy.sleep(10)
        return self.country_dict[country]

    def correct_answer(self):
        self.soundc.say("You are not so bad")

    def wrong_answer(self):
        self.soundc.say("Oh,hell,with who I have to work?")

    def lose(self):
        self.soundc.say("It is over for you!")

    def win(self):
        self.soundc.say("This was unreal but you won!")

    def shutdown(self):
        self.soundc.say("OK. I am going to shutdown!")
        rospy.shutdown()

