#!/usr/bin/python3

__author__ = "blueShard"
__license__ = "GPL-3.0"
__version__ = "0.1.0"

from aion_core import logging as alog
from aion_core import utils as atils
from aion_core import variable as avar

from aion_core.config import Aion
from aion_core.language import language_directory
from aion_core.skill import skills_file, skills_path
from aion_core.plugin import get_all_run_after_plugins, get_all_run_before_plugins
from aion_core.utils import aion_path, aion_data_path, is_dict_in_dict

import os, signal, sys, traceback
import snowboydecoder
import speech_recognition as sr

from colorama import Fore
from inspect import currentframe, getframeinfo
from multiprocessing import Process
from threading import Thread

console_logger = alog.LogConsole()
logger = alog.LogAll(aion_data_path + "/logs/aion.log",
                     critical_fname=aion_data_path + "/logs/critical.log",
                     debug_fname=aion_data_path + "/logs/debug.log",
                     error_fname=aion_data_path + "/logs/error.log",
                     info_fname=aion_data_path + "/logs/info.log",
                     warning_fname=aion_data_path + "/logs/warning.log")


variables = avar.Variable()
variables.inititalize_variables()
variables.set_value(avar.IS_AION_RUNNING, str(True))


interrupted = False

language = Aion().get_language()
listening_mode = "auto"
stt_engine = Aion().get_stt_engine()


def get_main_file_from_skill(skill):
    for skills_list in atils.BaseXMLReader(skills_file).get_infos("main_file").values():
        for skill_name in skills_list:
            if skill_name["parent"]["tag"] == skill:
                return "".join(skill_name["text"].split(".")[:-1])


phrase_dict = {}

activate_phrase_file = language_directory + "/" + Aion().get_language() + ".acph"
if os.path.isfile(activate_phrase_file) is False:
    logger.warning("Couldn't find an activate phrase (.acph) file with your language locale (" + Aion().get_language() + ") in " + language_directory + ". Using the default activate phrase file (en_US)", getframeinfo(currentframe()).lineno - 1)
    activate_phrase_file = language_directory + "/en_US.acph"
for value_list in atils.BaseXMLReader(activate_phrase_file).get_infos("<all>").values():
    for phrase_infos in value_list:
        try:
            if phrase_infos["parent"]["tag"] == "activate_phrases":
                and_phrase_list = []
                if "__and__" in phrase_infos["tag"]:
                    for phrase in phrase_infos["tag"].split("__and__"):
                        and_phrase_list.append(phrase.replace("_", " "))
                    phrase_dict["__and__".join(and_phrase_list)] = [get_main_file_from_skill(phrase_infos["attrib"]["skill"]), phrase_infos["attrib"]["method"]]
                else:
                    phrase_dict[phrase_infos["tag"].replace("_", " ")] = [get_main_file_from_skill(phrase_infos["attrib"]["skill"]), phrase_infos["attrib"]["method"]]
        except KeyError:
            pass


run_after_plugins = get_all_run_after_plugins()
run_before_plugins = get_all_run_before_plugins()


def getset_stt_engine():
    global stt_engine
    if listening_mode == "auto":
        if atils.is_internet_connected() is True:
            if stt_engine != "google":
                Aion().set_stt_engine("google")
                stt_engine = "google"
                logger.info("Set listening_source in '" + aion_path + "/config.xml' to 'google'", getframeinfo(currentframe()).lineno - 1)
        else:
            if stt_engine != "pocketsphinx":
                Aion().set_stt_engine("pocketsphinx")
                stt_engine = "pocketsphinx"
                logger.info("Set listening_source in '" + aion_path + "/config.xml' to 'pocketsphinx'", getframeinfo(currentframe()).lineno - 1)
    else:
        stt_engine = Aion().get_stt_engine()
    return stt_engine


#def start_pysb():
#    from aion_core.usb import USB
#    for action in USB().listen():
#        pass


def execute(main_file, method, speech_input, acph):
    if skills_path in sys.path:
        pass
    else:
        sys.path.insert(0, skills_path)
    exec("skill = __import__(main_file)." + method + "('" + acph + "', '" + speech_input + "', " + str(run_after_plugins) + ", " + str(run_before_plugins) + ")")
    exec("skill.run_before()", {"skill": locals()["skill"]})
    exec("skill.main()", {"skill": locals()["skill"]})
    exec("skill.run_after()", {"skill": locals()["skill"]})


