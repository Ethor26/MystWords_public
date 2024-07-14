from string import ascii_lowercase
from enum import Enum
import numpy as np
# from numba import jit
# =============================
# GESTION DES ALPHABETS

# ------------------
# ENUM : liste des alphabets possibles
class Alphabet_types(Enum):
    SPECIAL = 0
    LATIN = 1
    ARAMEEN = 2

# ------------------
# CLASS ALPHABET : permet de gérer les détails d'un alphabet
class Alphabet():
    def __init__(self, typeAlphab):
        self.typeAlphab = typeAlphab # Attribut représentant le type de l'alphabet défini par l'enum
        # ."__...__" Pour privatiser variable, inutile avec getattr
        self.tabAlphab = self.GetAlphabet_fromEnum(self.typeAlphab) # Attribut représentant le tableau avec l'alphabet
        self.dir_resCartProd = self.getDirectoryForAlphab(self.typeAlphab) # Attribut représentant le dossier
        # utilisé pour l'affichage avec le produit cartésien

    def __repr__(self):
        return "Alphabet_" + self.typeAlphab

    # ------------------
    # FONCTION Attribue le bon dossier selon le type d'alphabet
    @staticmethod
    def getDirectoryForAlphab(alphabUsed):
        if alphabUsed == Alphabet_types.LATIN:
            return "ResCartProd_AlphabetLatin"
        elif alphabUsed == Alphabet_types.ARAMEEN:
            return "ResCartProd_AlphabetHebreu"

    # ------------------
    # FONCTION Attribue le bon tableau selon le type d'alphabet
    @staticmethod
    def GetAlphabet_fromEnum(Alphab_enum):
        list_char_norm = [] # liste des caractères appartenant à une langue définie, non spéciaux

        # ------------------
        # FONCTION interne qui vérifie si le type d'alphabet est celui en paramètre, sinon inclus l'alphabet en paramètre
        # dans la list des charactères normaux
        def verifAlphab_fromEnum(Alphab_studied, enum_alphab):
            if Alphab_enum == enum_alphab:
                return True
            list_char_norm.extend(list(map(ord, Alphab_studied)))
            return False

        # Vérification pour chaque type d'alphabet s'il correspond à Alphab_enum
        if verifAlphab_fromEnum(list(ascii_lowercase), Alphabet_types.LATIN): return list(ascii_lowercase)
        if verifAlphab_fromEnum(list(map(chr, range(1488, 1515))), Alphabet_types.ARAMEEN): return list(map(chr, range(1488, 1515)))

        # Si aucun alphabet n'a correspondu à Alphab_enum, il est de type spécial donc on retourne le tableau des
        # caractères spéciaux : caractères hors langue déclarée et pas dans list_char_norm
        else:
            list_char_spec = list(set(list(range(1, 1114112))).difference(set(list_char_norm)))
            # On fait la différence de la liste de tous les charactères avec celles des caractères normaux pour avoir les spéciaux.
            """ # Pour différence absolue (si list char norm non inclu dans range_thr(1, 1114112)
            list_char_spec = list(
                    (set(list(range_thr(1, 1114112))).difference(set(list_char_norm)))
                     .union
                    (set(list_char_norm).difference(set(list(range_thr(1, 1114112)))))
            )
            """
            return list(map(chr, list_char_spec))

    # ------------------
    # FONCTION retourne le type d'alphabet du caractère entré
    @staticmethod
    def GetTypeAlphab_fromChar(char):
        for type_alphab in Alphabet_types:
            Alphabet_tested = Alphabet(type_alphab)
            if ord(char) in map(ord, Alphabet_tested.tabAlphab):
                return Alphabet_tested.typeAlphab

    # ------------------
    def get_particular_letters(self):
        if self.typeAlphab == Alphabet_types.ARAMEEN:
            return sorted(['ך', 'ם' , 'ן', 'ף', 'ץ'])
        else:
            return []

    def get_letters_inPhonetic(self):
        if self.typeAlphab == Alphabet_types.ARAMEEN:
            phonetics = ['אלף', 'בית', 'גימל', 'דלת', 'הא', 'ואו', 'זין', 'חית', 'טית', 'יוד', 'כף','כף', 'למד', 'מם', 'מם', 'נון','נון', 'סמך', 'עין', 'פא', 'פא', 'צדי', 'צדי', 'קוף', 'ריש', 'שין', 'תו']
            return {self.tabAlphab[i]: phonetics[i] for i in range(len(self.tabAlphab))}
        else:
            return []

# =============================
# GESTION DES CARACTERES A POIDS

