# -*- coding: utf-8 -*-

import argparse, codecs, os, re, sys

# line related regular expression data
atr_RegExpStrSongNumber = r'(.*)Nr (\d+)[\.]*(.*)'

# text origin related regular expression
atr_RegExpSongNumberQuery = re.compile(atr_RegExpStrSongNumber, re.UNICODE | re.IGNORECASE)

def main():
  tmp_Parser = argparse.ArgumentParser()
  tmp_Parser.add_argument('OptInput', metavar='FILE', help='input file to be processed')
  tmp_Parser.add_argument('OptOutput', metavar='FOLDER', help='output folder')
  tmp_Args = tmp_Parser.parse_args()

  # sanity check
  if not os.path.exists(tmp_Args.OptInput):
    sys.exit(os.EX_OSFILE)

  if not os.path.exists(tmp_Args.OptOutput):
    sys.exit(os.EX_OSFILE)

  print 'Processing file ' + tmp_Args.OptInput

  with codecs.open(tmp_Args.OptInput, 'r', 'utf-8') as tmp_File:
    tmp_FileContents = [tmp_Line.strip() for tmp_Line in tmp_File.readlines()]

  # remove empty lines
  tmp_FileContents[:] = [tmp_Line for tmp_Line in tmp_FileContents if len(tmp_Line) > 0]

  tmp_Count = 0
  tmp_Key = ''
  tmp_Songs = {}
  for tmp_Line in tmp_FileContents:
    tmp_Rslt = atr_RegExpSongNumberQuery.match(tmp_Line)
    if tmp_Rslt is not None:
      tmp_Groups = tmp_Rslt.groups()
      if tmp_Key != '' and len(tmp_Groups[0]) > 0:
        tmp_Songs[tmp_Key].append(tmp_Groups[0])
      tmp_Key = tmp_Groups[1]
      if tmp_Key not in tmp_Songs:
        tmp_Songs[tmp_Key] = [tmp_Key + u'.']
        if len(tmp_Groups[2]) > 0:
          tmp_Songs[tmp_Key].append(tmp_Groups[2])
        tmp_Count = tmp_Count + 1
    elif tmp_Key != '':
      tmp_Songs[tmp_Key].append(tmp_Line)
  
  for tmp_Key, tmp_Value in tmp_Songs.items():
    tmp_OutputFileName = os.path.join(tmp_Args.OptOutput.decode('utf-8'), tmp_Key + '.txt')
    print u'Write output file: ' + tmp_OutputFileName
    with codecs.open(tmp_OutputFileName, 'w+', 'utf-8') as f:
      f.write(u'\n'.join(tmp_Value))

  print 'Found ' + str(tmp_Count) + ' entries'


if __name__ == "__main__":
  main()

