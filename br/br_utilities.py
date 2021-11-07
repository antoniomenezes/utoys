#!/usr/bin/python
# coding=utf-8

# !pip install unidecode
import random
from unidecode import unidecode

# The CPF number is the Brazilian individual taxpayer registry identification.
# It is an 11-digit number in the format 000.000.000-00.
# There is a two digit verification value (DV) used for CPF.
# The following code was based on http://ghiorzi.org/DVnew.htm

# Returns the first 9 CPF digits concatenated to DV digits
def get_cpf_and_dv(value):
  primary_val = str(value).rjust(9,'0')
  sum1 = 0
  sum2 = 0
  for i in range(len(primary_val)):
    sum1 += int(primary_val[i]) * (i+1)
  digit1 = sum1 % 11
  if digit1 == 10:
    digit1 = 0

  for j in range(len(primary_val+str(digit1))):
    sum2 += int((primary_val+str(digit1))[j]) * (j)
  digit2 = sum2 % 11
  if digit2 == 10:
    digit2 = 0

  return primary_val + str(digit1) + str(digit2)


# Generate random brazilian phone book according to CPF, brazilian proper nouns, brazilian phone numbers
# Example:
# book = {}
# book = random_br_phone_book(book, 5)
#
def random_br_phone_book(phone_book, entries_quantity):
  # Loading proper nouns
  proper_nouns_file = open('nomes_proprios.txt','r')
  proper_nouns = proper_nouns_file.readlines()
  proper_nouns_file.close()

  for n in range(entries_quantity):
    value_random = random.randrange(100000000, 999999999)
    value_prefix_phone = random.randrange(2100, 9999)
    value_suffix_phone = random.randrange(0000, 9999)
    year_random = random.randrange(1930, 2021)
    list_ddd = [11,12,13,14,15,16,17,18,19,21,22,24,27,28,31,32,33,34,35,37,38,41,42,43,44,45,46,47,48,49,
                 51,53,54,55,61,62,63,64,65,66,67,68,69,71,73,74,75,77,79,81,82,83,84,85,86,87,88,89,
                 91,92,93,94,95,96,97,98,99]
    ddd_random = '('+str(random.choice(list_ddd))+')'
    first_name = random.choice(proper_nouns).replace('\n','')
    last_name = random.choice(proper_nouns).replace('\n','')
    phone_random = ddd_random+' '+str(value_prefix_phone)+'-'+str(value_suffix_phone)
    twitter_user_random = '@'+unidecode(first_name[:3])+unidecode(last_name[:3])+str(year_random)

    phone_book[get_cpf_and_dv(value_random)] = [first_name+' '+last_name, phone_random, twitter_user_random]
  return phone_book


# Just to print a random brazilian phone book generated by previous function
# Example:
# print_phone_book(book)
# 46395598520: Marilda Racevalina, (81) 4045-3448 (@MarRac1996)
# 32233086104: Vivaldi Nouméa, (24) 3753-2035 (@VivNou1958)
# 11754914110: Giovane Ervino, (48) 2366-695 (@GioErv1933)
# 30738898848: Alaor Colodino, (62) 6683-1419 (@AlaCol1955)
# 48234032747: Graciete Milca, (34) 9786-3131 (@GraMil2005)
#
def print_phone_book(phone_book):
  print('CPF        : name, telephone (twitter user)')
  for k, v in phone_book.items():
    name = v[0]
    phone = v[1]
    user = v[2]
    print(k+':', name+', '+phone+' ('+user+')')