# ------------------
# CLASSE pour créer des lettres avec leur poids
class LetterWithWeight:

    def __init__(self, char_letter, alphab=None):
        self.char_letter = char_letter # le caractère string
        self.alphab = alphab if alphab else Alphabet(Alphabet.GetTypeAlphab_fromChar(self.char_letter)) # l'alphabet correspondant

    def __repr__(self):
        return "CharWeighted:" + self.char_letter
    # ------------------
    # FONCTION retourne le poid du caractère entré : calcul selon les normes de l'alphabet araméen
    # @jit
    def getWeight(self, mode = 'RAGIL', submodes=None):
        """
        :param mode: mode de calcul du poids
        :param submodes: modes de calculs pour les modes utilisant des valeurs d'autres modes. Les autres sont terminaux
        - Modes terminaux : RAGIL, KATAN, KOLEL, RANGS
        - Modes non terminaux : MILOUYI, HAKADMI

        :return: poids du caractère
        """
        if submodes is None:
            submodes = []
        if 'RAGIL' not in submodes:
            submodes.append('RAGIL')

        if self.alphab.typeAlphab.name == "ARAMEEN":
            sofits = self.alphab.get_particular_letters()
            # pairs_sofits = {sofits[i]: self.alphab.tabAlphab[self.alphab.tabAlphab.index(sofits[i])-1] for i in range(len(sofits))}
            alphab_sans_sofits = sorted(list(set(self.alphab.tabAlphab).difference(set(sofits))))
            Res = 0
            if mode == 'RAGIL' or mode == 'KATAN' or mode == 'KOLEL':
                if self.char_letter in sofits:
                    Res = (sofits.index(self.char_letter)* 100) + 500
                else:
                    indLetter = alphab_sans_sofits.index(self.char_letter) + 1

                    Res = (indLetter%10 + indLetter//10)*pow(10, indLetter//10)
                if mode == 'KATAN' and Res > 10:
                    Res = Res // 10
                elif mode == 'KOLEL':
                    Res = Res + 1 # +1 pour le kolel car on compte l'ajout d'une lettre supplémentaire

            elif mode == 'RANGS':
                alphab_ranked = alphab_sans_sofits + sofits
                Res = alphab_ranked.index(self.char_letter) + 1

            elif mode == 'MILOUYI' or mode == 'NISTAR':
                Letters_complete = self.alphab.get_letters_inPhonetic()
                phonetic_word = Letters_complete[self.char_letter]
                if mode == 'NISTAR':
                    phonetic_word = phonetic_word[1:]
                # Res = sum([LetterWithWeight(letter).getWeight(mode = 'RAGIL') for letter in Letters_complete[self.char_letter]])
                Res = sum([LetterWithWeight(letter).getWeight(mode = submodes[0], submodes = submodes[1:]) for letter in phonetic_word])

            elif mode == 'HAKADMI': # IMPORTANT : le hakadmi actuel prend les valeurs régulières des sophites, rien n'étant précisé dans la doc de base
                # Res = sum([LetterWithWeight(self.alphab.tabAlphab[i]).getWeight(mode = 'RAGIL') for i in range(0, self.alphab.tabAlphab.index(self.char_letter)+1)])
                if self.char_letter in sofits:
                    Res = LetterWithWeight(self.alphab.tabAlphab[self.alphab.tabAlphab.index(self.char_letter)+1]).getWeight(mode = mode, submodes = submodes)
                else:
                    Res = sum([LetterWithWeight(alphab_sans_sofits[i]).getWeight(mode = submodes[0], submodes = submodes[1:]) for i in range(0, alphab_sans_sofits.index(self.char_letter)+1)])

            return Res
        return 0

# ------------------
# CLASSE pour créer des mots composés de lettres avec poids
class WordsWithWeight():
    def __init__(self, word=""):
        self.wordStr = word # mot en str
        self.word=[LetterWithWeight(letter) for letter in self.wordStr] # mot en lettre à poids

    def __repr__(self):
        return "WordWeighted:" + self.wordStr
    # ------------------
    # FONCTION retourne le poid du mot entré : somme des poids des caractères
    def getCalcGuem(self, mode = 'RAGIL', submodes = None):
        list_weights = [letter.getWeight(mode, submodes=submodes) for letter in self.word]
        return sum(list_weights)

    # ------------------
    @staticmethod
    def calculate_gematria_vectorized(word, mode='RAGIL', submodes=None):
        return np.cumsum([LetterWithWeight(letter, alphab_aram).getWeight(mode, submodes) for letter in word])
        # np.sum(np.array([LetterWithWeight(letter, alphab_aram).getWeight(mode, submodes) for letter in word]))

modes = ['RAGIL','KATAN', 'KOLEL', 'RANGS', 'MILOUYI','NISTAR', 'HAKADMI'] # 'RAGIL',
alphab_aram = Alphabet(Alphabet_types.ARAMEEN)
if __name__ == '__main__':
    WordsWithWeight_test = {"word_'a'" : WordsWithWeight("א"),
                            "word_'al'": WordsWithWeight("אל"),
                            "word_'an'" : WordsWithWeight("אך"),
                            "word_'bt'": WordsWithWeight("בת"),
                            "word_unknown": WordsWithWeight('ךאבםג'),
                            "word_all" : WordsWithWeight("אבגדהוזחטיכךלמםנןסעפףצץקרשת")}

    for word in WordsWithWeight_test:
        for mode in modes: # , 'MILOUYI'
            if mode == 'MILOUYI' or mode == 'HAKADMI' or mode == 'NISTAR':
                for submode in modes[:4]:
                    print(WordsWithWeight_test[word].wordStr, ", mode = " ,mode, " , submode = ", submode," : ", WordsWithWeight_test[word].getCalcGuem(mode = mode, submodes=[submode]))
            else:
                print(WordsWithWeight_test[word].wordStr, ", mode = " ,mode, " : ", WordsWithWeight_test[word].getCalcGuem(mode = mode)) # , submodes=['RANGS']
        print('\n')
