class BaseItem:
    def __init__(self, item):
        self.item = item
    
    def is_same(self, item):
        return self.item == item

class CheckableItem(BaseItem):
    def __init__(self, item):
        super().__init__(item)
        self._is_checked = False
    
    @property
    def is_checked(self):
        return self._is_checked
    
    @is_checked.setter
    def is_checked(self, flg):
        if not isinstance(flg, bool):
            raise TypeError('flg has to be bool type') 
        self._is_checked = flg
    
    def get_item(self):
        self.is_checked = True
        return self
