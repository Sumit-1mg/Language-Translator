# Language-Translator

## Project Description

This project is a Language Translator web application built using the Sanic framework and three public APIs (Lacto API, Rapid API, and Google API). The application allows users to translate text from one language to another and also detect the source language of a given text.

## Prerequisites
Before running the project, make sure you have the following installed:
1. Python 3.11
2. Pipenv (for managing Python dependencies)

## Installation
Install project dependencies using Pipenv:  
    pipenv install --dev

## Usage

1. Activate the virtual environment:  
    pipenv shell
2. Start the Sanic server:   
    python3 -m app.service
3. Open your web browser and navigate to http://127.0.0.1:8000 to access the translate.html page. This page allows you to input the source language, text, and target language for translation.
4. If you want to use the language detection feature, access the detection.html page by typing http://127.0.0.1:8000/find in your browser. On this page, you can enter the text and click the "Detect" button to view the detected source language.


