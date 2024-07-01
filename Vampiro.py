import itertools as it

class Vampiro:
    def __init__(self):
        pass
  

    def getColmillos(self, num_str):
    
        
        num_iter = it.permutations(num_str, len(num_str))
    
        
        for num_list in num_iter:
            
            v = ''.join(num_list)
            x, y = v[:int(len(v)/2)], v[int(len(v)/2):]
    
            
            if x[-1] == '0' and y[-1] == '0':
                continue
    
            
            if int(x) * int(y) == int(num_str):
                return x,y
        return False
    

    def esVampiro(self, m_int):
    
        
        n_str = str(m_int)
        
        if len(n_str) % 2 == 1:
            return False
    
        
        colmillos = self.getColmillos(n_str)
        if not colmillos:
            return False
        return True
  


