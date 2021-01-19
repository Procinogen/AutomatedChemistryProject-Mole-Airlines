from mendeleev import element
import json

#Subscripts
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

#The threshold value for getRatio
THRESHOLD = 0.05

#Function that returns the number of moles, rounded to three decimals
def getNumberOfMoles(chemicalSymbol, percentage):
    return percentage / round(element(chemicalSymbol).mass, 3) 

#Functions that provides a ratio for each of the elements relative to each other
def getRatio(elements):
    #Initialize an array that holds the number of moles per element
    moleNumbers = []
    for e in elements:
        #Add each element's number of moles into the array
        moleNumbers.append(elements[e])
    
    #Find the lowest value to divide by
    lowestValue = min(moleNumbers)
    #Make a new dictionary containing all the elements to use for the ratio
    ratio = elements
    
    #Iterate through the new dictionary to set each key as their ratio
    for e in ratio:
        quotient = elements[e] / lowestValue
        #Check to see if the difference between the rounded and the unrounded meets a certain theshold (Used to check if something should be rounded)
        difOne = round(quotient, 0) - quotient
        if (abs(difOne) < THRESHOLD):
            #print(ratio[e], difOne)
            ratio[e] = int(round(quotient, 0))
        else:
            ratio[e] = round(quotient, 3)
        #ratio[e] = round(quotient, 5)
    #Return the dictionarycs
    return (ratio, lowestValue)

#Function that returns the empirical formula
def getEmpiricalFormula(ratio):
    formula = ""
    for e in ratio:
        if(ratio[e] == 1):
            formula += e
        else:
            formula += e + str(ratio[e])
    return formula.translate(SUB)

def main():
    output = open("output.txt", 'w', encoding="utf8")
    calculations = open("calculations.txt", "w", encoding="utf8")

    #Read file
    with open('data.json', 'r') as datafile:
        dataloader = datafile.read()

    #Turn the json file into a readable format (dictionary)
    data = json.loads(dataloader)

    output.write("**Suggested empirical formulas with decimals will need to have their ratios multiplied by the appropriate amount**\n")

    #Get all the used elements
    usedElements = data["Used Elements"]

    #Iterate through the compounds via their assigned number
    #This is sorted via the compound's number, not the associated passenger's number
    for i in range(1, len(data)):
        #Turn the compund number into a reusable string that can be used to parse the JSON file
        compoundNumber = str(i)
        output.write(f"\n{compoundNumber}:")
        calculations.write(f"\n{compoundNumber}:\n")
        output.write(f"\n\tLocation: {data[compoundNumber]['Location']}")
        
        #Initialize dictionary to hold the number of moles in the compound
        compoundsMoles = {}
        moleNumCalc = {}

        #Iterate through the given elements, these need to be in order in the JSON
        for e in usedElements:
            currentElement = data[compoundNumber][e]
            #Check to see if the element is actually present
            if currentElement != "N/A":
                moleNum = getNumberOfMoles(e, currentElement)
                output.write(f"\n\t{e}: {moleNum}")
                compoundsMoles[e] = moleNum
                moleNumCalc[e] = moleNum

                #Writing to the calculations for the "show your work"
                #roundedMoles = round(moleNum, 3)
                #tempString += f"{e}:\n{currentElement}g ÷ {round(element(e).mass, 3)}g/mol = {roundedMoles}mol\n\n"

        ratio = getRatio(compoundsMoles)
        output.write(f"\n\tRatio: {ratio[0]}")
        output.write(f"\n\tSuggested Empirical Formula: {getEmpiricalFormula(ratio[0])}")
        #calculations.write(tempString)

        for e in compoundsMoles:
            moleCount = moleNumCalc[e]
            rounded = round(moleCount, 3)
            calculatedRatio = ratio[0][e]
            calculations.write(f"{e}:\n{data[compoundNumber][e]}g ÷ {round(element(e).mass, 3)}g/mol = {rounded}mol\n{rounded} ÷ {round(ratio[1], 3)} ")
            if type(calculatedRatio) == int and calculatedRatio != 1:
                calculations.write(f"≈ {ratio[0][e]}\n")
            else:
                calculations.write(f"= {ratio[0][e]}\n")

    output.close()
    calculations.close()


if __name__ == "__main__":
    main()
