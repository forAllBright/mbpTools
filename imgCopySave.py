#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: forAllBright
# @Date:   2018-12-13 20:54:20
# @Last Modified by:   forAllBright
# @Last Modified time: 2018-12-14 23:50:21

from PIL import ImageGrab  # ImageGrab == 5.0.0 works fine on MacOS 10.11.6 EiCapitan, other versions may cause IO error as "CGSLookupServerRootPort: Failed to look up the port for "com.apple.windowserver.active"
import os
import argparse
import re
import git
import time

parser = argparse.ArgumentParser(
    description="image saved locally from clipboard")
parser.add_argument(
    "-n", "--name", required=True, help="set the name of the image locally")
parser.add_argument(
    "-s", "--size", required=False, help="set the size of saving image")
args = parser.parse_args()


class SaveImg:
    def __init__(self, saveFolder, imageFormat='PNG'):
        """[summary]

        [description]

        Arguments:
            saveFolder {str} -- [image to be saved folder path]

        Keyword Arguments:
            imageFormat {str} -- [the format of image to be saved] (default: {'PNG'})
            imgSize {tuple} -- [the 2-D Pixel size of image to be saved] (default: {(500,500)})
        """
        self.saveFolder = saveFolder
        self.Ag = Ag(args.name,
                     args.size)  # init Ag object with 2 args from command line
        self.imageFormat = self.Ag.verifyFormatCorrect(
        )['imgformat'] if self.Ag.verifyFormatCorrect(
        )['imgformat'] else imageFormat
        self.name = self.Ag.imgPathFile
        self.imgSize = self.Ag.imgSizeTuple
        self.newFilePath = r'{0}/{1}'.format(self.saveFolder, self.name)
        self.clip2Save()

    def getLastCreatedImgAndVerify(self):
        """[summary]

        [Get the last modified(Created) file in the folder and verify the last one is exactly the new one to be saved]

        Returns:
            [bool] -- [True means the last file inside the folder is indeed the one to be prepared to saved
            which means the image save from clipboard succeed]
        """
        currentAllFiles = filter(lambda x: not x.endswith('.git'),
                                 os.listdir(self.saveFolder))
        tmp = [
            r'{0}/{1}'.format(self.saveFolder, file)
            for file in currentAllFiles
        ]
        tmp.sort(key=lambda x: os.stat(x).st_mtime)
        lastCreateFile = tmp[-1]
        return lastCreateFile == self.newFilePath

    def clip2Save(self):
        """[summary]

        [The behavior to save image or do nothing]
        """
        img = ImageGrab.grabclipboard()
        if img is None:
            print(bcolors.RED + "Invalid image in clipboard" + bcolors.ENDC)
            os._exit(0)
        elif self.overWriteImg():
            if args.size:
                img = self.resizeImg(img, self.Ag.specialParse())
            img.save(self.newFilePath, self.imageFormat)
        else:
            print(bcolors.BLUE + '\nCancel process\n' + bcolors.ENDC)
            os._exit(0)

    def overWriteImg(self):
        """[summary]

        [If no conflict about the file name to be saved then return True defaultly which means
        process on saving file to the folder, Otherwise, will prompt for user's input to choose
        yes or no to overwrite file existed and return True for yes, False for no to cancel and exit the process]

        Returns:
            bool -- [Will process writing image to this folder?]
        """
        currentAllFiles = os.listdir(self.saveFolder)
        if self.name in currentAllFiles:
            while True:
                userPrompt = input(
                    'The same name file existed. Are you sure overwrite it? type yes or no --> '
                )
                if userPrompt not in ['yes', 'no']:
                    print(bcolors.RED + "Wrong type!!!\n" + bcolors.ENDC)
                else:
                    break
            if userPrompt == 'yes':
                try:
                    os.remove(self.newFilePath)
                    return True
                except:
                    print(bcolors.RED + "Overwrite same name file process error!!!" + bcolors.ENDC)
                    os._exit(0)
            else:
                return False
        else:
            return True

    def resizeImg(self, img, newSize):
        """[summary]

        [description]

        Arguments:
            img {PIL.img} -- [Resize the image for saving from original one of clipboard.]
            newSize {tuple} -- [tuple with two numerical elements]

        Returns:
            [PIL.img] -- [resized img of PIL.img type]
        """
        print('\n{}\n'.format(img.size))
        resizedImg = img.resize(newSize)
        # print("*********************************************")
        # print(resizedImg.size)
        return resizedImg


