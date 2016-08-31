import base64
class Settings():
  myword = base64.b64encode("bob is awesome", None)
  def getWord(self):
    return base64.b64decode(self.myword, None)
  def setWord(self, input):
    self.myword = b64encode(input, None)
