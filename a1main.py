import numpy as np


class grid:
  def __init__(self, gamma=1, length=5):
    # initialize the grid of size x*x and put initial value to all states
    self.gamma = gamma  # the discount rate
    self.length = length  # the length of the grid
    self.stateNum = length ** 2  # the number of states in the grid
    self.grid = np.full((length, length), 0)  # init the grid with value of each state to 0
    self.a = np.array([np.array([0.] * self.stateNum)] * self.stateNum)  # init A for Ax = B
    self.b = [0.] * self.stateNum  # init B for Ax = B

  def analyze(self):
    # find A and B matrices from  Ax = B

    for i in range(self.stateNum):
      # for every state in the grid: cacluate the value for four movements one by one
      newA = self.a[i]

      if i - self.length < 0:
        # can't go up'
        newA[i] += 0.25
      else:
        newA[i - self.length] -= 0.25

      if i + self.length >= self.stateNum:
        # can't go down
        newA[i] += 0.25
      else:
        newA[i + self.length] -= 0.25

      if i % self.length == 0:
        # can't go left
        newA[i] += 0.25
      else:
        newA[i - 1] -= 0.25

      if i % self.length == self.length - 1:
        # can't go right
        newA[i] += 0.25
      else:
        newA[i + 1] -= 0.25

  
      newB = newA[i] * -1
      # modify A and B with discount rate
      newA = self.gamma * newA
      newA[i] = 1 - newA[i]
      self.a[i] = newA * self.gamma
      self.b[i] = newB * self.gamma

  def solve(self):
    # solve the Ax = B equation set representing the grid, update all values in grid
    answer = np.linalg.solve(self.a, self.b)
    answer.shape = (self.length, self.length)
    # print(answer)

    print(np.around(answer,decimals=1))
    return answer

  def setPortal(self, x, y, reward):
    # set state x where when agent set food on it will teleport to y with a reward
    # change A for all state x to that have possiblity to state y + reward


    self.a[x] = [0.] * self.stateNum  # reset the state x's A
    self.a[x, x] = 1  # set up new A for state x
    self.a[x, y] = -1 * self.gamma  # from cacluation, a[x,y] = -discount rate

    self.b[x] = reward  # b of state x will simply be reward



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  testGrid = grid(gamma=0.9, length=5)
  # set two portals
  testGrid.analyze()
  testGrid.setPortal(1, 21, 10)
  testGrid.setPortal(3, 13, 5)

  testGrid.solve()

  grid5a = grid(gamma=0.85, length=5)
  grid5a.analyze()
  grid5a.setPortal(1, 21, 10)
  grid5a.setPortal(3, 13, 5)
  grid5a.solve()
  print('----------------')
  grid5b = grid(gamma=0.75, length=5)
  grid5b.analyze()
  grid5b.setPortal(1, 21, 10)
  grid5b.setPortal(3, 13, 5)
  grid5b.solve()
  print('----------------')
  grid7a = grid(gamma=0.85, length=7)
  grid7a.analyze()
  grid7a.setPortal(15, 43, 10)
  grid7a.setPortal(5, 26, 5)
  grid7a.solve()
  print('----------------')
  grid7b = grid(gamma=0.75, length=7)
  grid7b.analyze()
  grid7b.setPortal(15, 43, 10)
  grid7b.setPortal(5, 26, 5)
  grid7b.solve()