class Ag:
    def __init__(self, imgfilePath, imgSizeTuple):
        """[summary]

        [Initialize an instance with two arguments from command line]

        Arguments:
            imgfilePath {str} -- [string name of the file to be saved]
            imgSizeTuple {str} -- [string of a tuple with two numerical elements]
        """
        self.imgPathFile = imgfilePath
        self.imgSizeTuple = imgSizeTuple
        self.veri = {}

    def verifyFormatCorrect(self):
        """[summary]

        [Verify if the string format is correct]

        Returns:
            [dict] -- [dict with 3 keys which are 1.imgname format corrent? 2.size format correct? 3.img format]
        """
        self.veri['imgV'] = False
        self.veri['sizeV'] = False
        self.veri['imgformat'] = None
        # imgFilePath format verify
        for fmt in ['.png', '.jpg']:
            if self.imgPathFile[-4:] == fmt:
                self.veri['imgV'] = True
                self.veri['imgformat'] = fmt[1:].upper()
                break
        else:
            print(bcolors.RED + "image file path format is invalid!!!" + bcolors.ENDC)
            os._exit(0)
        # imgSizeTuple format verify
        if self.imgSizeTuple is None or re.search("\(\d+,\d+\)",
                                                  self.imgSizeTuple):
            self.veri['sizeV'] = True
        else:
            print(bcolors.RED + "size format is invalid!!!" + bcolors.ENDC)
            os._exit(0)

        return self.veri  # Return a dict

    def specialParse(self):
        """[summary]

        [Special parser to convert string of img size tuple to exact tuple]

        Returns:
            [tuple] -- tuple of string size tuple or None if not set the arg
        """
        assert self.imgSizeTuple is not None, "ERROR"
        return eval(self.imgSizeTuple)


class RemoteGit:
    def __init__(self, localGitFolderPath, updatefilename):
        self.localGitFolderPath = localGitFolderPath
        self.repo = git.Repo(self.localGitFolderPath)
        self.updatefilename = updatefilename

    def addCommitPush(self):
        g = git.cmd.Git(r"{}".format(self.localGitFolderPath))
        g.execute(["git", "add", "{}".format(self.updatefilename)])
        g.execute([
            "git", "commit", "-m",
            "update image: {}".format(self.updatefilename)
        ])
        g.execute(["git", "push", "origin", "master"])

    def checkGitConnection(self):
        repo = git.Repo(r"{}".format(self.localGitFolderPath))
        try:
            repo.remotes.origin.fetch()
        except:
            pass
            return False
        return True

    # def wait_timeout(proc, seconds):       # not work
    #     """Wait for a process to finish, or raise exception after timeout"""
    #     start = time.time()
    #     end = start + seconds
    #     interval = min(seconds / 1000.0, .25)

    #     while True:
    #         result = proc.poll()
    #         if result is not None:
    #             return result
    #         if time.time() >= end:
    #             raise RuntimeError("Git connect check time out!!!")
    #         time.sleep(interval)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[1;31;1m'
    BLUE = '\033[1;34;1m'
    GREEN = '\033[1;32;1m'
    CYAN = "\033[1;36;1m"


if __name__ == "__main__":
    """[summary]

    [Here is the main playing ground]
    """
    imageFolder = r"/Users/pmz/gitee/Blogpics"
    repoGit = RemoteGit(imageFolder, args.name)
    if not repoGit.checkGitConnection():
        os._exit(1)
    else:
        print(bcolors.GREEN + "\nChecking git connection complete........\n" +
              bcolors.ENDC)
    startSaveImg = SaveImg(imageFolder)
    if startSaveImg.getLastCreatedImgAndVerify():
        repoGit.addCommitPush()
        print(bcolors.GREEN +
              "\nPush to remote repository complete.........\n" + bcolors.ENDC)
        os.system(r"open {}".format(startSaveImg.newFilePath))
        imgurl = r"https://gitee.com/Pbright/Blogpics/raw/master/{}".format(
            startSaveImg.name)
        os.system(r"echo '![{0}]({1})' | pbcopy".format(
            startSaveImg.name, imgurl))
        print(bcolors.GREEN +
              "\nCopy remote image url to clipboard complete..........\n" +
              bcolors.ENDC)
    else:
        print("""
               ,ad8888ba,
             d8"'    `"8b
            d8'        `8b
            88          88  ,adPPYba,   ,adPPYba,  8b,dPPYba,  ,adPPYba,
            88          88 a8"     "8a a8"     "8a 88P'    "8a I8[    ""
            Y8,        ,8P 8b       d8 8b       d8 88       d8  `"Y8ba,
             Y8a.    .a8P  "8a,   ,a8" "8a,   ,a8" 88b,   ,a8" aa    ]8I 888 888 888
              `"Y8888Y"'    `"YbbdP"'   `"YbbdP"'  88`YbbdP"'  `"YbbdP"' 888 888 888
                                                   88
              """)