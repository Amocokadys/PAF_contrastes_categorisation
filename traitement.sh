#!/bin/bash

mkdir -p 'temp_bureautique'
mkdir -p 'livres'

liste_bureautique=`ls -1 ~/Téléchargements`

function nettoyer_texte() {
	if [ -n "`grep 'édition électronique' "$1"`" ]
	then
		echo "$1 -> suppression du message de fin"
		sed -i "`grep -n 'édition électronique' "$1"  | tail -n1 | sed 's/^\([0-9]*\):.*/\1/'`,$ d" "$1"
	fi
	if [ -n "`grep 'CHAPITRE PREMIER' "$1"`" ]
	then
		echo "$1 -> suppression du sommaire"
		sed -i "1,`grep -n 'CHAPITRE PREMIER' "$1"  | tail -n1 | sed 's/^\([0-9]*\):.*/\1/'` d" "$1"
	fi
	if [ -n "`grep 'PREMIÈRE PARTIE' "$1"`" ]
	then
		echo "$1 -> suppression du sommaire"
		sed -i "1,`grep -n 'PREMIÈRE PARTIE' "$1"  | tail -n1 | sed 's/^\([0-9]*\):.*/\1/'` d" "$1"
	fi
	sed -i '/CHAPITRE/ d' "$1"
}

for livre in $liste_bureautique
do
	
	
	equivalent=`echo $livre | sed -e 's/\.zip$//'`
	reformat=`echo $equivalent | sed 's/\([[:alpha:]]*\)_\(.*\)_source/\2 - \1/'`
	if [ ! -e "livres/$reformat" ]
	then
		unzip -d './temp_bureautique/' "$HOME/Téléchargements/$livre"
	
		if [ -e "temp_bureautique/$equivalent.odt" ]
		then
			odt2txt "temp_bureautique/$equivalent.odt" > "livres/$reformat"
			nettoyer_texte "livres/$reformat"
		
		elif [ -e "temp_bureautique/$equivalent.doc" ]
		then
			libreoffice --headless --convert-to "txt:Text (encoded):UTF8" "temp_bureautique/$equivalent.doc" > /dev/null
			mv "$equivalent.txt" "livres/$reformat"
			nettoyer_texte "livres/$reformat"
			
		else			
			echo "WARNING : $equivalent n'a pas d'équivalent de même nom en format .doc ni .odt."
			
		fi
	fi
done

