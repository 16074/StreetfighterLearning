naam = input("Wat is de naam van een vriend van u? ")
geslacht = input("Wat is het geslacht van die vriend? U kunt kiezen uit man, vrouw of anders. ")
if geslacht == "man":
    voornaamwoord = "Hij"
    lijdend = "hem"
elif geslacht == "vrouw":
    voornaamwoord = "Zij"
    lijdend = "haar"
elif geslacht == "anders":
    voornaamwoord = "die"
    lijdend = "hun"
activiteit = input("Wilt de vriend wandelen of lezen? ")
if activiteit == "wandelen":
    print(voornaamwoord + " gaat graag wandelen. Dat past echt bij " + lijdend)
elif activiteit == "lezen":
    print(voornaamwoord + " houdt van lezen. Dat past echt bij " + lijdend)