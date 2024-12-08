algo naïf :
tous les maw sont des substrings de  taille i+1 par rapport à 2 kmer de taille i de s 
=> on sample toutes les kmer de taille i pour i in range(k)
et on teste pour tout ajout de lettre au début ou à la fin si on l'a dans la string ou non.

