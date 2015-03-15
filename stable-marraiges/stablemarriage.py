
class Suitor(object):
   def __init__(self, id, prefList):
      self.prefList = prefList
      self.rejections = 0 # num rejections is also the index of the next option
      self.id = id

   def preference(self):
      return self.prefList[self.rejections]

   def __repr__(self):
      return repr(self.id)


class Suited(object):
   def __init__(self, id, prefList):
      self.prefList = prefList
      self.held = None
      self.currentSuitors = set()
      self.id = id

   def reject(self):
      if len(self.currentSuitors) == 0:
         return set()

      if self.held is not None:
         self.currentSuitors.add(self.held)

      self.held = min(self.currentSuitors, key=lambda suitor: self.prefList.index(suitor.id))
      rejected = self.currentSuitors - set([self.held])
      self.currentSuitors = set()

      return rejected

   def __repr__(self):
      return repr(self.id)


# stableMarriage: [Suitor], [Suited] -> {Suitor: Suited}
# construct a stable marriage between suitors and suiteds
def stableMarriage(suitors, suiteds):
   unassigned = set(suitors)

   while len(unassigned) > 0:
      for suitor in unassigned:
         suiteds[suitor.preference()].currentSuitors.add(suitor)
      unassigned = set()

      for suited in suiteds:
         unassigned |= suited.reject()

      for suitor in unassigned:
         suitor.rejections += 1

   return dict([(suited.held, suited) for suited in suiteds])


# verifyStable: [Suitor], [Suited], {Suitor: Suited} -> bool
# check that the assignment of suitors to suited is a stable marriage
def verifyStable(suitors, suiteds, marriage):
   import itertools
   suitedToSuitor = dict((v,k) for (k,v) in marriage.items())

   precedes = lambda L, item1, item2: L.index(item1) < L.index(item2)

   def suitorPrefers(suitor, suited):
      return precedes(suitor.prefList, suited.id, marriage[suitor].id)

   def suitedPrefers(suited, suitor):
      return precedes(suited.prefList, suitor.id, suitedToSuitor[suited].id)

   for (suitor, suited) in itertools.product(suitors, suiteds):
      if suited != marriage[suitor] and suitorPrefers(suitor, suited) and suitedPrefers(suited, suitor):
         return False, (suitor.id, suited.id)

   return True


if __name__ == "__main__":
   from test import test

   suitors = [Suitor(0, [0,1]), Suitor(1, [1,0])]
   suiteds = [Suited(0, [0,1]), Suited(1, [1,0])]
   marriage = stableMarriage(suitors, suiteds)
   test({suitors[0]:suiteds[0], suitors[1]:suiteds[1]}, marriage)
   test(True, verifyStable(suitors, suiteds, marriage))


   suitors = [Suitor(0, [3,5,4,2,1,0]), Suitor(1, [2,3,1,0,4,5]),
               Suitor(2, [5,2,1,0,3,4]), Suitor(3, [0,1,2,3,4,5]),
               Suitor(4, [4,5,1,2,0,3]), Suitor(5, [0,1,2,3,4,5])]

   suiteds = [Suited(0, [3,5,4,2,1,0]), Suited(1, [2,3,1,0,4,5]),
               Suited(2, [5,2,1,0,3,4]), Suited(3, [0,1,2,3,4,5]),
               Suited(4, [4,5,1,2,0,3]), Suited(5, [0,1,2,3,4,5])]

   marriage = stableMarriage(suitors, suiteds)
   test({suitors[0]:suiteds[3], suitors[1]:suiteds[2], suitors[2]:suiteds[5],
         suitors[3]:suiteds[0], suitors[4]:suiteds[4], suitors[5]:suiteds[1]}, marriage)
   test(True, verifyStable(suitors, suiteds, marriage))
