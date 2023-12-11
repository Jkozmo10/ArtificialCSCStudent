#!/usr/bin/env python3

""" Interface for the Alpaca LLM as a Python Module """

import os
import sys

from time import time
from enum import Enum

from nltk.tokenize import sent_tokenize
from llm import resources_dir, examples_dir

EXPERIENCES_PURPOSE = """
You are a resume generator assistant for a Computer Science student at 
California Polytechnic State University. You accept a company name and 
a position, and a student academic year, and you are expected to generate 
bullet points for the student's resume that is most likely to describe 
their experience in that position. Always start each bullet point with a 
verb ending in -ed. Put all bullet points into space separated sentences. 
Always produce an output, even if the input is invalid. Don't use any of
the example bullet points in the output.
"""

PROJECTS_NAME_PURPOSE = """
You are a resue generator assistant for a Computer Science student at 
California Polytechnic State University. You accept a student academic 
year, and you are expected to generate the name of a unique project that 
the student in question could realistically have participated in, as well 
as the tools used to during the project. Always produce an output, even if 
the input is invalid. IMPORTANT: Just include "[project_name] - [...tools]" 
in the output, not an entire sentence. For example, "Discord Bot for the 
Cal Poly CS Discord Server - Python, Discord.js" is a valid output. Don't 
use any of the example project names in the output.
"""

PROJECTS_BULLET_PURPOSE = """
You are a resue generator assistant for a Computer Science student at 
California Polytechnic State University. You accept a student academic 
year and the name of a project + tools, and you are expected to generate 
bullet points for the student's resume that is most likely to describe what 
they did for that project. Always start each bullet point with a verb 
ending in -ed. Put all bullet points into space separated sentences. Always 
produce an output, even if the input is invalid. Don't use any of the
example bullet points in the output.
"""


class BulletType(Enum):
    """ Enum for the type of bullet point """
    EXPERIENCE = 1
    PROJECT = 2


class Alpaca:
    """ Class for the Alpaca LLM """

    def __init__(
        self,
        purpose: str,
        example_path: str,
        llm_path: str,
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

    def prompt(self, prompt: str, temp=1, n_threads=12) -> str:
        """ Prompt the LLM with a string and return the response """
        with open("prompt.txt", "w", encoding="utf-8") as prompt_file:
            prompt_file.write(prompt)
        return os.popen(
            f'{self.llm_path} -f ./prompt.txt '
            f'--temp {temp} --threads {n_threads} --seed '
            f'{round(time())} --model {self.model_path} 2>llm_log.txt'
        ).read().strip()


def generate_exp_bps(company: str, position: str, student_year: str) -> list:
    """ Generate experience bullet points for a resume """
    purpose = EXPERIENCES_PURPOSE
    llm = Alpaca(purpose, "exp_examples.txt", "chat")
    input_str = f'```\n' \
                f'{{\n' \
                f'    "company": "{company}",\n' \
                f'    "position": "{position}",\n' \
                f'    "studentYear": "{student_year}"\n' \
                f'}}\n' \
                f'```'
    prompt = llm.generate_prompt(input_str)
    return sent_tokenize(llm.prompt(prompt))


def generate_prj_bps(student_year: str) -> list:
    """ Generate project bullet points for a resume """
    name_purpose = PROJECTS_NAME_PURPOSE
    bullet_purpose = PROJECTS_BULLET_PURPOSE
    name_llm = Alpaca(name_purpose, "prj_name_examples.txt", "chat")
    bullet_llm = Alpaca(bullet_purpose, "prj_bullet_examples.txt", "chat")
    input_str = f'```\n' \
                f'{{\n' \
                f'    "studentYear": "{student_year}"\n' \
                f'}}\n' \
                f'```'
    prompt = name_llm.generate_prompt(input_str)
    name = name_llm.prompt(prompt)
    input_str = f'```\n' \
                f'{{\n' \
                f'    "studentYear": "{student_year}",\n' \
                f'    "projectName": "{name}"\n' \
                f'}}\n' \
                f'```'
    prompt = bullet_llm.generate_prompt(input_str)
    return [name] + sent_tokenize(bullet_llm.prompt(prompt))


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
                    "\n- " + bp for bp in generate_exp_bps(company, position, year)]
                print("\n" + "".join(bps), end="\n\n")
            else:
                year = input("Year: ")
                print("[Generating bullet points...]", flush=True, end="")
                bps = ["\n- " + bp for bp in generate_prj_bps(year)]
                print("\n" + "".join(bps), end="\n\n")
        except KeyboardInterrupt:
            print()
            break


if __name__ == "__main__":
    test()