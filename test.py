import re

recognized = [u'I hope you have finished your job or Departmentrobot to paint', u'what does basil need to come to the third person', u'they are competing to see if they thinking about it still under construction in the garage garage', u'we have to cut this meeting short I just received an encryptedmessage.', u'need the money for the Packers either you come with me', u'I hope you have finished your job or did possible to pay it', u'whatdoes daily news contact address', u'still under construction in the garage', u'Milton garage for the laboratory', u'look up this morning Charles I just received a message.', u'spider', u'I hope you had finished', u'what does Baileys come to the dojo', u'they are completely to see if they think the is still under construction at the garage', u"we'll figure it out"]
words = [['Robot \r\n'.rstrip(), []], ['Gadget\r\n', []], ['Labyrinth\r\n', []], ['Escobar\r\n', []], ['Bomb\r\n', []], ['Beetle\r\n', []], ['Penguin\r\n', []], ['Package\r\n', []], ['Interface\r\n', []], ['Laboratory\r\n', []], ['Glasses\r\n', []], ['Prototype', []]]

print recognized
print words

result = False

print words[0][0]

for phrase in recognized:    
    if re.search(words[0][0], phrase, re.IGNORECASE):
        result = True

print result

