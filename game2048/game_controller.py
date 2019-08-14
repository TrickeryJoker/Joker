"""
    负责处理游戏核心逻辑模块

    步骤：
        1. 创建项目game2048,创建模块game_controller
        2. 将之前完成的面向过程的核心算法，移动到GameController类中．
            数据作为实例变量，操作作为实例方法.
        3. 在GameController类中，定义产生一个新数字的方法
            在随机的空白位置(零元素)上
            产生随机的数字(2的概率90%  4的概率10%)　

        4. 在GameController类中，定义判断游戏是否结束的方法
            如果有空位置不能结束
            如果水平方向，相邻具有相同元素，不能结束
            如果垂直方向，相邻具有相同元素，不能结束
            以上都不满足，游戏结束.

"""
import copy
import random

from model import Location


class GameController:
    """
        负责处理游戏核心逻辑
    """

    def __init__(self):
        self.__list_merge = [2, 16, 0, 4]
        self.__map = [
            [2, 0, 0, 2],
            [2, 2, 0, 4],
            [0, 4, 0, 4],
            [2, 2, 2, 0],
        ]
        self.__list_empty_location = []

    # 只读属性
    @property
    def map(self):
        return self.__map  # 缺点：类外仍然可以修改列表对象　
        # 缺点：每次读取数据，都会复制一份数据,内存占用过大．
        # return self.__map[:]
        # return copy.deepcopy(self.__map)

    # def get_map(self):
    #     return self.__map
    # 对象.get_map()
    # 对象.map
    def __zero_to_end(self):
        for i in range(len(self.__list_merge) - 1, -1, -1):
            if self.__list_merge[i] == 0:
                del self.__list_merge[i]
                self.__list_merge.append(0)

    def __merge(self):
        self.__zero_to_end()
        for i in range(len(self.__list_merge) - 1):
            if self.__list_merge[i] == self.__list_merge[i + 1]:
                self.__list_merge[i] *= 2
                del self.__list_merge[i + 1]
                self.__list_merge.append(0)

    def move_left(self):
        """
            向左移动
        """
        for line in self.__map:
            self.__list_merge = line
            self.__merge()

    def move_right(self):
        """
            向右移动
        """
        for line in self.__map:
            self.__list_merge = line[::-1]
            self.__merge()
            line[::-1] = self.__list_merge

    def move_up(self):
        """
            向上移动
        """
        self.__square_matrix_transpose()
        self.move_left()
        self.__square_matrix_transpose()

    def move_down(self):
        """
            向下移动
        """
        self.__square_matrix_transpose()
        self.move_right()
        self.__square_matrix_transpose()

    def __square_matrix_transpose(self):
        for c in range(1, len(self.__map)):
            for r in range(c, len(self.__map)):
                self.__map[r][c - 1], self.__map[c - 1][r] = self.__map[c - 1][r], self.__map[r][c - 1]

    def generate_new_number(self):
        """
            生成新数字　
        """
        self.__calculate_empty_location()
        # if len(self.__list_empty_location) == 0: return
        loc = random.choice(self.__list_empty_location)
        # self.__map[location[0]][location[1]] = 4 if random.randint(0,10) ==1 else 2
        self.__map[loc.r][loc.c] = self.__create_random_number()
        # self.__list_empty_location.remove(loc)

    def __create_random_number(self):
        return 4 if random.randint(0, 10) == 1 else 2

    def __calculate_empty_location(self):
        self.__list_empty_location.clear()
        for r in range(len(self.__map)):
            for c in range(len(self.__map[r])):
                if self.__map[r][c] == 0:
                    # 记录r c
                    # self.__list_empty_location.append((r, c))
                    self.__list_empty_location.append(Location(r, c))


if __name__ == "__main__":
    # 测试代码
    controller = GameController()
    # controller.move_right()
    # controller.move_down()

    # controller.map = 100 只读属性不能修改
    # controller.map[0][0] = 100　通过属性返回对象地址，可以修改对象.

    print(controller.map)
    controller.generate_new_number()
    print(controller.map)
