import random

class node:
    def __init__(self, location:tuple[int,int]) -> None:

        '''node of a graph, connects to other nodes thru edges obv.
        truroom is the like full functioning room for the node which is just like the location.
        i feel like it could come in handy maybe but idk just a thought.'''

        self.edges,self.secret_edges,self.connect_nodes,self.secret_connect_nodes,self.truroom=[],[],[],[],None
        self.x,self.y=location

    def connecting_nodes(self)->dict[any, str]:

        '''returns a dict of the conecting node and the direction. 
         directions-> north east west south passage(passage number)
          caz SECRET PASSAGES . anyways hope u can read this code now, got ridd of the list and dict comp'''
        
        dif_x_or_y=lambda x: ['north','south'] if self.y != x.y else ['east','west']
        dir_to_node=lambda x: dif_x_or_y(x)[0] if  x.y > self.y or x.x > self.x else dif_x_or_y(x)[1]
        connecting_nodes_dict={}
        for n in self.connect_nodes:
             connecting_nodes_dict[n]=dir_to_node(n)
        for s_n in self.secret_connect_nodes:
            connecting_nodes_dict.update({s_n:f'passageway {self.secret_connect_nodes.index(s_n)+1}'})
        return connecting_nodes_dict
    def delete(self) -> None:
        [e.delete() for e in self.edges]
        [e.delete() for e in self.secret_edges]
        
    def __str__(self) -> str:
        return f'room({self.x, self.y})'
    
class edge:
    def __init__(self, node1:node, node2:node, 
                    is_passage:bool=False) -> None:
        """an edge """
        
        self.node1, self.node2, self.is_passage = node1, node2, is_passage
        self.node1.edges.append(self)
        self.node2.edges.append(self)
        if self.is_passage:
            self.node1.connect_nodes.append(self.node2)
            self.node2.connect_nodes.append(self.node1)
        else:
            self.node1.secret_connect_nodes.append(self.node2)
            self.node2.secret_connect_nodes.append(self.node1)

    def delete(self) -> None:
        if self.is_passage:
            self.node1.secret_connect_nodes.remove(self.node2)
            self.node2.secret_connect_nodes.remove(self.node1)
            self.node1.secret_edges.remove(self)
            self.node2.secret_edges.remove(self)
        else:
            self.node1.connect_nodes.remove(self.node2)
            self.node2.connect_nodes.remove(self.node1)
            self.node1.edges.remove(self)
            self.node2.edges.remove(self)
        
    def __str__(self) -> str:
        return f'(edge({self.node1}, {self.node2}))' if not self.is_passage else f'(edge({self.n1}, {self.n2}, is_passage))'

class new_graph:    
    def __init__(self, size:tuple[int, int],
                    node_and_edge_deletion_chance:float=0.0,
                    passages_amount:int=10) -> None:
        """makes a graph obv
        idk randomisations and stuff"""
        
        self.x,self.y=size[0], size[1] 
        self.nodes=[node((x, y)) for x in range(self.x) for y in range(self.y)] #makes a grid of nodes based on the dungeon size
        self.edges=[]

        
        for n in self.nodes: 
            if random.random() < node_and_edge_deletion_chance:
                self.nodes.pop(self.nodes.index(n)) 
                #randomly deletes node based on the chances of naedc a very good acrynm, this is why im probs gonna fail english



        for n in self.nodes:
                for n_ in self.nodes:
                        if (n.x==n_.x and n.y==n_.y+1) or (n.y==n_.y and n.x==n_.x+1):  
                            self.edges.append(edge(n,n_)) 
                            #connects all of the nodes in a gridlike pattern (unless they dont exist)
        
        for e in self.edges:
            if random.random() < node_and_edge_deletion_chance:
                e.delete()
                self.edges.pop(self.edges.index(e)) 
                #randomly deletes edges based on naedc a very good acronym

        for n in self.nodes:
            if len(n.edges)==0:
                self.nodes.pop(self.nodes.index(n)) 
                #deletes nodes that dont have any edges
        
        for i in range(passages_amount):
            random_node1=self.nodes[random.randint(0,len(self.nodes)-1)]
            random_node2=self.nodes[random.randint(0,len(self.nodes)-1)]
            self.edges.append(edge(random_node1, random_node2, True))
            #this one looks like super confusing but it just randomly makes secret passeges

    def save(self, file:str):
            """make sure the file is raw btws"""
            #i hate annotating
            nodelocations, edgelocations=[], []

            for n in self.nodes:
                nodelocations.append(f'{n.x}|{n.y}')


            for e in self.edges:
                n1,n2=f'{e.node1.x}|{e.node1.y}',f'{e.node2.x}|{e.node2.y}'
                edgelocations.append(f'{nodelocations.index(n1)}j{nodelocations.index(n2)}j{e.is_passage}')

            ns='i'.join(nodelocations)
            es='i'.join(edgelocations)
            inf='thisismakingmeloosemywilltolive(:'.join([ns,es])

            with open(file, 'w') as outp:
                outp.write(inf)
            outp.close()

class load_graph(new_graph):
    def __init__(self, file):
        with open(file, 'r') as fl:
            info=fl.read()
        nodes, edges = info.split('thisismakingmeloosemywilltolive(:')[0], info.split('thisismakingmeloosemywilltolive(:')[1]
        nodes, edges = nodes.split('i'), edges.split('i')
        #all of this is just decoding the batshit crazy formating i used to save the info.
        nodes=[node((int(i.split('|')[0]), int(i.split('|')[1]))) for i in nodes]
        edges=[edge(nodes[int(i.split('j')[0])],nodes[int(i.split('j')[1])], i.split('j')[2]) for i in edges]
        self.nodes,self.edges=nodes,edges



