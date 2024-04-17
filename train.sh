
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
echo $SCRIPTPATH
PROJECTROOTPATH="$(dirname "$SCRIPTPATH")"
echo $PROJECTROOTPATH
pyenv install 3.8.16
pyenv local 3.8.16
python3 -m venv renv
source ${SCRIPTPATH}/renv/bin/activate
"${SCRIPTPATH}"/rasaenv/bin/pip3 install --upgrade setuptools pip
"${SCRIPTPATH}"/rasaenv/bin/pip3 install spacy
"${SCRIPTPATH}"/rasaenv/bin/pip3 install rasa
"${SCRIPTPATH}"/rasaenv/bin/pip3 install rasa[convert]
"${SCRIPTPATH}"/rasaenv/bin/pip3 install rasa[spacy]
"${SCRIPTPATH}"/rasaenv/bin/pip3 install rasa[transformer]
"${SCRIPTPATH}"/rasaenv/bin/python3 -m spacy download en_core_web_md
"${SCRIPTPATH}"/rasaenv/bin/python3 -m spacy link en_core_web_md en

rasa train 