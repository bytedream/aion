#!/usr/bin/python3

from glob import glob
from sys import path

path.insert(0, glob("/usr/local/aion-*/aion_core")[0])

from aion_core import config as aconf
from aion_core import language as alang

from aion_core.skill import Skill


class CpuRamUsage(Skill):
    """
    skill class to get the cpu and ram usage
    """

    def main(self):
        from psutil import cpu_percent, virtual_memory
        from statistics import mean
        from time import sleep

        testing_time = 10
        print_process = False

        cpu_list = []
        ram_list = []

        while True:
            cpu = cpu_percent()
            cpu_list.append(cpu)
            ram = virtual_memory()[2]
            ram_list.append(ram)
            if print_process is True:
                print("CPU: " + str(cpu) + "%")
                print("RAM: " + str(ram) + "%")
            sleep(1)

            if 0.0 in cpu_list:
                cpu_list.remove(0.0)
            if len(cpu_list) == testing_time and len(ram_list) == testing_time:
                cpu = mean(cpu_list)
                ram = mean(ram_list)
                break
            elif len(cpu_list) == testing_time - 1 and len(ram_list) == testing_time:
                cpu = cpu_percent()
                cpu_list.append(cpu)
                cpu = mean(cpu_list)
                ram = mean(ram_list)
                break

        self.speech_output(alang.start("skills", "cpu_ram_usage", {"cpu_usage": round(cpu, 2), "ram_usage": round(ram, 2)}))


class CpuUsage(Skill):
    """
    skill class to get the cpu usage
    """

    def main(self):
        from statistics import mean
        from psutil import cpu_percent
        from time import sleep

        testing_time = 10
        print_process = False

        cpu_list = []

        while True:
            cpu = cpu_percent()
            cpu_list.append(cpu)
            if print_process is True:
                print("CPU: " + str(cpu) + "%")
            sleep(1)

            if 0.0 in cpu_list:
                cpu_list.remove(0.0)
            if len(cpu_list) == testing_time:
                cpu = (mean(cpu_list))
                break

        self.speech_output(alang.start("skills", "cpu_usage", {"cpu_usage": round(cpu, 2)}))


class CurrentTime(Skill):
    """
    skill class to get the current time
    """

    def main(self):
        from datetime import datetime

        current_time = datetime.now()
        time_dict = {"hour": current_time.hour, "minute": current_time.minute, "second": current_time.second, "microsecond": current_time.microsecond}
        if aconf.Aion().get_time_format() == "12":
            if time_dict["minute"] == 0:
                if time_dict["hour"] < 13:
                    self.speech_output(alang.start("skills", "current_time_full_am", time_dict))
                else:
                    time_dict["hour"] = time_dict["hour"] - 12
                    self.speech_output(alang.start("skills", "current_time_full_pm", time_dict))
            elif time_dict["minute"] == 30:
                if time_dict["hour"] < 13:
                    self.speech_output(alang.start("skills", "current_time_half_am",  time_dict))
                else:
                    time_dict["hour"] = time_dict["hour"] - 12
                    self.speech_output(alang.start("skills", "current_time_half_pm", time_dict))
            elif 0 < time_dict["minute"] < 30:
                if time_dict["hour"] < 13:
                    self.speech_output(alang.start("skills", "current_time_past_am", time_dict))
                else:
                    time_dict["hour"] = time_dict["hour"] - 12
                    self.speech_output(alang.start("skills", "current_time_past_pm", time_dict))
            elif time_dict["minute"] > 30:
                time_dict["minute"] = 60 - time_dict["minute"]
                if time_dict["hour"] < 13:
                    self.speech_output(alang.start("skills", "current_time_to_am", time_dict))
                else:
                    time_dict["hour"] = time_dict["hour"] - 12
                    self.speech_output(alang.start("skills", "current_time_to_pm", time_dict))
            else:
                self.speech_output(alang.start("skills", "current_time_etc", time_dict))
        else:
            if time_dict["minute"] == 0:
                self.speech_output(alang.start("skills", "current_time_full", time_dict))
            elif time_dict["minute"] == 30:
                self.speech_output(alang.start("skills", "current_time_half", time_dict))
            else:
                self.speech_output(alang.start("skills", "current_time_etc", time_dict))


class IpAddress(Skill):
    """
    skill class to get the ip address
    """

    def main(self):
        from socket import gethostname, gethostbyname

        self.speech_output(alang.start("skills", "ip_address", {"ip_address": gethostbyname(gethostname() + ".local")}))


class Play(Skill):
    """
    skill class to play a audio from youtube
    """

    def main(self):
        from aion_core.utils import get_full_directory_data, vlc

        file_or_search_element = self.speech_input.lower().replace(self.activate_phrase.lower(), "")
        for file in get_full_directory_data(file_or_search_element):
            if file_or_search_element in file:
                return vlc(file_or_search_element)
        import urllib.parse, urllib.request
        from pafy import new
        from re import findall
        search_query = urllib.parse.urlencode({"search_query": file_or_search_element})
        for i in range(10):  # sometimes the video url's cannot be found
            try:
                html_content = urllib.request.urlopen("https://www.youtube.com/results?" + search_query)
                search_results = findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                vlc(new(str("https://www.youtube.com/watch?v=" + search_results[0])).getbestaudio().url)
                break
                # i do it this way, because vlc sometimes don't extract the 'only audio url' from the youtube url
            except IndexError:
                pass

    def run_after(self):
        for plugin in self.run_after_plugins:
            self.start_run_after_plugin(plugin["name"])


class RamUsage(Skill):
    """
    skill class to get ram usage
    """

    def main(self):
        from statistics import mean
        from psutil import virtual_memory
        from time import sleep

        testing_time = 10
        print_process = False

        ram_list = []

        while True:
            ram = virtual_memory()[2]
            ram_list.append(ram)
            if print_process is True:
                print("RAM: " + str(ram) + "%")
            sleep(1)

            if len(ram_list) == testing_time:
                ram = mean(ram_list)
                break

        self.speech_output(alang.start("skills", "ram_usage", {"ram_usage": round(ram, 2)}))


class Shutdown(Skill):
    """
    skill class to shutdown the system
    """

    def main(self):
        from os import system

        system("sudo shutdown -h 0")


class Wikipedia(Skill):
    """
    skill class to search an article on wikipedia
    """

    def main(self):
        from aion_core.utils import remove_brackets, remove_space, remove_string_sequence
        from wikipediaapi import Wikipedia

        splitted_acph = self.activate_phrase.split("__and__")
        searched_article = remove_string_sequence(self.speech_input, splitted_acph[0], splitted_acph[-1])
        wiki = Wikipedia(aconf.Aion().get_language().split("_")[0])
        article = wiki.page(searched_article)

        if article.exists():
            article_text = remove_brackets(article.summary)
            article_text = remove_space(article_text)
            self.speech_output(alang.start("skills", "wikipedia", {"article_text": article_text}))
        else:
            self.speech_output(alang.start("skills", "wikipedia_article_not_found", {"article_name": searched_article}))
