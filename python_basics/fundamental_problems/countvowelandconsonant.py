def countVowConsonent(value:str) -> dict:
    vowel = ["a","e","i","o","u","A","E","I","O","U"]
    count_dict = {"Vowel":0,"Consonant":0}
    for i in value:
         if i in vowel:
             count_dict["Vowel"] = count_dict["Vowel"]+1
         else:
             count_dict["Consonant"] = count_dict["Consonant"] + 1

    return count_dict

print(countVowConsonent("Prince"))



