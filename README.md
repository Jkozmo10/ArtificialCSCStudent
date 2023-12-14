# Resumator

Resumator is a project created by [Nathan McCutchen](https://github.com/N8WM), [Jeremy Kozlowski](https://github.com/Jkozmo10), ... for **CSC 482** &mdash; *Speech and Language Processing* at Cal Poly.

## Setup

This project requires Python 3.8+ and a system running MacOS or Linux. If you do not have Python 3.8 installed, you can download it [here](https://www.python.org/downloads/).

### Clone the repository

First clone the repository with the `git clone` command:

```sh
git clone https://github.com/RG-mania/CSC482-Project.git
```

Then `cd` into the repository:

```sh
cd CSC482-Project
```

### Create a virtual environment (optional)

This step is optional, but recommended. To create a virtual environment, run the following command:

```sh
mkdir .venv && python3 -m venv .venv
```

Then activate the virtual environment:

```sh
source .venv/bin/activate
```

### Install Python dependencies

```sh
pip install -r requirements.txt
```

### Download LLM weights and NLTK data

This will create a folder in your home directory (`~/nltk_data`). If you prefer, you can safely delete the folder after you are done with this project.

```sh
python3 -c "from llm import alpaca; alpaca.download()"
```

## How to Run the Resume Generator (GUI/CLI)

Our project has both graphical and command-line interfaces.

### Running the GUI

The GUI requires the webapp to be running.

The webapp can be run with the following command:

```sh
python3 server.py
```

With the webapp, navigate to http://localhost:8000 in your browser and you should see the GUI.

The architecture of the GUI will now be described. server.py contains all the endpoints. The page is generated with using a template html page. Templates are found in the /templates directory. Any data that needs to be displayed are found in the /static directory. Thus for resumes to be displayed, they must be moved to the /static directory. 

### Running the CLI

Description...

```sh
python3 ...
```

## About the Project

Description...

## Resources

Our project uses a combination of open source libraries and tools:

- [antimatter15/alpaca.cpp](https://github.com/antimatter15/alpaca.cpp) (forked from [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)) &mdash; Alpaca language model
- [Sosaka/Alpaca-native-4bit-ggml](https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml) &mdash; Alpaca language model weights
