#!/usr/bin/env python3
""" Interface for the Alpaca LLM as a Python Module """

import os
import sys
import time
import nltk

from gdown import download as gdownload

from llm import resources_dir, examples_dir
from llm.helper import CHAT_FILE, BulletType
from llm.prompts import EXPERIENCES_PURPOSE, PROJECTS_NAME_PURPOSE, \
    PROJECTS_BULLET_PURPOSE


class Alpaca:
    """ Class for the Alpaca LLM """

    def __init__(
        self,
        purpose: str,
        example_path: str,
        llm_path: str = CHAT_FILE,
        model_path: str = "ggml-alpaca-7b-q4.bin"
    ):
        """
        Initialize the LLM
        - `purpose`: The purpose given to the LLM by the user
        - `example_path`: Path to the `examples.txt` file
        - `llm_path`: Path to the `chat` executable
        - `model_path`: Path to the model file

        examples.txt should be a file containing examples of inputs and outputs
        for the LLM.
        """
        self.purpose = purpose
        self.llm_path = os.path.join(resources_dir, llm_path)
        self.model_path = os.path.join(resources_dir, model_path)
        if not os.path.exists(self.llm_path):
            raise FileNotFoundError(f"Could not find '{self.llm_path}'")
        example_path = os.path.join(examples_dir, example_path)
        with open(example_path, "r", encoding="utf-8") as example_file:
            self.examples = example_file.read().strip()

    def generate_prompt(self, input_str: str) -> str:
        """ Generate a prompt for the LLM from the given input """
        return f"# Purpose:\n\n{self.purpose}\n\n" \
               f"# Example Problems:\n\n{self.examples}\n\n" \
               f"# Real Problem:\n\nInput:\n{input_str}\nOutput:"

    def prompt(self, prompt: str, temp=1, n_threads=None) -> str:
        """ Prompt the LLM with a string and return the response """
        if n_threads is None:
            n_threads = os.cpu_count() - 1
        with open("prompt.txt", "w", encoding="utf-8") as prompt_file:
            prompt_file.write(prompt)
        return os.popen(
            f'{self.llm_path} -f ./prompt.txt '
            f'--temp {temp} --threads {n_threads} --seed '
            f'{round(time.time())} --model {self.model_path} 2>llm_log.txt'
        ).read().strip()


def generate_experience(
    company: str,
    position: str,
    student_year: str,
    retries: int = 3,
    debug: bool = False
) -> list:
    """
    Generate experience bullet points for a resume
    - `company`: Name of the company
    - `position`: Name of the position
    - `student_year`: Student's year at Cal Poly (e.g. "1", "2", etc.)
    - `retries`: Number of times to retry if the LLM fails to generate a
        valid response

    Returns a list of bullet points
    """
    purpose = EXPERIENCES_PURPOSE
    llm = Alpaca(purpose, "exp_examples.txt")
    input_str = f'```\n' \
                f'{{\n' \
                f'    "company": "{company}",\n' \
                f'    "position": "{position}",\n' \
                f'    "studentYear": "{student_year}"\n' \
                f'}}\n' \
                f'```'
    result = []

    def validator(lst: list):
        correct_len = len(lst) >= 2
        correct_pos = len([
            nltk.pos_tag(nltk.word_tokenize(bp))[0][1].upper()
            in ["VBD", "VBN"] for bp in lst[:-1]
        ])
        return correct_len and correct_pos >= len(lst) / 2

    prompt = llm.generate_prompt(input_str)
    while not validator(result) and retries > 0:
        result = nltk.sent_tokenize(llm.prompt(prompt))
        if debug:
            print("\nFailure, retrying...", result, sep="\n")
        result = [
            bp for bp in result
            if len(bp) > 0 and bp.strip()[-1] in [".", "?", "!"]
        ]
        retries -= 1
    return result


