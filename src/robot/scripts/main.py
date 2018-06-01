#!/usr/bin/env python
import speak
import recognizer
import rospy


def main():
    rospy.init_node("main")
    speaker = speak.Speaker()
    speaker.intro()
    rec = recognizer.Recognizer()
    res = rec.start_recognizer()
    if res[0] == "HELLO ":
        num_of_right_answers = 0
        num_of_wrong_answers = 0
        while (num_of_right_answers < 15) or (num_of_wrong_answers < 3):
            answer = speaker.game()
            rec = recognizer.Recognizer()
            res = rec.start_recognizer()
            if answer.lower() == res[:-1].lower:
                speaker.correct_answer()
                num_of_right_answers += 1
            else:
                speaker.wrong_answer()
                num_of_wrong_answers += 1
    else:
        speaker.shutdown()
main()
