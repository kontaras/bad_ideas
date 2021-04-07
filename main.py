import textile
import os
import shutil

inFolder = os.path.abspath("content")
staticFolder = os.path.abspath("static")
outFolder = os.path.abspath("outsite")
outFileExt = ".html"
indexFileName = "index"

def init():
    os.makedirs(outFolder, exist_ok=True)

def place_static():
    shutil.copytree(staticFolder, outFolder, dirs_exist_ok=True)

def render_files():
    for root, _, files in os.walk(inFolder):
        relRoot = os.path.relpath(root, inFolder)
        for fileName in files:
            inPath = os.path.join(root, fileName)
            inFileRoot, _ = os.path.splitext(fileName)
            outPath = os.path.join(outFolder, relRoot, inFileRoot) + outFileExt
            render_file(inPath, outPath)

def render_file(inFile, outFile):
    with open(inFile, "r") as inStream:
        input = inStream.read()
        with open(outFile, "w") as outStream:
            outStream.write(textile.textile(input))

def generate_index():
    index_file_path = os.path.join(outFolder,indexFileName) + outFileExt
    print(index_file_path)
    with open(index_file_path, "w") as index_file:
        index_file.write("This is the index.\n")

def generate():
    init()
    place_static()
    render_files()
    generate_index()

if __name__ == "__main__":
    generate()
