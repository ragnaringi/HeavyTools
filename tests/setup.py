import os, shutil, zipfile

# Downloads precompiled Heavy source of pd/metro patch for testing without hv-uploader installed

def downloadSource():
  zipFile = "metro.1.c.src.zip"
  zipUrl  = "https://www.dropbox.com/s/3ldots4vtv8bqlw/" + zipFile

  os.system("wget " + zipUrl)

  dstDir  = "src"
  if os.path.exists(dstDir):
    shutil.rmtree(dstDir)
  os.makedirs(dstDir)

  zip_ref = zipfile.ZipFile(zipFile, "r")
  zip_ref.extractall(dstDir)
  zip_ref.close()

  os.remove(zipFile)

if __name__ == '__main__':
  downloadSource()