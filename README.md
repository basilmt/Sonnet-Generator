# Sonnet Generator
# ADAWIE20FORGE



## File Structure
---
* Sonnet Generator
    * assets
        * fonts
            * DMSerif.ttf
            * OldLondon.ttf
        * images
            * scroll.png
    * datasets
        * dataset.txt
        * dataset2.txt
    * backend.py
    * datavisual.py
    * README.md
    * requirements.txt
    * test.py
    * uiscroll.py

  
>We can add additional datasets as .txt  file inside the folder *datasets* for training the model


## Install necessary packages
---
1. Run the below code in Terminal(Command Prompt or IDE terminal)
    ```bash
    pip install -r requirements.txt
    ```
2. Type python in the terminal
    ```bash
    python
    ```
3. It will open up a python terminal for you
4. Type the below code in Python Terminal
    ```python
    >>>import nltk
    >>>nltk.download('cmudict')
    >>>nltk.download('wordnet')
    ```

## Run the program(UI)
---
### Using Command Prompt

1. Open Command Prompt
2. Change working directory to the folder Sonnet Generator
3. Run the below code to open the UI
    ```bash
    python uiscroll.py
    ```
4. It will open up the UI with a generated sonnet
5. Click on "Generate" button to generate next sonnet

### Using IDE
1. Open the Folder Sonnet Generator in the IDE
2. Install necessary packages as mentioned above in IDE terminal
3. Run uiscroll.py
4. It will open up the UI with a generated sonnet
5. Click on "Generate" button to generate next sonnet

## Visualisation of program(Dataset)
---
### Using Command Prompt

1. Run the below code to open the visualisation
    ```bash
    python datavisual.py
    ```

### Using IDE

1. Run datavisual.py

tested on : windows 10 Home (64-bit OS)
