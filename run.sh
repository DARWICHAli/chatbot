#!/bin/bash


echo Downloading requirements
#pip install -r requirements.txt
echo Done




cd ./static
mkdir model
cd model

#https://drive.google.com/file/d/1QAbnIvz7OgZnejdUfDgOhJ5izJYqvA_y/view?usp=share_link (model-classification)
#https://drive.google.com/file/d/1xkWruxx3YbAUdBaFW8c4rMII4TVTsaha/view?usp=sharing (model-extraction) 


echo Downloading Model-classification
#wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1QAbnIvz7OgZnejdUfDgOhJ5izJYqvA_y' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1QAbnIvz7OgZnejdUfDgOhJ5izJYqvA_y" -O model-classification.zip && rm -rf /tmp/cookies.txt
echo Done


echo Downloading model-extraction

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1QsAg7WxfED91pQz6pDnyJsbsAqctkkan' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1QsAg7WxfED91pQz6pDnyJsbsAqctkkan" -O model-extraction.zip && rm -rf /tmp/cookies.txt

echo Done

echo unzipping models
unzip  model-classification.zip
mv model model-classification
rm -r model
unzip  model-extraction.zip
mv model-best model-extraction

echo Done



cd ../../
pwd


python3 app.py
