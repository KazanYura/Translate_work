#!/usr/bin/env python

import rospy

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio
from std_msgs.msg import String
from std_srvs.srv import *
import os
import commands


class Recognizer(object):

    def __init__(self):
        self.got_answer = False
        # initialize ROS
        rospy.on_shutdown(self.shutdown)
        # you may need to change publisher destination depending on what you run
        self.pub_ = rospy.Publisher('~output', String, queue_size=1)
        self.lm = "/home/yura/ros_project_dependencies_ws/src/robot/cmusphinx-en-us-8khz-5.2"
        self.lexicon = "/home/yura/ros_project_dependencies_ws/src/robot/vocab/voice_cmd.dic"
        self.kw_list = "/home/yura/ros_project_dependencies_ws/src/robot/vocab/voice_cmd.kwlist"

    def start_recognizer(self):
        self.got_answer = False
        # initialize pocketsphinx. As mentioned in python wrapper
        rospy.loginfo("Initializing pocketsphinx")
        config = Decoder.default_config()
        rospy.loginfo("Done initializing pocketsphinx")

        # Hidden Markov model: The model which has been used
        config.set_string('-hmm', self.lm)
        # Pronunciation dictionary used
        config.set_string('-dict', self.lexicon)
        # Keyword list file for keyword searching
        config.set_string('-kws', self.kw_list)

        rospy.loginfo("Opening the audio channel")
        stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=16000,
                                        input=True,
                                        frames_per_buffer=1024)
        stream.start_stream()
        rospy.loginfo("Done opening the audio channel")

        self.decoder = Decoder(config)
        self.decoder.start_utt()
        rospy.loginfo("Done starting the decoder")
        # Main loop
        while not self.got_answer:
            # taken as is from python wrapper
            buf = stream.read(1024)
            if buf:
                self.decoder.process_raw(buf, False, False)
            else:
                break
        return self.publish_result()

    def publish_result(self):
        """
        Publish the words
        """
        if self.decoder.hyp() is not None:
            print([seg.word
                   for seg in self.decoder.seg()])
            seg.word = seg.word.lower()
            self.decoder.end_utt()
            self.decoder.start_utt()
            rospy.loginfo(seg.word)
            self.got_answer = True
        return seg.word

    def shutdown(self):
        """
        command executed after Ctrl+C is pressed
        """
        rospy.loginfo("Stopping PocketSphinx")
