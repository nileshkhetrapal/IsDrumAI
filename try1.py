from contextlib import suppress
from pyAudioAnalysis import audioTrainTest as aT
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import ShortTermFeatures
import matplotlib.pyplot as plt
import os
import sys
import shutil
#This project was made by Nilesh Khetrapal under the guidance of Prof. Frank Canovatchel
#This project will not work without installing pyAudioAnalysis first. Please make sure to install that before attempting to run it.
#This code uses the pyAudioAnalysis library to classify samples as drums or instrumental pieces of music
#So far the model has not been tested thoroughly but early results indicate that the model works well
#Run this code, the simple and quick interface will let you use this software to sort all your samples or test a sample.
print("Hello, this is a simple tool to differentiate between drum samples and instrumental samples ")
print("Make sure all the folders you deal with are in the directory this code is in. It will not work otherwise.")
print("This project already has a trained model, but if you feel that you need to train it again, just replace the files in classifierData and run option no. 3")
userInput = int(input("Press 1 for classifying one sample, input 2 for sorting the samples into two directories (this will automatically create two directories within the folder), input 3 for training the model with newer samples"))
#This is my way of interacting with the user
def trainmodel(FileFolder):
    realpath = "{}/{}"
    aT.extract_features_and_train([realpath.format(FileFolder, "Instrumentals"),realpath.format(FileFolder, "Drums")], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "try54", False, train_percentage=0.90)

def classifying_a_sample(testFileFolder, name_of_file):
    #This function uses the pyAudioAnalysis library to check if a sample is an instrumental or a drum
    #This function uses the model try54
    #Without all the necessary files downloaded, it will not work
    aT.load_model_knn("try54", False)
    file_location = "{}/{}"
    probability_of_instrumental = [aT.file_classification(file_location.format(testFileFolder, name_of_file), "try54", "knn")[1][0]]
    # This gives us an integer called probability_of_instrumental the 1 at the end lets us only get the probability array and 0 at the end only gets us the first value of the array
    if probability_of_instrumental[0] > 0.5:
        answer_str = ("The sample is an Instrumental")
        isDrum = False #I am using this to save cpu power and increase speed while sorting
    else:
        answer_str = ("The sample is a Drum")
        isDrum = True
    return answer_str, isDrum

if userInput == 1:
    name_of_file = str(input("input the name of the file (without .wav) in the data folder. Hit enter for default (test)")) #standard input method on several python projects
    if name_of_file == "":
        name_of_file = "test.wav"
    testFileFolder = str(input("input the name of the folder with the sample you want to test, hit enter for default (./data)"))
    if testFileFolder == "":
        testFileFolder = "data"
    print(classifying_a_sample(testFileFolder, name_of_file)[0]) #it calls the function to classify this sample. The 0 at the end indicates that only the str will be returned.
elif userInput == 2:
    path = str(input("input the name of the folder that has all the samples. Press enter for default(plxsort)"))
    if path == "":
        path = "plxsort"
    files = os.listdir(path)
    print("These are the files chosen- ", files)
    canidoit = str(input("Do you want to train the model using this data as well? y/n?")) #asking for permission before training your ai with it is important.
    if canidoit == "y": #I didn't want to let the user type true or false, asking for y or n is pretty standard.
        doit = True
    else:
        doit = False
    realpath = "{}/{}" #I find it funny how much time these saved me and how much I actually ended up using them.
    veryrealpath = "{}/{}/{}"
    for file in files: #Using file for variable just makes it read easier
        if classifying_a_sample(path, file)[1]: #This returns a boolean, if isdrum is true then path1 will be set as Drums
            path1 = "Drums"
        else:
            path1 = "Instrumentals"
        if not os.path.exists(realpath.format(path, path1)): #This is a simple code used for checking if the subdirectories already exist, really saves a lot of time.
            os.mkdir(realpath.format(path, path1))
            print("made directory " + realpath.format(path, path1))
        os.rename(realpath.format(path, file), veryrealpath.format(path, path1, file))
        if doit:
         shutil.copy(veryrealpath.format(path, path1, file), realpath.format("classifierData", path1))
        print("{} transferred successfully into ".format(file), path1)
    if doit:
     trainmodel("classifierData")
elif userInput == 3:
    FileFolder = str(input("enter the folder where the new data is. Make sure that dataset is divided into two folders- Drums and Instrumentals, Press enter for default (classifierData)"))
    if FileFolder == "":
        FileFolder = "classifierData"
    realpath = "{}/{}"
    aT.extract_features_and_train([realpath.format(FileFolder, "Instrumentals"), realpath.format(FileFolder, "Drums")],
                                  1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "try54", False,
                                  train_percentage=0.90)
    print("training complete")


