# Raspberry-PI-Vector-Server
A simple python server running on my raspberry pi, meant to handle EVERYTHING that an anki vector could do and respond.

STT / TTS Core: These handle the Speech to Text and Text to Speech modules.
Vector Brain: Decides what to do
App: the server

Workflow:

User asks vector something. Vector listens, and creates an audio file.

Audio file is sent to APP, which calls STT to parse speech audio file into text. Once the text is created, it is stored in vectors memory, and the audio file is deleted.

APP sends text to VECTOR BRAIN, who uses logic to decide what to do with it. If VECTOR BRAIN detects user wants vector to say something, it will call TTS.

Vector creates his response, as well as an intended action depending on the request. If he is asked to say something, the TTS will make a temporary audio file that will
be played to the user, and then deleted after playing.