def generate_project(
    student_year: str,
    course_taken: str,
    technologies: list,
    retries: int = 3,
    debug: bool = False
) -> tuple:
    """
    Generate project name and bullet points for a resume
    - `student_year`: Student's year at Cal Poly (e.g. "1", "2", etc.)
    - `course_taken`: Course taken to enspire the project
    - `technologies`: List of technologies used in the project
    - `retries`: Number of times to retry if the LLM fails to generate a
        valid response

    Returns a tuple containing containing project name followed by list of bullet points
    """
    name_purpose = PROJECTS_NAME_PURPOSE
    bullet_purpose = PROJECTS_BULLET_PURPOSE
    name_llm = Alpaca(name_purpose, "prj_name_examples.txt")
    bullet_llm = Alpaca(bullet_purpose, "prj_bullet_examples.txt")
    input_str = f'```\n' \
                f'{{\n' \
                f'    "studentYear": "{student_year}"\n' \
                f'    "courseTaken": "{course_taken}"\n' \
                f'    "technologies": {"[" + ", ".join(technologies) + "]"}\n' \
                f'}}\n' \
                f'```'
    name = ""
    prompt = name_llm.generate_prompt(input_str)
    while len(name.strip()) == 0:
        name = name_llm.prompt(prompt)
    ts = [('"' + t + '"') for t in technologies]
    input_str = f'```\n' \
                f'{{\n' \
                f'    "studentYear": "{student_year}",\n' \
                f'    "courseTaken": "{course_taken}",\n' \
                f'    "projectName": "{name}"\n' \
                f'    "technologies": {"[" + ", ".join(ts) + "]"}\n' \
                f'}}\n' \
                f'```'
    result = []

    def validator(lst: list):
        correct_len = len(lst) >= 1
        correct_pos = len([
            nltk.pos_tag(nltk.word_tokenize(bp))[0][1].upper()
            in ["VBD", "VBN"] for bp in lst[:-1]
        ])
        return correct_len and correct_pos >= len(lst) / 2

    prompt = bullet_llm.generate_prompt(input_str)
    while not validator(result) and retries > 0:
        result = nltk.sent_tokenize(bullet_llm.prompt(prompt))
        if debug:
            print("\nFailure, retrying...", result, sep="\n")
        result = [
            bp for bp in result
            if len(bp) > 0 and bp.strip()[-1] in [".", "?", "!"]
        ]
        retries -= 1
    return name, result


def test():
    fn = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "prj":
            fn = BulletType.PROJECT
        elif sys.argv[1] == "exp":
            fn = BulletType.EXPERIENCE
        else:
            print("Usage: python3 alpaca.py (exp | prj)")
            sys.exit(1)
    else:
        print("Usage: python3 alpaca.py (exp | prj)")
        sys.exit(1)
    while True:
        try:
            if fn == BulletType.EXPERIENCE:
                company = input("Company:  ")
                position = input("Position: ")
                year = input("Year:     ")
                print("[Generating bullet points...]", flush=True, end="")
                bps = [
                    "\n- " + bp for bp in generate_experience(company, position, year)]
                print("\n" + "".join(bps), end="\n\n")
            else:
                year = input("Year:   ")
                course = input("Course: ")
                tech = input("Tech:   ").split(", ")
                print("[Generating bullet points...]", flush=True, end="")
                prj = generate_project(year, course, tech)
                print(f"\n{prj[0]} - {', '.join(tech)}", flush=True)
                bps = ["\n- " + bp for bp in prj[1]]
                print("\n" + "".join(bps), end="\n\n")
        except KeyboardInterrupt:
            print()
            break


def download():
    """ Downloads the LLM's weights and NLTK dependencies """
    download_path = os.path.join(resources_dir, "ggml-alpaca-7b-q4.bin")
    g_drive_id = "1HMBBW5lwmhJCn9x0NGrDZdMo5U8j_eiy"
    print("[ Downloading model weights ]\n")
    if os.path.exists(download_path):
        print("Model already downloaded!")
    else:
        try:
            gdownload(id=g_drive_id, output=download_path, resume=True)
        except KeyboardInterrupt:
            print(flush=True)
            print("Download paused. Please run again to resume.")
            sys.exit(1)
    if not os.path.exists(download_path):
        print("Model download failed!")
        sys.exit(1)
    print("\n[ Updating NLTK dependencies ]\n")
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    print("\n[ Done ]")


if __name__ == "__main__":
    test()
