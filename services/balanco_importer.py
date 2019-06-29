from xml_extractors import formulario_cadastral_extractor
import helpers.download_helper as downloader_helper
import helpers.bovespa_unzipper as bovespa_unzipper
import xml_extractors.info_financeiras_extractor as info_financeiras_extractor
from xml_extractors import composicao_capital_social_extractor


def import_balanco(id_documento):
    url_to_download = \
        'https://www.rad.cvm.gov.br/enetconsulta/frmDownloadDocumento.aspx?' \
        'CodigoInstituicao=2&NumeroSequencialDocumento=81551'

    downloaded_file = downloader_helper.download_zip_file_from_bovespa(url_to_download)
    all_files = bovespa_unzipper.unzip(downloaded_file)

    formulario_cadastral_info = formulario_cadastral_extractor.extract_information(all_files['formulario_cadastral'])
    info_financeiras = info_financeiras_extractor.extract_information(all_files['informacoes_financeiras'])
    composicao_capital = composicao_capital_social_extractor.extract_information(all_files['composicao_capital_social'])

    return True
