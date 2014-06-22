cardscan
========

Python command-line tool to parse scanned documents with cards to various data structures

features:
 - Reads cards from any valid image source for [SimpleCV][simplecv] (Currently expects 300 dpi images)
 - Outputs a yaml or json data structure
 - Reads multiple cards from a single image (Multiple cards on the scanbed)
 
Supported cards:
 - Dutch personal indentification card
 
## Installation

cardscan depends on `python2.7`, `SimpleCV`, `pyyaml`, `tesseract-ocr` and `python-tesseract`

```bash
$ sudo apt-get install python2 tesseract-ocr
# simplecv instructions
$ sudo apt-get install ipython python-opencv python-scipy python-numpy python-pygame python-setuptools python-pip
$ sudo pip install https://github.com/sightmachine/SimpleCV/zipball/develop
# python-tesseract installation
$ wget "https://bitbucket.org/3togo/python-tesseract/downloads/python-tesseract_0.9-0.3ubuntu0_amd64.deb"
$ sudo dpkg -i python-tesseract_0.9-0.3ubuntu0_amd64.deb
$ sudo apt-get -f install
# pyyaml installation
$ sudo pip install pyyaml
# cardscan installation
$ git clone git@github.com:MartijnBraam/cardscan.git
$ cd cardscan
$ echo ":)"
```
 
 
  [simplecv]: http://simplecv.org/
