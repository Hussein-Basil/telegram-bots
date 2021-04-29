keyboards = {"Main Menu": [['Files'], ['Photos'], ['Voice Notes'], ['Back','Main Menu'], ['Button Editor']]}

class Key:
    def __init__(self,name,parent_key,keyboards):
        self.name = name
        self.parent_keyboard = keyboards[parent_key]
        self.row_index, self.col_index = self.find(self.name,self.parent_keyboard)
        self.is_found = (True if self.row_index else False)
        if not self.is_found:
            self.row_index,self.col_index = 0,0
            self.add_row()


    def find(self,target,keyboard):
        for row in self.parent_keyboard:
            if target in row:
                row_index = self.parent_keyboard.index(row)
                col_index = row.index(target)
                return row_index, col_index
        return None,None

    def move(self, direction):
        if direction == 'up':
            self.col_index = 0
            self.remove()

            if self.row_index==0:
                self.row_index = (0 if len(self.parent_keyboard[0])>1 else len(self.parent_keyboard))
                self.add_row()
                
            else:
                self.row_index -= 1
                self.add_column()
                
        elif direction == 'down':
            self.col_index = 0
            self.remove()

            if self.row_index == len(self.parent_keyboard)-1:
                self.row_index = (0 if len(self.parent_keyboard[self.row_index])==1 else len(self.parent_keyboard))
                self.add_row()

            else:
                self.row_index +=1
                self.add_column()

        
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
        if [] in self.parent_keyboard: self.parent_keyboard.remove([])

    def remove_column(self):
        self.parent_keyboard[self.row_index].pop(self.col_index)

    def add_row(self):
        self.parent_keyboard.insert(self.row_index, [self.name])

    def add_column(self):
        self.parent_keyboard[self.row_index].insert(self.col_index, self.name)



print(keyboards['Main Menu'])

name = input('Enter Target Button : ')
k = Key(name,'Main Menu',keyboards)

while True:
    x = input("Enter Direction : ")
    if x=='up' or x=='down' or x=='left' or x=='right':
        k.move(x)
        print(keyboards['Main Menu'])