def main(fname):
    global output_pid

    found = False
    and_found = True

    print("Converting...")
    global speech_input
    speech = sr.Recognizer()

    with sr.AudioFile(fname) as source:
        audio = speech.record(source)

    try:
        if getset_stt_engine() == "google":
            speech_input = speech.recognize_google(audio_data=audio, language=language)
        elif getset_stt_engine() == "pocketsphinx":
            speech_input = speech.recognize_sphinx(audio_data=audio, language=language)
        speech_input_lower = str(speech_input.lower())
        logger.info("Speech_input: " + str(speech_input), getframeinfo(currentframe()).lineno - 2)

        os.remove(fname)

        if speech_input_lower.startswith("system call "):  # 'system call ' <- copied from SAO Alicization? maybe...
            speech_input_lower = speech_input_lower.replace("system call ", "").strip()
            if speech_input_lower == "shutdown":
                if atils.is_root():
                    os.system("sudo shutdown -h 0")
                else:
                    logger.error("No root privileges, couldn't shutdown system", getframeinfo(currentframe()).lineno - 1)
            elif speech_input_lower == "stop":
                variables.close()
                try:
                    os.kill(output_pid, signal.CTRL_C_EVENT)
                except ProcessLookupError:
                    pass
                try:
                    os.kill(os.getpid(), signal.CTRL_C_EVENT)
                except ProcessLookupError:
                    pass
                sys.exit(1)
            found = True

        if speech_input_lower.endswith("stop"):
            try:
                output_pid = output_pid + Aion().get_pid_manipulation_number()  # the pid is from 'aion_task.pid' given pid plus 5 and i don't know why
                os.kill(output_pid, signal.SIGKILL)
                logger.info("Killed an aion skill with the PID " + str(output_pid), getframeinfo(currentframe()).lineno - 1)
                output_pid = None
            except (ProcessLookupError, TypeError):
                logger.error("No process with the PID " + str(output_pid), getframeinfo(currentframe()).lineno - 1)
            except NameError:
                logger.error("No PID was given", getframeinfo(currentframe()).lineno - 1)
            found = True

        for activate_phrase, value in phrase_dict.items():
            activate_phrase_lower = activate_phrase.lower()
            if "__and__" in activate_phrase_lower:
                for and_phrase in activate_phrase.split("__and__"):
                    if and_phrase.lower() not in speech_input_lower:
                        and_found = False
                        break
                if and_found is True:
                    aion_task = Process(target=execute, args=(value[0], value[1], speech_input, activate_phrase,))
                    aion_task.daemon = False
                    aion_task.start()
                    output_pid = aion_task.pid
                    found = True
                    break
            elif activate_phrase_lower in speech_input_lower:
                aion_task = Process(target=execute, args=(value[0], value[1], speech_input, activate_phrase,))
                aion_task.daemon = False
                aion_task.start()
                output_pid = aion_task.pid
                break

        if found is False:
            logger.warning("Couldn't find skill", getframeinfo(currentframe()).lineno - 1)
        else:
            try:
                logger.info("Output_pid: " + str(output_pid + Aion().get_pid_manipulation_number()), getframeinfo(currentframe()).lineno - 1)
            except NameError:
                logger.info("Output_pid: None", getframeinfo(currentframe()).lineno - 1)

    except KeyboardInterrupt:
        variables.close()
        try:
            os.kill(output_pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            os.kill(os.getpid(), signal.SIGKILL)
        except ProcessLookupError:
            pass
        sys.exit(1)
    except sr.UnknownValueError:
        print("I couldn't understand you")
        logger.error("Couldn't understand the spoken word(s)", getframeinfo(currentframe()).lineno - 2)
        pass
    except BaseException:
        traceback.print_exc()
        exception_list = []
        for exception in traceback.format_exc().split("\n"):
            exception_list.append(exception.strip())
        logger.error(" |-| ".join(exception_list), getframeinfo(currentframe()).lineno - 5)
        pass


def detected_callback():
    # wake_up.terminate()
    print('recording audio...', end='', flush=True)


def signal_handler(sig, frame):
    variables.close()
    try:
        os.kill(output_pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        os.kill(os.getpid(), signal.SIGKILL)
    except ProcessLookupError:
        pass
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def snowboy():
    hotword_file = Aion().get_hotword_file()
    logger.info("Set the hotword file", getframeinfo(currentframe()).lineno - 1)

    try:
        global main_pid
        main_pid = os.getpid()
        print("Main PID: " + str(main_pid))
        wake_up = snowboydecoder.HotwordDetector(hotword_file, sensitivity=0.5)
        logger.info("Configured the hotword detector", getframeinfo(currentframe()).lineno - 1)
        logger.info("Starting hotword detection...", getframeinfo(currentframe()).lineno - 1)
        wake_up.start(detected_callback=detected_callback,
                      audio_recorder_callback=main,
                      recording_timeout=50,
                      sleep_time=0.01)

        wake_up.terminate()
    except KeyboardInterrupt:
        variables.close()
        sys.exit(1)
    except Exception:
        print(Fore.CYAN + "Caught error: " + Fore.RED + "\n" + traceback.format_exc() + Fore.RESET)
        error_list = []
        for error in traceback.format_exc().split("\n"):
            error_list.append(error.strip())
        logger.error("Caught error: " + " |-| ".join(error_list), getframeinfo(currentframe()).lineno - 5)
        pass


if __name__ == '__main__':
    #Thread(target=start_pysb).start()
    #logger.info("executed 'pysb.main'", getframeinfo(currentframe()).lineno - 1)

    snowboy()
