import requests
import helpers.bovespa_unzipper as bovespa_unzipper
from xml_extractors import formulario_cadastral_extractor
import helpers.zip_helper as zip_helper
import os
from helpers import bovespa_unzipper

bovespa_url_base = \
    'https://www.rad.cvm.gov.br/enetconsulta/frmDownloadDocumento.aspx?' \
    'CodigoInstituicao=2&NumeroSequencialDocumento={}'


def process_file(index):
    downloaded_file = requests.get(bovespa_url_base.format(index), verify=False).content

    try:
        root_zip_file = zip_helper.bytes_to_zipfile(downloaded_file)
    except:
        print('file index {} is not a zip file'.format(index))
        return

    if len(list(filter(lambda x: ('DFP' in x.filename) or ('ITR' in x.filename), root_zip_file.filelist))) == 0:
        print('file index {} is not dfp nor itr'.format(index))
        return

    all_files = bovespa_unzipper.unzip(downloaded_file)
    formulario_cadastral_info = formulario_cadastral_extractor.extract_information(all_files['formulario_cadastral'])

    directory = '{}/{}'.format('/home/zembrzuski/labs/rolling-snow-zips', formulario_cadastral_info['codigo_cvm'])

    os.makedirs(directory, exist_ok=True)

    with open('{}/{}.zip'.format(directory, index), 'wb') as f:
        f.write(downloaded_file)


def download():
    index = 9675

    while index > 0:
        print('trying {}'.format(index))
        process_file(index)
        print('finished {}'.format(index))
        index = index - 1
