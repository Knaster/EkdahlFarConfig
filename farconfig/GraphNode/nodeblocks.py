from customnode import CustomBaseNode

class NodeBlockChild:
    def __init__(self, node, rank, parentNode):
        self.node = node
        self.rank = rank
        self.parentNode = parentNode

class NodeBlock:
    def __init__(self):
        self.childNodes = []
        self.childBlocks = []
        self.parentBlock = None
        self.parentNode = []

    def addBlock(self, parentBlock, parentNode):
        newBlock = NodeBlock()
        newBlock.parentBlock = parentBlock
        newBlock.parentNode.append(parentNode)
        self.childBlocks.append(newBlock)
        return newBlock

    def addNode(self, node:CustomBaseNode, rank:int, parentNode:CustomBaseNode):
        for lookNode in self.childNodes:
            if lookNode.node == node:
                return
        node = NodeBlockChild(node, rank, parentNode)
        self.childNodes.append(node)

    def inAncestors(self, node:CustomBaseNode):
        if node in self.parentNode:
            return True
        for parent in self.parentNode:
            if hasattr(parent, "block"):
                if parent.block.inAncestors(node):
                    return True
        return False

    def processNode(self, node:CustomBaseNode, parentNode:CustomBaseNode, rank:int, block = None):
        # If node already exists in block, makes sure it is as far back in the ranks as needed by the furthest down node
        if hasattr(node, "block"):
            node.block.parentNode.append(parentNode)
            for child in node.block.childNodes:
                if child.node == node:
                    if child.rank < rank:
                        child.rank = rank
                        #Once we've changed this childs rank we have to go through the nodes it connects to and make sure they do not collide
                        for outPort in child.node.output_ports():
                            for connectedNodePort in outPort.connected_ports():
                                if (connectedNodePort.model.node.block is not None):
                                    for findMe in connectedNodePort.model.node.block.childNodes:
                                        if findMe.node == connectedNodePort.model.node:
                                            if (findMe.rank <= child.rank):
                                                findMe.rank = child.rank + 1
                                            break

            return
        if block is None:
            block = self.addBlock(self, parentNode)
        node.block = block
        block.addNode(node, rank, parentNode)

        #For each output port, add any output nodes that does not already exist to 'nodes'
        nodes = []
        for outPort in node.output_ports():
            for connectPort in outPort.connected_ports():
                if (connectPort.model.node not in nodes):
                    nodes.append(connectPort.model.node)

        #If we only have one node, its a good chance we are creating a block
        if (len(nodes) == 1):
            #Check that the input ports of the next node are all connected to the previous node
            #Or it's ancestors
            allThis = True
            for inPort in nodes[0].input_ports():
                for connectPort in inPort.connected_ports():
                    if (connectPort.model.node != node) and (not block.inAncestors(connectPort.model.node)):
                        allThis = False
                        break
                if (not allThis): break
            if (allThis):
                block.processNode(nodes[0], node, rank + 1, block)
            else:
                self.processNode(nodes[0], node, rank + 1, None)
        else:
            for nextNode in nodes:
                self.processNode(nextNode, node, rank + 1, None)

class BaseBlock(NodeBlock):
    def __init__(self):
        super().__init__()

    def processRank(self, allRanks):
        for node in allRanks[0]:
            self.processNode(node, None, 0, None)
        self.pushBlocksToEnd()
        pass

    def pushBlocksToEnd(self):
        maxRank = 0
        for block in self.childBlocks:
            #if block.childNodes[len(block.childNodes)]
            if (len(block.childBlocks) == 0):
                endRank = -1
                for outPort in block.childNodes[len(block.childNodes) - 1].node.output_ports():
                    for connectedNodePort in outPort.connected_ports():
                        if (endRank > connectedNodePort.model.node.depthLevel) or (endRank == -1):
                            endRank = connectedNodePort.model.node.depthLevel
                            if (maxRank < endRank): maxRank = endRank
                if ((endRank - 2) > block.childNodes[len(block.childNodes) - 1].rank):
                    pushBy = endRank - 1 - block.childNodes[len(block.childNodes) - 1].rank
                    for child in block.childNodes:
                        child.rank += pushBy
        self.maxRank = maxRank

class BlockGridItem:
    def __init__(self, block, index):
        self.block = block
        self.index = index
        self.length = len(block.childNodes)
        self.blockNode = block.childNodes[index]

