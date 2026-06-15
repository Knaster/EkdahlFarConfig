from nodeblocks import BaseBlock, BlockGrid
from NodeGraphQt.nodes.port_node import PortInputNode, PortOutputNode
from NodeGraphQt import Port
from customnode import CustomBaseNode

class NodeOrganizer():
    def __init__(self, graph):
        self.graph = graph
        self.rankingList = None
        self.hideImplicits = False
        self.hideAdvanced = False
        self.baseBlock = BaseBlock()
        self.blockGrid = None
        self.maxDepth = 0
        self.rankingList = []

    def clearData(self):
        self.rankingList = None
        self.baseBlock.childBlocks.clear()
        self.baseBlock.childNodes.clear()
        self.baseBlock.parentNode.clear()
        self.baseBlock.maxRank = 0
        self.blockGrid = None
        self.maxDepth = 0
        if (self.rankingList is not None):
            self.rankingList.clear()

    def rankHorizontalDepth(self):
        roots = []
        for node in self.graph.all_nodes():
            #("nodes.midi" in node.type_) or ("CB" in node.NODE_NAME) or ("Variables" in node.NODE_NAME)
            try:
                if not hasattr(node, 'source'):
                    node.source = True
                    node.depthLevel = 0

                if (node.source) or (isinstance(node, PortInputNode)) or (isinstance(node, PortOutputNode)):
                    roots.append(node)
                else:
                    pass
            except Exception as e:
                pass

        # Calculate max depth level of each item as well as max child nodes per item and overall max depth level
        depthLevel = 0
        maxLevel = 0
        for node in roots:
            maxChildren = 0
            maxLevel, maxChildren = self.rankHorizontalDepthIter(node, depthLevel, maxLevel, maxChildren, None)
            node.maxChildren = maxChildren

        self.maxDepth = maxLevel

    def rankHorizontalDepthIter(self, node, depthLevel, maxLevel, maxChildren, sourceObject):
        if (maxLevel < depthLevel): maxLevel = depthLevel
        if (node.depthLevel < depthLevel):
            node.depthLevel = depthLevel
        node.verticalLevel = 0
        node.verticalChildren = 0
        for sourcePort in node.connected_output_nodes():
            sourcePort:Port = sourcePort
            for destPort in sourcePort.connected_ports():
                node.verticalChildren += 1
                maxLevel, maxChildren = self.rankHorizontalDepthIter(destPort.node(), depthLevel + 1, maxLevel, maxChildren, node)
            pass

        if (maxChildren < node.verticalChildren): maxChildren = node.verticalChildren
        return maxLevel, maxChildren

    def hideObjectsWithAllImplicitChildren(self):
        for depth in reversed(range(0, self.maxDepth)):
            nodesAtDepth = [obj for obj in self.graph.all_nodes() if obj.depthLevel == depth]
            for node in nodesAtDepth:
                node:CustomBaseNode = node
                showNode = False
                if (len(node.connected_output_nodes()) > 0):
                    for outPortConnections in node.connected_output_nodes():
                        outPortConnections:Port = outPortConnections
                        for connection in outPortConnections.connected_ports():
                            showNode = (showNode or not(connection.model.node.implicit and self.hideImplicits))
                    if (showNode or node.source or ((("hardware" in node.type_) or ("Variables" in node.NODE_NAME)) and not node.implicit)):
                        node.allImplicitChildren = False
                        if (hasattr(node, "show")):
                            node.show()
                    else:
                        node.allImplicitChildren = True
                        node.hide()

    def buildHorizontalTree(self, horizontalSpacing = 500, verticalSpacing = 200):
        # Hide all implicit objects if so chosen
        for node in self.graph.all_nodes():
            node.set_pos(-1500,0)
            if (isinstance(node, CustomBaseNode)):
                #node.sourceObjects.clear()
                if ((node.implicit or node.allImplicitChildren) and self.hideImplicits):
                    node.hide()
                else:
                    node.show()

        self.rankHorizontalDepth()
        if (self.maxDepth == 0): return

        if (self.hideImplicits): self.hideObjectsWithAllImplicitChildren()

        rankingList = []
        self.rankVerticalByConnections(self.maxDepth, rankingList)
        rankingList.reverse()

        self.rankingList = rankingList
        self.baseBlock.processRank(self.rankingList)
        self.blockGrid = BlockGrid(self.baseBlock)

        self.drawFromBlocks()
        #self.rankVerticalPreference(self.rankingList)
        #self.drawFromRankingList(self.rankingList)

    def drawFromBlocks(self, horizontalSpacing = 500, verticalSpacing = 200):
        y = 0
        for row in self.blockGrid.grid:
            for column in row:
                if (column is not None):
                    child = column.blockNode
                    node = child.node
                    node.set_pos(child.rank * horizontalSpacing - (node.view.boundingRect().width() / 2),
                                 y * verticalSpacing - (node.view.boundingRect().height() / 2))
            y += 1


    def drawFromRankingList(self, rankingList = None, horizontalSpacing = 500, verticalSpacing = 200):
        if (rankingList is None): rankingList = self.rankingList
        for depth in rankingList:
            y = 0
            for node in depth:
                if (node is not None):
                    node.set_pos(node.depthLevel * horizontalSpacing - (node.view.boundingRect().width() / 2),
                                y * verticalSpacing - (node.view.boundingRect().height() / 2))
                y += 1

    def rankVerticalPreferenceUntilDone(self, maxIterations = 20):
        iter = 0
        while ((iter < maxIterations)):
            self.rankVerticalPreference(self.rankingList)
            iter += 1
    '''
    Ranks each object in the grid vertically depending on the connections it needs to make to other objects.
    Starts at the end destination depth (right-most as of this writing) and moves all objects per row
    '''
    def rankVerticalPreference(self, rankingList = None, noInserts = True, exploded = False):
        if (rankingList is None): rankingList = self.rankingList
        for depth in reversed(range(0, self.maxDepth + 1)):
            anyMoved, explode = self.rankVerticalPreferenceIter(depth, rankingList, noInserts=noInserts)
            if ((explode > 20) and (not exploded)):
                self.explodeRanks(rankingList)
                self.rankVerticalPreference(rankingList, noInserts=noInserts, exploded=True)
                return True
            pass
        return True

    def explodeRanks(self, rankingList):
        i = 0
        for depth in rankingList:
            while (i < len(depth)):
                depth.insert(i, None)
                i += 2
            depth.insert(i, None)
            pass

    def findVerticalPositionOfObject(self, node, rankingList):
        for depth in rankingList:
            verticalPos = 0
            for posNode in depth:
                if posNode == node: return verticalPos
                verticalPos += 1
        return -1

    def granulateByPortPosition(self, node, port, direction):
        node:CustomBaseNode = node
        if (direction == "out"):
            index = node.input_ports().index(port)
            length = len(node.input_ports())
        else:
            index = node.output_ports().index(port)
            length = len(node.output_ports())

        weight = 1 / length
        granulation = -0.5 + (weight / 2) + weight * index
        return granulation

    # Calculates the preferred Y position of a node by averaging the Y positions of all connected nodes
    # Adds in the position of the various ports as fractions to get a -0.5 - 0 - +0.5 as top, center or bottom leaning
    def calculatePreferredY(self, depth, rank, rankingList):
        preferredY = []
        for node in rank:
            if (node is not None):
                node:CustomBaseNode = node
                prefY = 0
                objects =0
                if (node.name() == "Equation1 1"):
                    pass
                for connectedPorts in node.connected_output_nodes():
                    connectedPorts:Port = connectedPorts
                    for connection in connectedPorts.connected_ports():
                        if (connection.model.node._view.isVisible()):
                            prefY += self.findVerticalPositionOfObject(connection.model.node, rankingList)
                            prefY += self.granulateByPortPosition(connection.model.node, connection, "out")
                            objects += 1
                for connectedPorts in node.connected_input_nodes():
                    connectedPorts:Port = connectedPorts
                    for connection in connectedPorts.connected_ports():
                        if (connection.model.node._view.isVisible()):
                            prefY += self.findVerticalPositionOfObject(connection.model.node, rankingList)
                            prefY += self.granulateByPortPosition(connection.model.node, connection,"in")
                            objects += 1
                    pass
                if (objects != 0):
                    prefY = (prefY / (objects)) * 0.99
                else:
                    prefY = None
                preferredY.append(prefY)
            else:
                preferredY.append(None)
        return preferredY

    def swapPositions(self, rank, preferredY, pos, destinationPos):
        savedItem = rank[destinationPos]
        savedYPreference = preferredY[destinationPos]
        rank[destinationPos] = rank[pos]
        preferredY[destinationPos] = preferredY[pos]
        rank[pos] = savedItem
        preferredY[pos] = savedYPreference

    def insertBlankRank(self, rankingList, preferredY):
        for depth in reversed(range(0, self.maxDepth + 1)):
            rankingList[depth].insert(0, None)
        preferredY.insert(0, None)
        for yPos in range(1, len(preferredY)):
            if (preferredY[yPos] is not None): preferredY[yPos] += 1

    #def findClosestNeighbor(self, space, ranksAtDepth, ):

    def insertIfHasOpeningOrIsShort(self, destinationPos, currentPos, rank, preferredY):
        moved = False
        if len(rank) <= destinationPos:
            while (len(rank) < destinationPos):
                rank.append(None)
                preferredY.append(None)
            rank.append(rank[currentPos])
            preferredY.append(preferredY[currentPos])
            rank[currentPos] = None
            preferredY[currentPos] = None
            moved = True
        elif rank[destinationPos] == None:
            self.swapPositions(rank, preferredY, currentPos, destinationPos)
            moved = True
        return moved

    def findClosestEmptyNeighbor(self, space, rank):
        up = down = space
        change = True
        while (change):
            if (rank[up] is None): return up
            if (rank[down] is None): return down
            change = False
            if (up < len(rank) - 1): up += 1; change = True
            if (down > 0): down -=1; change = True
        return None

    def calculateDeviationFromSpace(self, itemPos, space, preferredY):
        return abs(space - preferredY[itemPos])

    def rankVerticalPreferenceIter(self, depth, rankingList, maxIterations = 20, noInserts = True):
        explode = 0
        rank = rankingList[depth]
        preferredY = self.calculatePreferredY(depth, rank, rankingList)

        moved = True
        anyMoved = False
        iterations = 0
        while(moved):
            moved = False
            for pos in range(0, len(rank)):
                if ((rank[pos] is not None) and (preferredY[pos] is not None)):
                    destinationPos = round(preferredY[pos])

                    # If we have an object that wants to be put in the negative zone we have to push down all objects in every rank,
                    # do the same with the current preferredY and then increase each preferredY with 1 in order to reflect the new order
                    if (destinationPos == -1):
                        self.insertBlankRank(rankingList, preferredY)
                        destinationPos += 1
                        break
                    elif (destinationPos < -1):
                        raise("Whoa boy")

                    # If our current position is indeed our preferred position, do nothing. Otherwise go forth!
                    if (pos != destinationPos):
                        #The physical position in the ranks needs to be rounded (not truncated) in order to get the port position skew in there
                        destinationPos = round(preferredY[pos])
                        '''
                        #If the preferred position is beyond the current ranks, increase them and move the item to last
                        if len(rank) <= destinationPos:
                            while(len(rank) < destinationPos):
                                rank.append(None)
                                preferredY.append(None)
                            rank.append(rank[pos])
                            preferredY.append(preferredY[pos])
                            rank[pos] = None
                            preferredY[pos] = None
                            moved = True
                        else:
                            #If the preferred position is empty, we can just move our object there and the old spots will have the empties instead
                            if rank[destinationPos] == None:
                                self.swapPositions(rank, preferredY, pos, destinationPos)
                                moved = True
                            else:
                        '''
                        if (self.insertIfHasOpeningOrIsShort(destinationPos, pos, rank, preferredY)):
                            moved = True
                        else:
                            found = False
                            while((destinationPos != pos) and (not found)):
                                #If the position is occupied, calculate how far away the object that wants to move in is currently from its preferred
                                #position. Calculate how far away the current inhabitant is from its preferred position
                                if (preferredY[destinationPos] is None):
                                    break
                                occupyingItemPPos = round(preferredY[destinationPos])
                                if (destinationPos == occupyingItemPPos):
                                    neighbor = self.findClosestEmptyNeighbor(destinationPos, rank)
                                    if (neighbor is not None):
                                        moveItemDeviation = self.calculateDeviationFromSpace(pos, neighbor, preferredY)
                                        occupyingItemDeviation = self.calculateDeviationFromSpace(destinationPos, neighbor, preferredY)
                                        if (moveItemDeviation < occupyingItemDeviation):
                                            self.swapPositions(rank, preferredY, pos, neighbor)
                                            #self.swapPositions(rank, preferredY, destinationPos, pos)
                                        else:
                                            self.swapPositions(rank, preferredY, destinationPos, neighbor)
                                            self.swapPositions(rank, preferredY, pos, destinationPos)
                                        moved = True
                                        break
                                    else:
                                        #i think this means that all ranks are full which probably means we should explode the ranks, aka insert empty
                                        #rows everywhere
                                        explode += 1
                                        break
                                else:
                                    if (self.insertIfHasOpeningOrIsShort(occupyingItemPPos, destinationPos, rank, preferredY)):
                                        self.swapPositions(rank, preferredY, pos, destinationPos)
                                        moved = True
                                        found = True
                                    else:
                                        #If the position is occupied, calculate how far away the object that wants to move in is currently from its preferred
                                        #position, also calculate how far away the current inhabitant will be from its preferred position if they were to trade places
                                        currentItemsDeviation = abs(pos - preferredY[pos])
                                        if preferredY[destinationPos] is not None:
                                            destinationItemsDeviation = abs(destinationPos - preferredY[destinationPos])
                                        else:
                                            destinationItemsDeviation = 0
                                        #If the new objects current position is further away from its preferred position than the current inhabitant will be if
                                        #places were to be traded, then there is a net gain and places will be traded
                                        if ((((currentItemsDeviation) > destinationItemsDeviation)) or (preferredY[destinationPos] is None)):
                                            #Since presumably both want to occupy the same space, check what neighbors are empty, then calculate which would
                                            #suffer most from being moved to the neighboring space, then move the least sufferer to the neighbor and most sufferer
                                            #to the space in question

                                            self.swapPositions(rank, preferredY, pos, destinationPos)
                                            moved = True
                                            found = True
                                            break
                                        if (destinationPos > pos): destinationPos -= 1
                                        else: destinationPos += 1

                            if (not found) and (not noInserts):
                                currentItemsDeviation = abs(pos - preferredY[pos])
                                destinationPos = round(preferredY[pos])

                                maxDistanceUp = 0
                                minDistanceUp = 99
                                for index in range(0, destinationPos - 1):
                                    if preferredY[index] is not None:
                                        if (preferredY[index] != -99):
                                            distance = abs(preferredY[index] - index - 1)
                                            if (distance > maxDistanceUp): maxDistanceUp = distance
                                            if (distance < minDistanceUp): minDistanceUp = distance
                                maxDistanceDown = 0
                                minDistanceDown = 99
                                for index in range(destinationPos + 1, len(preferredY) - 1):
                                    if preferredY[index] is not None:
                                        if (preferredY[index] != -99):
                                            distance = abs(preferredY[index] - index + 1)
                                            if (distance > maxDistanceDown): maxDistanceDown = distance
                                            if (distance < minDistanceDown): minDistanceDown = distance

                                upPossible = False
                                if (currentItemsDeviation > maxDistanceUp): upPossible = True
                                downPossible = False
                                if (currentItemsDeviation > maxDistanceDown): downPossible = True
                                if (upPossible or downPossible):
                                    if (upPossible and downPossible):
                                        if (minDistanceUp < minDistanceDown): goDir = "up"
                                        else: goDir = "down"
                                    elif (upPossible): goDir = "up"
                                    else: goDir = "down"

                                    if (goDir == "up"):
                                        if rank[0] is not None:
                                            self.insertBlankRank(rankingList, preferredY)
                                        rank.remove(rank[0])
                                        preferredY.remove(preferredY[0])

                                    rank.insert(destinationPos, rank[pos])
                                    preferredY.insert(destinationPos, preferredY[pos])
                                    rank[pos + 1] = None
                                    preferredY[pos + 1] = None
                                    moved = True

                pos += 1
            if (moved): anyMoved = True
            iterations += 1
            if (iterations == maxIterations):
                #if (depth == 0 and ("Variables" in rank[9].NODE_NAME) and ("Engage") in rank[2].NODE_NAME):
                #    pass
                #else:
                break
        return anyMoved, explode

    def rankVerticalByConnections(self, depth, rankingList):
        if (depth < 0): return
        nodesAtDepth = [obj for obj in self.graph.all_nodes() if (obj.depthLevel == depth and obj._view.isVisible())]
        thisDepth = []
        rankingList.append(thisDepth)
        for node in nodesAtDepth:
            if (len(thisDepth) == 0):
                thisDepth.append(node)
            else:
                iter = 0
                for subNode in thisDepth:
                    if (node.verticalChildren > subNode.verticalChildren):
                        thisDepth.insert(iter, node)
                        break
                    iter += 1
                if (iter == len(thisDepth)):
                    thisDepth.append(node)
        #for node in thisDepth:
        self.rankVerticalByConnections(depth - 1, rankingList)
        pass
