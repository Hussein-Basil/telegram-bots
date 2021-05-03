class Key:
    def __init__(self,name,parent_key,keyboards):
        self.name = name
        self.parent_keyboard = keyboards[parent_key]
        self.row_index, self.col_index = self.find(self.name,self.parent_keyboard)
        if self.row_index == None:
            self.parent_keyboard.insert(0,[self.name])
        
    def find(self,target,keyboard):
        for row in self.parent_keyboard:
            if target in row:
                row_index = self.parent_keyboard.index(row)
                col_index = row.index(target)
                return row_index, col_index
        return None,None

    def move(self, direction):
        if direction == 'up':
            if self.row_index==0 and len(self.parent_keyboard[self.row_index])==1:
                self.parent_keyboard.append(self.parent_keyboard.pop(0))
                self.row_index = len(self.parent_keyboard) - 1
                self.col_index = 0

            elif len(self.parent_keyboard[self.row_index])>1:
                self.parent_keyboard.insert(self.row_index,[self.parent_keyboard[self.row_index].pop(self.col_index)])
                self.row_index -= 1
                self.col_index = 0
            
            elif len(self.parent_keyboard[self.row_index])==1:
                self.parent_keyboard[self.row_index-1].insert(0,self.parent_keyboard.pop(self.row_index)[0])
                self.row_index -= 1
                self.col_index = 0
                
        elif direction == 'down':

            if self.row_index==len(self.parent_keyboard)-1 and len(self.parent_keyboard[self.row_index])==1:
                self.parent_keyboard.insert(0,self.parent_keyboard.pop())
                self.row_index,self.col_index = 0,0
            
            elif len(self.parent_keyboard[self.row_index])==1:
                self.parent_keyboard[self.row_index+1].insert(0,self.parent_keyboard.pop(self.row_index)[0])
                self.row_index,self.col_index = self.row_index,0
            
            elif len(self.parent_keyboard[self.row_index])>1:
                self.parent_keyboard.insert(self.row_index+1,[self.parent_keyboard[self.row_index].pop(self.col_index)])
                self.row_index += 1
                self.col_index = 0
        
        elif direction == 'left':
            self.remove_column()
            if self.col_index == 0:
                self.col_index = len(self.parent_keyboard[self.row_index])
                self.add_column()

            else:
                self.col_index -= 1
                self.add_column()
        
        elif direction == 'right':
            self.remove_column()
            if self.col_index == len(self.parent_keyboard[self.row_index]):
                self.col_index = 0
                self.add_column()

            else:
                self.col_index += 1
                self.add_column()

    def remove(self):
        self.parent_keyboard[self.row_index].pop(self.col_index)

    def remove_column(self):
        self.parent_keyboard[self.row_index].pop(self.col_index)

    def add_row(self):
        self.parent_keyboard.insert(self.row_index, [self.name])

    def add_column(self):
        self.parent_keyboard[self.row_index].insert(self.col_index, self.name)