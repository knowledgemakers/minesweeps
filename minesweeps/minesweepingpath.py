import math
from random import randint
import matplotlib.pyplot as plt
from statistics import mean


class MineSweepingPath():
    path = [(0, 0)]
    totalDifficulty = 0
    difficulties = []
    current_orientation = 0
    difficulties = [1.5, 2.15, 2.85, 1.5]
    difficulty_budget = 0
    current_step = 0
    budgets = []
    target_difficulty=8

    def add_step(self, coordinates):

        difficulty = self.get_difficulty(coordinates)
        angle = self.getangle(coordinates, self.path[-1])
        self.current_orientation = angle
        self.totalDifficulty += difficulty
        self.difficulties.append(difficulty)
        self.path.append(coordinates)

    def get_difficulty(self, next):
        curr = self.path[-1]
        xcurr, ycurr = curr
        xnext, ynext = next

        difficulty = max(abs(xnext - xcurr), abs(ynext - ycurr))
        new_orientation = self.getangle(next, curr) - self.current_orientation

        if new_orientation < 0 or new_orientation > 20:
            difficulty += abs(round(new_orientation / 180, 2))
        return difficulty

    def generate_next(self, difficulty):
        for x in range(0, 4):
            for y in range(0, 4):
                possible_difficulty = self.get_difficulty((x, y))
                if possible_difficulty == difficulty:
                    return x, y
        return None

    def next_step(self):
        current_difficulty = self.difficulties[self.current_step % len(self.difficulties)] + self.difficulty_budget
        next_steps = self.generate_next_possibilities(current_difficulty)
        if len(next_steps) > 1:
            choice = randint(0, len(next_steps) - 1)
            selected_difficulty, next_possibility = next_steps[choice]
        else:
            selected_difficulty, next_possibility = next_steps[0]
        if selected_difficulty != current_difficulty:
            self.difficulty_budget += round(selected_difficulty - current_difficulty, 2)
        self.budgets.append(self.difficulty_budget)
        budget_mean = mean(self.budgets)
        #if budget_mean < - 0.05 or budget_mean > 0.05:
        #    self.difficulty_budget -= budget_mean
        if self.current_step%5==0:
            diff_sum = sum(path.difficulties[-5:])
            self.difficulty_budget += self.target_difficulty-diff_sum
        self.add_step(next_possibility)
        self.current_step += 1
        return next_possibility

    def generate_next_possibilities(self, difficulty):
        exact_possibilities = []
        all_possibilities = []
        min_difference = 10000
        candidate = None
        for x in range(0, 4):
            for y in range(0, 4):
                possible_difficulty = self.get_difficulty((x, y))
                difference = abs(difficulty - possible_difficulty)
                if (x, y) not in self.path[-5:]:
                    if difference == 0:
                        exact_possibilities.append((possible_difficulty, (x, y)))
                    if difference < min_difference:
                        min_difference = difference
                        candidate = (possible_difficulty, (x, y))
                    all_possibilities.append((possible_difficulty, (x, y)))
        if len(exact_possibilities) == 0:
            return [candidate]
        else:
            return exact_possibilities

    def getangle(self, a, b):
        ax, ay = a
        bx, by = b
        degree_in_radians = math.atan2(ay - by, ax - bx)
        return math.degrees(degree_in_radians)

    def __str__(self):
        return str(self.totalDifficulty) + "\t" + str(self.path) + "\t" + str(self.difficulties)

    def __repr__(self):
        return str(self)


def generate_paths(current_path):
    paths = []
    if len(current_path.path) == 5:
        paths.append(current_path)
        print(current_path)
        return paths
    paths = []
    x_curr, y_curr = current_path.path[-1]
    for x in range(0, 4):
        for y in range(0, 4):
            if x == x_curr and y == y_curr or (x, y) in current_path.path:
                continue
            newpath = MineSweepingPath()
            newpath.path = current_path.path.copy()
            newpath.totalDifficulty = current_path.totalDifficulty
            newpath.difficulties = current_path.difficulties.copy()
            newpath.add_step((x, y))
            paths.extend(generate_paths(newpath))

    return paths


def main():
    path = MineSweepingPath()
    paths = generate_paths(path)
    for p in paths:
        print(p)


if __name__ == '__main__':
    # path = MineSweepingPath()
    # path.path = [(0, 0)]
    # path.add_step((0, 1))
    # path.add_step((1, 1))
    # path.add_step((0, 0))
    # path.add_step((0, 1))
    # path.add_step((3, 3))
    # path.add_step((0, 0))
    # print(path)
    # main()

    for k in range(5):
        path = MineSweepingPath()
        sums = []
        for g in range(1000):
            path.next_step()
            # print(str(g) + "\t " + str(path.totalDifficulty) + "\t " + str(path.difficulty_budget) + "\t " + str(path.path))
        for i in range(0,len(path.difficulties),5):
            diff_sum = sum(path.difficulties[i:i+4])
            #print(str(i) + " sum=" + str(diff_sum))
            sums.append(diff_sum)

        plt.plot(sums)
        plt.title('1000 budgets run#' + str(k) + " Total Difficulty: " + str(path.totalDifficulty))
        plt.ylabel("Sum of 5 step value")
        plt.savefig("difftot_run#" + str(k) + ".png")
        plt.cla()
        plt.clf()
        plt.close(plt.figure())
        print("#" + str(k) + str(mean(sums)))
#    main()
