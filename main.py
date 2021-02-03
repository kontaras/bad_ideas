import textile
import os
import shutil

inFolder = os.path.abspath("content")
staticFolder = os.path.abspath("static")
outFolder = os.path.abspath("outsite")
outFileExt = ".html"

def render(inFile, outFile):
    with open(inFile, "r") as inStream, open(outFile, "w") as outStream:
        outStream.write(textile.textile(inStream.read()))

os.makedirs(outFolder, exist_ok=True)

shutil.copytree(staticFolder, outFolder, dirs_exist_ok=True)

for root, _, files in os.walk(inFolder):
    relRoot = os.path.relpath(root, inFolder)
    for fileName in files:
        inPath = os.path.join(root, fileName)
        inFileRoot, _ = os.path.splitext(fileName)
        outPath = os.path.join(outFolder, relRoot, inFileRoot) + outFileExt
        render(inPath, outPath)
