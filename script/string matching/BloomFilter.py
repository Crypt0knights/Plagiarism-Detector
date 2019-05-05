from bitarray import *

class BloomFilter:
    def __init__(self, size):
        self.size = size
        self.filter_one = bitarray(size)
        self.filter_two = bitarray(size)
        self.filter_one.setall(0)
        self.filter_two.setall(0)
    
    def set_bit(self, filter_num, indexes):
        for index in indexes:
            if filter_num == 1:
                self.filter_one[int(index)] = 1
            else:
                self.filter_two[int(index)] = 1
    
    def look_up(self, filter_num, indexes):
        for index in indexes:
            if filter_num == 1 and not self.filter_one[int(index)]:
                return False
            if filter_num == 2 and not self.filter_two[int(index)]:
                return False
        return True

    def display(self):
        print(self.filter_one)
        print(self.filter_two)

if __name__ == "__main__":
    bf = BloomFilter(20)
    bf.display()
    bf.set_bit(1, [1,5,6,7,3,15])
    bf.display()
    print(bf.look_up(1, [1,5,6,7,3,15]))