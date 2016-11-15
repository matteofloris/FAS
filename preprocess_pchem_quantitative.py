import sys, os

ROOT = sys.argv[1]

frammenti = {}
nomi_frammenti = {}
molecole  = {}
nomi_molecole  = {}
c_fr = 1
c_mo = 1

###4697-14-7	9	>= 2 C
f = open(ROOT + ".pcfrags", "r")
for l in f:
	mol = l.split("\t")[0].strip()
	fra = l.split("\t")[1].strip()
	if mol not in molecole: 
		molecole[mol] = []
		ID_mo = "MOL_" + str(c_mo)
		nomi_molecole[mol] = ID_mo
		c_mo += 1
	if fra not in frammenti: 
		frammenti[fra] = []
	molecole[mol].append( fra )
	frammenti[fra].append( mol )
f.close()
muta = {}
###O=C([O-])C(C(=O)NC2C(=O)N1C(C(=O)[O-])C(C)(C)SC12)c3ccsc3	4697-14-7	0
f = open(ROOT + ".smi", "r")
for l in f:
	if "SMILES" not in l:
		r = l.strip()
		###print r.strip().split("\t")[0].strip()
		if r.strip().split("\t")[1].strip() in nomi_molecole:
			nome_mol = nomi_molecole[ r.strip().split("\t")[1].strip() ]
			muta[ nome_mol ] = r.strip().split("\t")[2].strip().replace("NON-Mutagen", "1").replace("Mutagen", "2")			
f.close()

lista_frammenti = frammenti.keys()
c = 1
o = open(ROOT + ".ped", "w")
for M in molecole:
	nome_mol = nomi_molecole[M]
	if nome_mol in muta and M in molecole:
		print "ok"
		tox = muta[ nome_mol ]
		s = []
		for FR in lista_frammenti:
			if FR in molecole[ M ]: 
				s.append("T A")
			else: s.append("T T")
		o.write( "FAM" + str(c) + " " + nomi_molecole[M] + " " + " " + tox + " " + " ".join(s) + "\n" )
		c += 1
o.close()

c = 1
o = open(ROOT + ".map", "w")
for FR in frammenti:
	o.write( "1\t" + FR + "\t0\t" + str(c) + "\n" )
	c += 1
o.close()

