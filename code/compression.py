def compress(filein,fileout):
  from PIL import Image

  foo = Image.open(filein)

  foo = foo.convert('RGB')


  foo.save(fileout,quality=20)
  return

  