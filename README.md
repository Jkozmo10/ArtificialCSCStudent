# Resumator

Resumator is a project created by [Nathan McCutchen](https://github.com/N8WM) ..., for **CSC 482** &mdash; *Speech and Language Processing* at Cal Poly.

## Setup

This project requires Python 3.8+ and a system running MacOS or Linux. If you do not have Python 3.8 installed, you can download it [here](https://www.python.org/downloads/).

### Clone the repository

First clone the repository with the `git clone` command:

```sh
$ git clone https://github.com/RG-mania/CSC482-Project.git
```

Then `cd` into the repository:

```sh
$ cd CSC482-Project
```

### Create a virtual environment

This step is optional, but recommended. To create a virtual environment, run the following command:

```sh
$ mkdir .venv && python3 -m venv .venv
```

Then activate the virtual environment:

```sh
$ source .venv/bin/activate
```

### Install Python dependencies

```sh
$ pip install -r requirements.txt
```

### Download the LLM weights

```sh
$ python3 -c "from llm import alpaca; alpaca.download()"
```

## How to Run the Resume Generator (GUI/CLI)

Our project has both graphical and a command line interfaces. It can be run from either, but the GUI may have some bugs.

### Running the GUI

The GUI requires two separate backend and frontend processes to be running simultaneously.

The backend can be run with the following command:

```sh
$ python3 ...
```

To run the frontend, open a new terminal window, `cd` into the project directory, and run the following command:

```sh
$ python3 ...
```

With both both the backend and frontend running, navigate to http://localhost:5000 in your browser and you should see the GUI.

Continue explaining the GUI...

### Running the CLI

Description...

```sh
$ python3 ...
```

## About the Project

Description...

## Resources

Our project uses a combination of open source libraries and tools:

- [antimatter15/alpaca.cpp](https://github.com/antimatter15/alpaca.cpp) (forked from [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)) &mdash; Alpaca language model
- [Sosaka/Alpaca-native-4bit-ggml](https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml) &mdash; Alpaca language model weights