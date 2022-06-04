def minmaxinterface(instance,gameState,depth,agentnum):
    maxvalues = []
    comparearray = []
    if gameState.isWin() or gameState.isLose():
        return instance.evaluationFunction(gameState)
    if depth > 0:
        if depth % agentnum == 0:
            NumberofAgent = 0
        else:
            NumberofAgent = agentnum -(depth % agentnum)

        legalactions = gameState.getLegalActions(NumberofAgent)
        for action in legalactions:
            successors = gameState.generateSuccessor(NumberofAgent,action)
            if NumberofAgent == 0:
                maxvalues.append((minmaxinterface(instance,successors,depth-1,agentnum),action))
                maxvalue = max(maxvalues)
                instance.value_max = maxvalue[0]
                instance.action1 = maxvalue[1]
            else:
                if isinstance(instance,MinimaxAgent):
                    comparearray.append((minmaxinterface(instance,successors,depth-1,agentnum),action))
                    minvalue = min(comparearray)
                    instance.value_min = minvalue[0]

                if isinstance(instance,ExpectimaxAgent):
                    comparearray.append((minmaxinterface(instance,successors,depth-1,agentnum),action))
                    avg = 0.0
                    for x in comparearray:
                        avg += comparearray[comparearray.index(x)][0]
                    avg/=len(comparearray)
                    instance.value_avg = avg
        if NumberofAgent == 0:
            return instance.value_max
        else:
            if isinstance(instance,MinimaxAgent):
                return instance.value_max
            else:
                return instance.value_min

    else:
        return instance.evaluationFunction(gameState)




