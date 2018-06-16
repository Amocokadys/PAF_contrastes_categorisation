#!/bin/bash

mkdir -p 'livres bureautique'
mkdir -p 'livres'

liste_bureautique=`ls -1 'livres bureautique' | sed 's/ - /_/g' | sed 's/ /_/g'`

for livre in `echo $liste_bureautique`
do
	if [ -n `echo $livre | grep '.odt'` ] 
	then
		#odt2txt $livre
		echo "odt    : $livre"
	elif [ -n `echo $livre | grep '.doc'` ]
	then 
		equivalent=`echo $livre | sed 's/.doc/.odt/g'`	
		if [ -z `ls -1 | grep $equivalent`]
		then
			echo "doc    : $livre"
		fi
	fi
done

