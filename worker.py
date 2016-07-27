import requests
import csv
from bs4 import BeautifulSoup
import datetime

# def create_programs():
#     beginning_record = 1
#
#     with open('programs.csv', 'w') as outfile:
#         fieldnames = ['name', 'guidebox_id', 'rating', 'runtime', 'thumbnail',
#         'banner', 'overview', 'review_text', 'positive_message', 'positive_role_model', 'violence',
#         'sex', 'language', 'consumerism', 'substance']
#         writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#         writer.writeheader()
#
#
#         while beginning_record <= 20000:
#             key = ""
#             base_url = "https://api-public.guidebox.com/v1.43/US/"
#             show_url = base_url + key + '/shows/all/{}/1'.format(beginning_record)
#             response = requests.get(show_url).json()
#             for show in response['results']:
#                 guidebox_id = show['id']
#                 info_url = base_url + key + '/show/' + str(guidebox_id)
#                 response = requests.get(info_url).json()
#                 name = response['title']
#                 thumbnail = response['artwork_448x252']
#                 banner = response['banner']
#                 overview = response['overview']
#                 rating = response['rating']
#                 runtime = response['runtime']
#                 link = response['common_sense_media']
#                 print(link)
#                 if link is None or link is '':
#                     review_text = 'Not Available'
#                     positive_message = 'Not Available'
#                     positive_role_model = "Not Available"
#                     violence = 'Not Available'
#                     sex = "Not Available"
#                     language = "Not Available"
#                     consumerism = "Not Available"
#                     substance = "Not Available"
#
#                 else:
#                     content = requests.get(link)
#                     souper = BeautifulSoup(content.text, 'html.parser')
#                     review = souper.find(class_='field field-name-field-parents-need-to-know field-type-text-long field-label-hidden')
#                     try:
#                         review_text = review.find("p").text.strip()
#                     except AttributeError:
#                         review_text = ""
#                     messages = souper.find_all(class_='content')
#                     for message in messages:
#                         message = message.text
#                         if 'Positive messages' in message:
#                             positive_message = message.split("Positive messages",1)[1].strip()
#
#
#                         if "Positive role models" in message:
#                             positive_role_model = message.split("Positive role models",1)[1].strip()
#
#
#                         if "Violence & scariness" in message:
#                             violence = message.split("scariness",1)[1].strip()
#                         elif 'Violence' in message:
#                             violence = message.split("Violence",1)[1].strip()
#
#
#                         if "Sexy stuff" in message:
#                             sex = message.split("Sexy stuff",1)[1].strip()
#                         elif "Sex" in message:
#                             sex = message.split("Sex",1)[1].strip()
#
#
#                         if "Language" in message:
#                             language = message.split("Language",1)[1].strip()
#
#
#                         if "Consumerism" in message:
#                             consumerism = message.split("Consumerism",1)[1].strip()
#
#
#                         if "Drinking, drugs, & smoking" in message:
#                             substance = message.split("Drinking, drugs, & smoking",1)[1].strip()
#
#
#
#
#                 writer.writerow({'name': name, 'guidebox_id': guidebox_id, 'rating': rating, 'runtime': runtime, 'thumbnail': thumbnail,
#                 'banner': banner, 'overview': overview, 'review_text': review_text, 'positive_message': positive_message,
#                 'positive_role_model': positive_role_model, 'violence': violence, 'sex': sex, 'language': language, 'consumerism':consumerism,
#                 'substance': substance})
#             beginning_record += 250
#             print(beginning_record, datetime.datetime.now())
# create_programs()


def add_program(apps, schema_editor):
    Program = apps.get_model('main', 'Program')
    Rating = apps.get_model('main', 'Rating')
    with open('programs.csv') as infile:
        data = csv.DictReader(infile, delimiter=",", fieldnames=('name', 'guidebox_id',
                                                                       'rating', 'runtime', 'thumbnail',
                                                                       'banner', 'overview', 'review_text', 'positive_message',
                                                                       'positive_role_model', 'violence', 'sex', 'language',
                                                                       'consumerism', 'substance'))
        for row in data:
            rating = Rating.objects.get(rating=row['rating'])
            print(row['guidebox_id'])
            Program.objects.create(name=row['name'],
                                 guidebox_id=row['guidebox_id'],
                                 rating=rating,
                                 runtime=row['runtime'],
                                 thumbnail=row['thumbnail'],
                                 banner=row['banner'],
                                 overview=row['overview'],
                                 review=row['review_text'],
                                 positive_message=row['positive_message'],
                                 positive_role_model=row['positive_role_model'],
                                 violence=row['violence'],
                                 sex=row['sex'],
                                 language=row['language'],
                                 consumerism=row['consumerism'],
                                 substance=row['substance'])

def add_ratings(apps, schema_editor):
    Rating = apps.get_model('main', 'Rating')
    with open('ratings.csv') as infile:
        data = csv.DictReader(infile, delimiter="|", fieldnames=('rating', 'description', 'detail'))
        for row in data:

            Rating.objects.create(rating=row['rating'],
                                 description=row['description'],
                                 detail=row['detail'])
