import sys, re, os
import argparse
import re
import inflect
from pathlib import Path

_inflect = inflect.engine()
_comma_number_re = re.compile(r'([0-9][0-9\,]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\.[0-9]+)')
_pounds_re = re.compile(r'£([0-9\,]*[0-9]+)')
_dollars_re = re.compile(r'\$([0-9\.\,]*[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+(st|nd|rd|th)')
_number_re = re.compile(r'[0-9]+')


def _remove_commas(m):
  return m.group(1).replace(',', '')


def _expand_decimal_point(m):
  return m.group(1).replace('.', ' point ')


def _expand_dollars(m):
  match = m.group(1)
  parts = match.split('.')
  if len(parts) > 2:
    return match + ' dollars'  # Unexpected format
  dollars = int(parts[0]) if parts[0] else 0
  cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
  if dollars and cents:
    dollar_unit = 'dollar' if dollars == 1 else 'dollars'
    cent_unit = 'cent' if cents == 1 else 'cents'
    return '%s %s, %s %s' % (dollars, dollar_unit, cents, cent_unit)
  elif dollars:
    dollar_unit = 'dollar' if dollars == 1 else 'dollars'
    return '%s %s' % (dollars, dollar_unit)
  elif cents:
    cent_unit = 'cent' if cents == 1 else 'cents'
    return '%s %s' % (cents, cent_unit)
  else:
    return 'zero dollars'


def _expand_ordinal(m):
  return _inflect.number_to_words(m.group(0))


def _expand_number(m):
  num = int(m.group(0))
  if num > 1000 and num < 3000:
    if num == 2000:
      return 'two thousand'
    elif num > 2000 and num < 2010:
      return 'two thousand ' + _inflect.number_to_words(num % 100)
    elif num % 100 == 0:
      return _inflect.number_to_words(num // 100) + ' hundred'
    else:
      return _inflect.number_to_words(num, andword='', zero='oh', group=2).replace(', ', ' ')
  else:
    return _inflect.number_to_words(num, andword='')


def normalize_numbers(text):
  text = re.sub(_comma_number_re, _remove_commas, text)
  text = re.sub(_pounds_re, r'\1 pounds', text)
  text = re.sub(_dollars_re, _expand_dollars, text)
  text = re.sub(_decimal_number_re, _expand_decimal_point, text)
  text = re.sub(_ordinal_re, _expand_ordinal, text)
  text = re.sub(_number_re, _expand_number, text)
  return text

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to dataset file")
    args = parser.parse_args(args)
    return args


cmudict = {}
_real_word_re = re.compile(r'[a-zA-Z\']+')
_arpabet_seq_re = re.compile(r'{.*?}')
_arpabet_split_re = re.compile(r'[^\s]*{.*?}[^\s]*|[^\s]+')
_whitespace_re = re.compile(r'\s+')

double = False
MAIN_SCRIPT_DIR = Path(__file__).resolve().parent

for line in (open(str(MAIN_SCRIPT_DIR) + '/merged.dict.txt', "r").read().splitlines()):
    entry = [x.strip() for x in line.split(" ", 1)]
    cmudict[entry[0]] = entry[1]

def arpa_word(word):
    if _arpabet_seq_re.search(word):
        return word
    try:
      arpa = _real_word_re.search(word).group(0);
      get = cmudict.get(arpa.upper());
      if get == None:
          return word
    except:
      return word.lower();
        
    return word.replace(arpa, "{%s}" % get);



if __name__ == "__arpa__":
    args = parse_args(sys.argv[1:])
    with open(args.file.replace(".txt","ARPA.txt"), 'w') as w:
      with open(args.file, 'r') as f:
          for line in f.readlines():
              split = line.strip().split("|")
              text = normalize_numbers(split[0]).replace("-",", ")
              text = _whitespace_re.sub(" ", text.lower())
              text = _arpabet_split_re.findall(text)
              text = [arpa_word(x) for x in text]
              text = " ".join(text).upper()
              wav = split[0]
              final = "|".join([wav, text]) + "\n"
              w.write(final)