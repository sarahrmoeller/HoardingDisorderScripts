import utils.data.datasaur as datasaur


TEXT_FILE_DIRECTORY = './data/mathews/documents/text_files/'


for doc in datasaur.docs:
    set_dir = "set0" + str(doc.set)
    filename = doc.fixed_name
    with open(TEXT_FILE_DIRECTORY + f"{set_dir}/{filename}", 'w+') \
        as f:
        f.write(doc.content())