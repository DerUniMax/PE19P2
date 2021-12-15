def parse(dataset):
  dataset["Zimmerzahl"] = dataset["Zimmerzahl"].map(_parse_room_amount)
  
  _assemble_net(dataset)
  
  print(dataset[dataset["Zimmerzahl"] == None])

def _assemble_net(dataset):
  pass

def _parse_room_amount(amount):
  number = amount.split(" ")[0]
  if len(number.split("-")) != 2:
    return _text_to_num(number)
  return number

def _text_to_num(text):
  if text == "Ein":
    return 1
  if text == "Zwei":
    return 2