class BlockGrid():
    def __init__(self, base:BaseBlock = None, rows = 0, columns = 0):
        self.baseBlock = base
        self.grid = []
        self.lastColumn = 0
        if (base is not None): self.maxRank = base.maxRank

        if (base != None):
            rown = 0
            for block in self.baseBlock.childBlocks:
                block:NodeBlock = block
                self.grid.append([])
                row = self.grid[rown]
                for i in range(0, block.childNodes[0].rank):
                    row.append(None)
                coln = 0
                for child in block.childNodes:
                    gridItem = BlockGridItem(block, coln)
                    gridItem.blockNode.node.gridItem = gridItem
                    row.append(gridItem)
                    if self.lastColumn < (coln + len(block.childNodes)): self.lastColumn = coln
                    coln += 1
                while(len(row) < self.maxRank + 1): row.append(None)
                rown += 1
            self.arrangeFromLast()

        elif (rows != 0) and (columns != 0):
            self.grid = self.createGrid(rows, columns)

    def isNodeOnGrid(self, node):
        found = False
        for r in self.grid:
            for c in r:
                if c is not None:
                    if c.blockNode.node == node:
                        found = True
                        break
            if found: break
        return found

    def putBlockOnGrid(self, insertRow, block:NodeBlock, fromNode:CustomBaseNode, rowIncrease = True) -> (bool, int):
        start = 0
        if (fromNode is not None):
            if self.isNodeOnGrid(fromNode): return True, insertRow

            for blockNode in block.childNodes:
                if (blockNode.node == fromNode):
                    start = blockNode.rank
                    break

        if insertRow > len(self.grid):
            return False, insertRow
        thisRow = self.grid[insertRow]
        if (start + len(block.childNodes)) > len(thisRow):
            return False, insertRow
        for i in range(start, start + len(block.childNodes)):
            if (thisRow[i] != None):
                if not rowIncrease: return False, insertRow
                success, insertRow = self.putBlockOnGrid(insertRow + 1, block, fromNode)
                return success, insertRow

        index = 0
        for i in range(start, start + len(block.childNodes)):
            thisRow[i] = BlockGridItem(block, index)
            index += 1
        return True, insertRow

    def arrangeFromNode(self, block, node, newGrid, insertRow) -> int:
        #children = 0
        for input in node.input_ports():
            for connectedTo in input.connected_ports():
                insertRow = self.arrangeFromNode(connectedTo.model.node.block, connectedTo.model.node, newGrid, insertRow)
                #check if child exists previously in grid before inserting
                success, insertRow = newGrid.putBlockOnGrid(insertRow, connectedTo.model.node.block, connectedTo.model.node)
                if not success:
                    pass
        return insertRow

        #nodeRow = (insertRow - startRow) / 2
        #if (not newGrid.putBlockOnGrid(nodeRow, block, node)):
        #    pass

    def insertWithSpread(self, block, node, newGrid, wantedRow, spread):
        if spread == 0:
            success, row = newGrid.putBlockOnGrid(int(wantedRow), block, node, False)
            if success: return True
            spread += 1

        if (wantedRow > 0):
            success, row = newGrid.putBlockOnGrid(int(wantedRow - spread), block, node, False)
            if success:
                return True
        success, row = newGrid.putBlockOnGrid(int(wantedRow + spread), block, node, False)
        if not success:
            spread += 1
            return self.insertWithSpread(block, node, newGrid, wantedRow, spread)
        return True

    def arrangeFromLast(self):
        insertRow = 0
        startRow = 0
        newGrid = BlockGrid(rows = self.maxRank + 1, columns = len(self.grid))
        rank = self.maxRank
        for i in reversed(range(0, rank + 1)):
            for row in self.grid:
                if (row[i] is not None):
                    startRow = insertRow
                    node:CustomBaseNode = row[i].blockNode.node
                    insertRow = self.arrangeFromNode(row[i].block, node, newGrid, insertRow)
                    if not self.insertWithSpread(row[i].block, node, newGrid, (startRow + insertRow) / 2, 0):
                        pass

        self.grid = newGrid.grid

    def createGrid(self, rows, columns):
        gr = []
        for c in range(0, columns):
            ln = []
            for r in range(0, rows):
                ln.append(None)
            gr.append(ln)
        return gr