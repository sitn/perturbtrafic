

import xmltodict
import os
import json
import transaction
from .. import models
import datetime
import logging
from ..scripts.utils import Utils

log = logging.getLogger(__name__)

class EvenementXML():
    folder_path = None
    settings = None
    request = None

    @classmethod
    def list_folder_files(cls, request):
        try:
            cls.request = request
            cls.settings = cls.request.registry.settings
            cls.folder_path = cls.settings['evenements_xml_files_folder']
            return [f for f in os.listdir(cls.folder_path) if f.endswith('.xml')]

        except Exception as error:
            raise Exception(str(error))
        return []

    @classmethod
    def remove_file(cls, request, file_name):
        try:
            os.remove(request.registry.settings['evenements_xml_files_folder'] + '/' + file_name)

        except Exception as error:
            raise Exception(str(error))
        return []


    @classmethod
    def xml_to_json(cls, file):
        with open(cls.folder_path + '/' + file, mode="r", encoding="utf-8") as file:
            data = file.read().replace('\n', '')
            xpars = xmltodict.parse(data)
            return xpars

        return None



    @classmethod
    def add_file_data(cls, file_json):
        try:
            if 'dossiers' in file_json:
                dossiers = file_json['dossiers']

                if dossiers and 'dossier' in dossiers:
                    dossier = dossiers['dossier']

                    if dossier:
                        id_dossier = dossier['@id']

                        ### (1) Autre entrave
                        if id_dossier and int(id_dossier) == 3:
                            return cls.add_file_data_autre_entrave(dossier)

                        ### (2) Fouille
                        elif id_dossier and int(id_dossier) == 1:
                            return cls.add_file_data_fouille(dossier)


        except Exception as e:
            log.error(str(e))
            return False

        return True

    @classmethod
    def add_file_data_autre_entrave(cls, dossier):
        try:

            max_event_id = None
            with transaction.manager:
                cls.request.dbsession.execute('set search_path to ' + cls.settings['schema_name'])

                if dossier:

                    # libelle
                    title = dossier['title'] if 'title' in dossier else None

                    # description
                    description = dossier['descriptions'][
                        'descr_lib'] if 'descriptions' in dossier and 'descr_lib' in dossier[
                        'descriptions'] else None

                    # Date debut
                    date_debut = None

                    # Heure debut
                    heure_debut = None

                    # Date fin
                    date_fin = None

                    # Heure fin
                    heure_fin = None

                    # Surface
                    surface = None

                    # Longueur_etape
                    longueur_etape = None

                    # Cause de la fouille
                    cause_fouille = None

                    # Description fouille
                    description_fouille = None

                    # Adresse de la fouille
                    adresse_fouille = None

                    # Rue requerant entreprise
                    rue_requerant_entreprise = None

                    # Localite requerant entreprise
                    localite_requerant_entreprise = None

                    # Telephone requerant entreprise
                    telephone_requerant_entreprise = None

                    # Fax requerant entreprise
                    fax_requerant_entreprise = None

                    # Courriel requerant entreprise
                    courriel_requerant_entreprise = None

                    # Nom requerant entreprise
                    nom_requerant_entreprise = None

                    # Nom requerant personne
                    nom_requerant_personne = None

                    # Prenom requerant personne
                    prenom_requerant_personne = None

                    # Mobile requerant personne
                    mobile_requerant_personne = None

                    # Telephone requerant personne
                    telephone_requerant_personne = None

                    # Fax requerant personne
                    fax_requerant_personne = None

                    # Courriel requerant personne
                    courriel_requerant_personne = None

                    # Nom maitre ouvrage direction locale
                    nom_maitre_ouvrage_dir_loc = None

                    # Prenom maitre ouvrage direction locale
                    prenom_maitre_ouvrage_dir_loc = None

                    # Mobile maitre ouvrage direction locale
                    mobile_maitre_ouvrage_dir_loc = None

                    # Telephone maitre ouvrage direction locale
                    telephone_maitre_ouvrage_dir_loc = None

                    # Fax maitre ouvrage direction locale
                    fax_maitre_ouvrage_dir_loc = None

                    # Courriel maitre ouvrage direction locale
                    courriel_maitre_ouvrage_dir_loc = None

                    # Rue maitre ouvrage entreprise
                    rue_maitre_ouvrage_entreprise = None

                    # Localite maitre ouvrage entreprise
                    localite_maitre_ouvrage_entreprise = None

                    # Telephone maitre ouvrage entreprise
                    telephone_maitre_ouvrage_entreprise = None

                    # Fax maitre ouvrage entreprise
                    fax_maitre_ouvrage_entreprise = None

                    # Courriel maitre ouvrage entreprise
                    courriel_maitre_ouvrage_entreprise = None

                    # Nom maitre ouvrage entreprise
                    nom_maitre_ouvrage_entreprise = None

                    # Adresse facturation
                    adresse_facturation = None

                    # Num bien-fonds
                    num_bien_fonds = None

                    # Commune
                    commune = None

                    # Coordonnee X
                    coordonnee_x = None

                    # Coordonnee Y
                    coordonnee_y = None

                    # Geometry collection
                    geometry_collection = None

                    # Cadastre
                    cadastre = None

                    # Lieu dit
                    lieu_dit = None

                    # Service à appliquer
                    service_a_appliquer = None

                    form = dossier['forms']['form'] if 'forms' in dossier and 'form' in dossier[
                        'forms'] else None

                    if form and len(form) > 0:

                        """------------- (1) Form evenement ---------------"""
                        evenement_form = [f for f in form if f['@id'] == '45']
                        evenement_form = evenement_form[0] if len(evenement_form) > 0 else None

                        if evenement_form:

                            section = evenement_form['sections'][
                                'section'] if 'sections' in evenement_form and 'section' in evenement_form[
                                'sections'] else None

                            if section and len(section) > 0:

                                """( 1.1) Info evenement """
                                # date_debut, heure_debut, date_fin, heure_fin, surface ....

                                section_evenement = [sec for sec in section if sec['@id'] == '51']
                                section_evenement = section_evenement[0] if len(section_evenement) > 0 else None

                                evenement_question = section_evenement['questions'][
                                    'question'] if section_evenement and 'questions' in section_evenement and 'question' in \
                                                   section_evenement['questions'] else None

                                for one_evenement_question in evenement_question:
                                    id = one_evenement_question['@id']

                                    # surface
                                    if id == '15':
                                        surface = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None
                                        try:
                                            surface = float(surface)
                                        except Exception as e:
                                            surface = None

                                    # longueur_etape
                                    elif id == '16':
                                        longueur_etape = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None

                                    # date_debut
                                    elif id == '121':
                                        date_debut = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None
                                        date_debut = date_debut.replace(".", "-") if date_debut else None

                                    # heure_debut
                                    elif id == '122':
                                        heure_debut = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None
                                        heure_debut = heure_debut.replace(".", ":").replace("h",
                                                                                            ":") if heure_debut else None
                                        heure_debut = heure_debut + ":00" if heure_debut and len(
                                            heure_debut) <= 2 else heure_debut
                                        heure_debut = "0" + heure_debut if heure_debut and len(
                                            heure_debut) == 3 else heure_debut

                                    # date_fin
                                    elif id == '123':
                                        date_fin = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None
                                        date_fin = date_fin.replace(".", "-") if date_fin else None

                                    # heure_fin
                                    elif id == '124':
                                        heure_fin = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None
                                        heure_fin = heure_fin.replace(".", ":").replace("h",
                                                                                            ":") if heure_fin else None
                                        heure_fin = heure_fin + ":00" if heure_fin and len(
                                            heure_fin) <= 2 else heure_fin
                                        heure_fin = "0" + heure_fin if heure_fin and len(
                                            heure_fin) == 3 else heure_fin

                                    # cause_fouille
                                    elif id == '134':
                                        cause_fouille = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None

                                    # description_fouille
                                    elif id == '135':
                                        description_fouille = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None

                                    # adresse_fouille
                                    elif id == '201':
                                        adresse_fouille = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None


                                """( 1.2) Reque©rant - Entreprise / Service / Commune """
                                section_requerant_entreprise = [sec for sec in section if sec['@id'] == '1']
                                section_requerant_entreprise = section_requerant_entreprise[0] if len(section_requerant_entreprise) > 0 else None

                                requerant_entreprise_question = section_requerant_entreprise['questions'][
                                    'question'] if section_requerant_entreprise and 'questions' in section_requerant_entreprise and 'question' in \
                                                   section_requerant_entreprise['questions'] else None

                                for one_requerant_entreprise_question in requerant_entreprise_question:
                                    id = one_requerant_entreprise_question['@id']

                                    # nom_requerant_entreprise
                                    if id == '1':
                                        nom_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None

                                    # rue_requerant_entreprise
                                    elif id == '2':
                                        rue_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None

                                    # localite_requerant_entreprise
                                    elif id == '3':
                                        localite_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None

                                    # telephone_requerant_entreprise
                                    elif id == '4':
                                        telephone_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None

                                    # fax_requerant_entreprise
                                    elif id == '5':
                                        fax_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None

                                    # courriel_requerant_entreprise
                                    elif id == '6':
                                        courriel_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None


                                """( 1.3) Reque©rant - Personne de contact """
                                section_requerant_personne = [sec for sec in section if sec['@id'] == '32']
                                section_requerant_personne = section_requerant_personne[0] if len(section_requerant_personne) > 0 else None

                                requerant_personne_question = section_requerant_personne['questions'][
                                    'question'] if section_requerant_personne and 'questions' in section_requerant_personne and 'question' in \
                                                   section_requerant_personne['questions'] else None

                                for one_requerant_personne_question in requerant_personne_question:
                                    id = one_requerant_personne_question['@id']

                                    # nom_requerant_personne
                                    if id == '100':
                                        nom_requerant_personne = \
                                        one_requerant_personne_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                        one_requerant_personne_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_personne_question['answers'][
                                                            'answer'] else None

                                    # prenom_requerant_personne
                                    elif id == '101':
                                        prenom_requerant_personne = \
                                            one_requerant_personne_question['answers']['answer'][
                                                'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                            one_requerant_personne_question[
                                                                'answers'] and 'value' in \
                                                            one_requerant_personne_question['answers'][
                                                                'answer'] else None

                                    # mobile_requerant_personne
                                    elif id == '102':
                                        mobile_requerant_personne = \
                                            one_requerant_personne_question['answers']['answer'][
                                                'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                            one_requerant_personne_question[
                                                                'answers'] and 'value' in \
                                                            one_requerant_personne_question['answers'][
                                                                'answer'] else None

                                    # one_requerant_personne_question
                                    elif id == '103':
                                        one_requerant_personne_question = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                        one_requerant_personne_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_personne_question['answers'][
                                                            'answer'] else None

                                    # fax_requerant_personne
                                    elif id == '104':
                                        fax_requerant_personne = \
                                            one_requerant_personne_question['answers']['answer'][
                                                'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                            one_requerant_personne_question[
                                                                'answers'] and 'value' in \
                                                            one_requerant_personne_question['answers'][
                                                                'answer'] else None

                                    # courriel_requerant_personne
                                    elif id == '105':
                                        courriel_requerant_personne = \
                                        one_requerant_personne_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                        one_requerant_personne_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_personne_question['answers'][
                                                            'answer'] else None


                                """( 1.4) Maitre de l'ouvrage ou mandataire - Direction locale """
                                section_maitre_ouvrage_dir_loc  = [sec for sec in section if sec['@id'] == '33']
                                section_maitre_ouvrage_dir_loc = section_maitre_ouvrage_dir_loc[0] if len(section_maitre_ouvrage_dir_loc) > 0 else None

                                maitre_ouvrage_question_dir_loc = \
                                section_maitre_ouvrage_dir_loc['questions'][
                                    'question'] if section_maitre_ouvrage_dir_loc and 'questions' in section_maitre_ouvrage_dir_loc and 'question' in \
                                                   section_maitre_ouvrage_dir_loc['questions'] else None

                                for one_maitre_ouvrage_question_dir_loc in maitre_ouvrage_question_dir_loc:
                                    id = one_maitre_ouvrage_question_dir_loc['@id']

                                    # nom_maitre_ouvrage_dir_loc
                                    if id == '106':
                                        nom_maitre_ouvrage_dir_loc = \
                                        one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                            'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                        one_maitre_ouvrage_question_dir_loc[
                                                            'answers'] and 'value' in \
                                                        one_maitre_ouvrage_question_dir_loc['answers'][
                                                            'answer'] else None

                                    # prenom_maitre_ouvrage_dir_loc
                                    elif id == '107':
                                        prenom_maitre_ouvrage_dir_loc = \
                                            one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                            one_maitre_ouvrage_question_dir_loc[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_question_dir_loc['answers'][
                                                                'answer'] else None

                                    # mobile_maitre_ouvrage_dir_loc
                                    elif id == '108':
                                        mobile_maitre_ouvrage_dir_loc = \
                                            one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                            one_maitre_ouvrage_question_dir_loc[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_question_dir_loc['answers'][
                                                                'answer'] else None

                                    # telephone_maitre_ouvrage_dir_loc
                                    elif id == '109':
                                        telephone_maitre_ouvrage_dir_loc = \
                                            one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                            one_maitre_ouvrage_question_dir_loc[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_question_dir_loc['answers'][
                                                                'answer'] else None


                                    # fax_maitre_ouvrage_dir_loc
                                    elif id == '110':
                                        fax_maitre_ouvrage_dir_loc = \
                                            one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                            one_maitre_ouvrage_question_dir_loc[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_question_dir_loc['answers'][
                                                                'answer'] else None

                                    # courriel_maitre_ouvrage_dir_loc
                                    elif id == '111':
                                        courriel_maitre_ouvrage_dir_loc = \
                                            one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                            one_maitre_ouvrage_question_dir_loc[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_question_dir_loc['answers'][
                                                                'answer'] else None


                                """( 1.5) Maitre de l'ouvrage ou mandataire - Entreprise / Bureau d'ingÃ©nieur """
                                section_maitre_ouvrage_entreprise  = [sec for sec in section if sec['@id'] == '2']
                                section_maitre_ouvrage_entreprise = section_maitre_ouvrage_entreprise[0] if len(section_maitre_ouvrage_entreprise) > 0 else None

                                maitre_ouvrage_entreprise_question = \
                                section_maitre_ouvrage_entreprise['questions'][
                                    'question'] if section_maitre_ouvrage_entreprise and 'questions' in section_requerant_entreprise and 'question' in \
                                                   section_maitre_ouvrage_entreprise[
                                                       'questions'] else None

                                for one_maitre_ouvrage_entreprise_question in maitre_ouvrage_entreprise_question:
                                    id = one_maitre_ouvrage_entreprise_question['@id']

                                    # rue_maitre_ouvrage_entreprise
                                    if id == '2':
                                        rue_maitre_ouvrage_entreprise = \
                                            one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'][
                                                                'answer'] else None

                                    # localite_maitre_ouvrage_entreprise
                                    elif id == '3':
                                        localite_maitre_ouvrage_entreprise = \
                                            one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'][
                                                                'answer'] else None

                                    # telephone_maitre_ouvrage_entreprise
                                    elif id == '4':
                                        telephone_maitre_ouvrage_entreprise = \
                                            one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'][
                                                                'answer'] else None

                                    # fax_maitre_ouvrage_entreprise
                                    elif id == '5':
                                        fax_maitre_ouvrage_entreprise = \
                                            one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'][
                                                                'answer'] else None

                                    # courriel_maitre_ouvrage_entreprise
                                    elif id == '6':
                                        courriel_maitre_ouvrage_entreprise = \
                                            one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'][
                                                                'answer'] else None

                                    # nom_maitre_ouvrage_entreprise
                                    elif id == '1':
                                        nom_maitre_ouvrage_entreprise = \
                                            one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'][
                                                                'answer'] else None


                                """( 1.6) Facturation """
                                section_facturation  = [sec for sec in section if sec['@id'] == '4']
                                section_facturation = section_facturation[0] if len(section_facturation) > 0 else None

                                facturation_question = \
                                    section_facturation['questions'][
                                        'question'] if section_facturation and 'questions' in section_facturation and 'question' in \
                                                       section_facturation['questions'] else None

                                if section_facturation:
                                    id = section_facturation['@id']

                                    # adresse_facturation
                                    if id == '4':
                                        adresse_facturation = \
                                            section_facturation['answers']['answer'][
                                                'value'] if 'answers' in section_facturation and 'answer' in \
                                                            section_facturation[
                                                                'answers'] and 'value' in \
                                                            section_facturation['answers'][
                                                                'answer'] else None


                                """( 1.7) Localisation et période """
                                section_loc_periode  = [sec for sec in section if sec['@id'] == '52']
                                section_loc_periode = section_loc_periode[0] if len(section_loc_periode) > 0 else None
                                loc_periode_question = \
                                    section_loc_periode['questions'][
                                        'question'] if section_loc_periode and 'questions' in section_loc_periode and 'question' in \
                                                       section_loc_periode['questions'] else None

                                for one_loc_periode_question in loc_periode_question:
                                    id = one_loc_periode_question['@id']

                                    # commune
                                    if id == '12':
                                        commune = \
                                            one_loc_periode_question['answers']['answer'][
                                                'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                            one_loc_periode_question[
                                                                'answers'] and 'value' in \
                                                            one_loc_periode_question['answers'][
                                                                'answer'] else None

                                    # coordonnee_x
                                    elif id == '94':
                                        coordonnee_x = \
                                            one_loc_periode_question['answers']['answer'][
                                                'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                            one_loc_periode_question[
                                                                'answers'] and 'value' in \
                                                            one_loc_periode_question['answers'][
                                                                'answer'] else None

                                    elif id == '95':
                                        coordonnee_y = \
                                            one_loc_periode_question['answers']['answer'][
                                                'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                            one_loc_periode_question[
                                                                'answers'] and 'value' in \
                                                            one_loc_periode_question['answers'][
                                                                'answer'] else None

                                    elif id == '96':
                                        cadastre = \
                                            one_loc_periode_question['answers']['answer'][
                                                'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                            one_loc_periode_question[
                                                                'answers'] and 'value' in \
                                                            one_loc_periode_question['answers'][
                                                                'answer'] else None

                                    # num_bien_fonds
                                    elif id == '97':
                                        num_bien_fonds = \
                                        one_loc_periode_question['answers']['answer'][
                                            'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                        one_loc_periode_question[
                                                            'answers'] and 'value' in \
                                                        one_loc_periode_question['answers'][
                                                            'answer'] else None

                                    # lieu_dit
                                    elif id == '99':
                                        lieu_dit = \
                                            one_loc_periode_question['answers']['answer'][
                                                'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                            one_loc_periode_question[
                                                                'answers'] and 'value' in \
                                                            one_loc_periode_question['answers'][
                                                                'answer'] else None

                                    # geometry_collection
                                    elif id == '213':
                                        geometry_collection = \
                                            one_loc_periode_question['answers']['answer'][
                                                'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                            one_loc_periode_question[
                                                                'answers'] and 'value' in \
                                                            one_loc_periode_question['answers'][
                                                                'answer'] else None

                                    # service_a_appliquer
                                    elif id == '242':
                                        service_a_appliquer = \
                                            one_loc_periode_question['answers']['answer'][
                                                'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                            one_loc_periode_question[
                                                                'answers'] and 'value' in \
                                                            one_loc_periode_question['answers'][
                                                                'answer'] else None


                            # Evenement model
                            evenement_model = models.Evenement(
                                id_entite=cls.settings['id_entite_xml_import'],
                                id_responsable=cls.settings['id_responsable_xml_import'],
                                type=int(cls.settings['autre_evenement_id']),
                                libelle=cause_fouille,
                                date_debut=datetime.datetime.strptime(date_debut,cls.settings['xml_date_template']),
                                heure_debut=heure_debut,
                                date_fin=datetime.datetime.strptime(date_fin,cls.settings['xml_date_template']),
                                heure_fin=heure_fin,
                                id_utilisateur_ajout=cls.settings['id_user_ajout_xml_import'],
                                id_utilisateur_modification=cls.settings['id_user_ajout_xml_import'],
                                numero_dossier=Utils.generate_numero_dossier(cls.request,
                                                                             int(cls.settings['autre_evenement_id'])),
                                localisation=commune
                            )

                            if evenement_model:
                                cls.request.dbsession.add(evenement_model)
                                cls.request.dbsession.flush()
                                max_event_id = evenement_model.id

                                # Autre evenement model
                                autre_ev_model = models.AutreEvenement(
                                    id_evenement = max_event_id,
                                    cause = cause_fouille,
                                    nom_maitre_ouvrage = nom_maitre_ouvrage_entreprise,
                                    rue_maitre_ouvrage = rue_maitre_ouvrage_entreprise,
                                    localite_maitre_ouvrage=localite_maitre_ouvrage_entreprise,
                                    telephone_maitre_ouvrage=telephone_maitre_ouvrage_entreprise,
                                    fax_maitre_ouvrage=fax_maitre_ouvrage_entreprise,
                                    courriel_maitre_ouvrage=courriel_maitre_ouvrage_entreprise,
                                    nom_direction_locale=nom_maitre_ouvrage_dir_loc,
                                    prenom_direction_locale=prenom_maitre_ouvrage_dir_loc,
                                    mobile_direction_locale=mobile_maitre_ouvrage_dir_loc,
                                    telephone_direction_locale=telephone_maitre_ouvrage_dir_loc,
                                    fax_direction_locale=fax_maitre_ouvrage_dir_loc,
                                    courriel_direction_locale=courriel_maitre_ouvrage_dir_loc,
                                    nom_entrepreneur=nom_requerant_entreprise,
                                    rue_entrepreneur=rue_requerant_entreprise,
                                    localite_entrepreneur=localite_requerant_entreprise,
                                    telephone_entrepreneur=telephone_requerant_entreprise,
                                    fax_entrepreneur=fax_requerant_entreprise,
                                    courriel_entrepreneur=courriel_requerant_entreprise,
                                    nom_responsable_travaux=nom_requerant_personne,
                                    prenom_responsable_travaux=prenom_requerant_personne,
                                    mobile_responsable_travaux=mobile_requerant_personne,
                                    telephone_responsable_travaux=telephone_requerant_personne,
                                    fax_responsable_travaux=fax_requerant_personne,
                                    courriel_responsable_travaux=courriel_requerant_personne
                                    #facturation = Column(Numeric)
                                    #date_debut_valide =
                                    #date_fin_valide =
                                    #date_maj_valide =
                                    #numero_facture =
                                    #date_facture =
                                    #reserve_eventuelle =
                                )

                                cls.request.dbsession.add(autre_ev_model)

                                # Evenement point model
                                """
                                geometry = json.loads(
                                    '{"type":"Point","coordinates":[' + coordonnee_x + ',' + coordonnee_y + ']}')
                                evenement_point_model = models.EvenementPoint(
                                    id_evenement=max_event_id,
                                )
                                evenement_point_model.set_json_geometry(str(geometry), cls.settings['srid'])

                                cls.request.dbsession.add(evenement_point_model)              
                            

                                # Evenement polygon model
                                if geometry_collection is not None:
                                    evenement_polygon_model = models.EvenementPolygone(
                                        id_evenement=max_event_id
                                    )
                                    evenement_polygon_model.set_geometry_collection(str(geometry_collection), cls.settings['srid'])
                                    cls.request.dbsession.add(evenement_polygon_model)
                                """

                                Utils.add_ev_geometries(cls.request, geometry_collection, max_event_id)



                        """------------- (2) Form perturbation ---------------"""
                        perturbations_form = [f for f in form if f['@id'] == '46']
                        perturbations_form = perturbations_form[0] if len(perturbations_form) > 0 else None

                        if perturbations_form:

                            # Type perturbation
                            type_pertubation = None

                            # Heure_fin
                            heure_fin = None

                            # Periode occupation
                            periode_occupation = None

                            # Type occupation
                            type_occupation = None

                            # Occupation durant le week-end
                            occupation_weekend = False

                            # Occupation durant les heures de pointe
                            occupation_heures_pointes = False

                            # Remarque
                            remarque = None

                            # Voie(s) condamnée(s)
                            voies_condamnees = None

                            # Type de régulation
                            type_regulation = None

                            # Nom
                            nom = None

                            # Prénom
                            prenom = None

                            # Mobile
                            mobile = None

                            # Telephone
                            telephone = None

                            # Courriel
                            courriel = None

                            # Date debut
                            date_debut = None

                            # Heure debut
                            heure_debut = None

                            # Date fin
                            date_fin = None

                            # Hauteur gabarit
                            hauteur_gabarit = None

                            # Largeur gabarit
                            largeur_gabarit = None

                            # Type fermeture
                            type_fermeture = None

                            # Deviation
                            deviation = None

                            section = perturbations_form['sections'][
                                'section'] if perturbations_form and 'sections' in perturbations_form and 'section' in \
                                              perturbations_form['sections'] else None

                            if section and len(section) > 0:

                                """( 2.1) Type perturbation """
                                section_type_perturbation = [sec for sec in section if
                                                             sec['@id'] == '42']
                                section_type_perturbation = section_type_perturbation[0] if len(
                                    section_type_perturbation) > 0 else None
                                type_perturbation_question = \
                                    section_type_perturbation['questions'][
                                        'question'] if section_type_perturbation and 'questions' in section_type_perturbation and 'question' in \
                                                       section_type_perturbation['questions'] else None

                                if section_type_perturbation:
                                    id = section_type_perturbation['@id']


                                    # type_pertubation
                                    if id == '42':
                                        type_pertubation = \
                                            type_perturbation_question['answers']['answer'][
                                                'value'] if 'answers' in type_perturbation_question and 'answer' in \
                                                            type_perturbation_question[
                                                                'answers'] and 'value' in \
                                                            type_perturbation_question['answers'][
                                                                'answer'] else None
                                        if type_pertubation == "Occupation":
                                            type_pertubation = int(cls.settings['occupation_perturbation_id'])
                                        elif type_pertubation == "Fermeture":
                                            type_pertubation = int(cls.settings['fermeture_perturbation_id'])
                                        else:
                                            type_pertubation = None

                                """(2.2) Occupation"""
                                section_occupation = [sec for sec in section if
                                                      sec['@id'] == '41']
                                section_occupation = section_occupation[0] if len(
                                    section_occupation) > 0 else None

                                if type_pertubation == int(
                                        cls.settings['occupation_perturbation_id']) and section_occupation:
                                    occupation_question = \
                                        section_occupation['questions'][
                                            'question'] if section_occupation and 'questions' in section_occupation and 'question' in \
                                                           section_occupation['questions'] else None

                                    for one_occupation_question in occupation_question:
                                        id = one_occupation_question['@id']


                                        # occupation_heures_pointes
                                        if id == '20':
                                            occupation_heures_pointes = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                            occupation_heures_pointes = True if occupation_heures_pointes is not None and occupation_heures_pointes.upper() == "OUI" else occupation_heures_pointes
                                            occupation_heures_pointes = False if occupation_heures_pointes is not None and occupation_heures_pointes != True and occupation_heures_pointes.upper() == "NON" else None

                                        # occupation_weekend
                                        elif id == '21':
                                            occupation_weekend = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                            occupation_weekend = True if occupation_weekend is not None and occupation_weekend.upper() == "OUI" else occupation_weekend
                                            occupation_weekend = False if occupation_weekend is not None and occupation_weekend != True and occupation_weekend.upper() == "NON" else None


                                        # remarque
                                        elif id == '24':
                                            remarque = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                       # nom
                                        elif id == '100':
                                            nom = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # prenom
                                        elif id == '101':
                                            prenom = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # mobile
                                        elif id == '102':
                                            mobile = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # telephone
                                        elif id == '103':
                                            telephone = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # courriel
                                        elif id == '105':
                                            courriel = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # date_debut
                                        elif id == '121':
                                            date_debut = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                            date_debut = date_debut.replace(".", "-") if date_debut else None

                                        # heure_debut
                                        elif id == '122':
                                            heure_debut = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                            heure_debut = heure_debut.replace(".", ":").replace("h",
                                                                                                ":") if heure_debut else None
                                            heure_debut = heure_debut + ":00" if heure_debut and len(
                                                heure_debut) <= 2 else heure_debut
                                            heure_debut = "0" + heure_debut if heure_debut and len(
                                                heure_debut) == 3 else heure_debut

                                        # date_fin
                                        elif id == '123':
                                            date_fin = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                            date_fin = date_fin.replace(".", "-") if date_fin else None

                                        # heure_fin
                                        elif id == '124':
                                            heure_fin = \
                                            one_occupation_question['answers']['answer'][
                                                'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                            one_occupation_question[
                                                                'answers'] and 'value' in \
                                                            one_occupation_question['answers'][
                                                                'answer'] else None
                                            heure_fin = heure_fin.replace(".", ":").replace("h",
                                                                                            ":") if heure_fin else None
                                            heure_fin = heure_fin + ":00" if heure_fin and len(
                                                heure_fin) <= 2 else heure_fin
                                            heure_fin = "0" + heure_fin if heure_fin and len(
                                                heure_fin) == 3 else heure_fin

                                        # periode_occupation
                                        elif id == '126':
                                            periode_occupation = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # type_occupation
                                        elif id == '127':
                                            type_occupation = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # voies_condamnees
                                        elif id == '128':
                                            voies_condamnees = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # type_regulation
                                        elif id == '129':
                                            type_regulation = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # hauteur_gabarit
                                        elif id == '130':
                                            hauteur_gabarit = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # largeur_gabarit
                                        elif id == '131':
                                            largeur_gabarit = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                """(2.2) Fermeture"""
                                section_fermeture = [sec for sec in section if
                                                     sec['@id'] == '43']
                                section_fermeture = section_fermeture[0] if len(
                                    section_fermeture) > 0 else None

                                if type_pertubation == int(
                                        cls.settings['fermeture_perturbation_id']) and section_fermeture:
                                    fermeture_question = \
                                        section_fermeture['questions'][
                                            'question'] if section_fermeture and 'questions' in section_fermeture and 'question' in \
                                                           section_fermeture['questions'] else None

                                    for one_fermeture_question in fermeture_question:
                                        id = one_fermeture_question['@id']

                                        #remarque
                                        if id == '24':
                                            remarque = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None


                                        # nom
                                        elif id == '100':
                                            nom = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # prenom
                                        elif id == '101':
                                            prenom = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # mobile
                                        elif id == '102':
                                            mobile = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # telephone
                                        elif id == '103':
                                            telephone = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # courriel
                                        elif id == '105':
                                            courriel = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # date_debut
                                        elif id == '121':
                                            date_debut = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None
                                            date_debut = date_debut.replace(".", "-") if date_debut else None

                                        # heure_debut
                                        elif id == '122':
                                            heure_debut = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None
                                            heure_debut = heure_debut.replace(".", ":").replace("h",
                                                                                                ":") if heure_debut else None
                                            heure_debut = heure_debut + ":00" if heure_debut and len(
                                                heure_debut) <= 2 else heure_debut
                                            heure_debut = "0" + heure_debut if heure_debut and len(
                                                heure_debut) == 3 else heure_debut

                                        # date_fin
                                        elif id == '123':
                                            date_fin = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None
                                            date_fin = date_fin.replace(".", "-") if date_fin else None

                                        # heure_fin
                                        elif id == '124':
                                            heure_fin = \
                                            one_fermeture_question['answers']['answer'][
                                                'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                            one_fermeture_question[
                                                                'answers'] and 'value' in \
                                                            one_fermeture_question['answers'][
                                                                'answer'] else None
                                            heure_fin = heure_fin.replace(".", ":").replace("h",
                                                                                            ":") if heure_fin else None
                                            heure_fin = heure_fin + ":00" if heure_fin and len(
                                                heure_fin) <= 2 else heure_fin
                                            heure_fin = "0" + heure_fin if heure_fin and len(
                                                heure_fin) == 3 else heure_fin

                                        # type_fermeture
                                        elif id == '132':
                                            type_fermeture = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None


                                        # deviation
                                        elif id == '133':
                                            deviation = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                # Check date_debut, if less than 24h, urgence=true
                                urgence = False
                                if date_debut != None and heure_debut != None:
                                    date_time_str = str(date_debut) + ' ' + str(heure_debut)
                                    date_time_obj = datetime.datetime.strptime(date_time_str,
                                                                               cls.settings['xml_date_template'] + ' ' + cls.settings['xml_heure_template'])
                                    now = datetime.datetime.now()

                                    if date_time_obj >= now and date_time_obj <= now + datetime.timedelta(days=1):
                                        urgence = True

                                perturbation_model = models.Perturbation(
                                    id_evenement=max_event_id,
                                    type=type_pertubation,
                                    # description=description,
                                    date_debut=datetime.datetime.strptime(date_debut,cls.settings['xml_date_template']),
                                    heure_debut=heure_debut,
                                    date_fin=datetime.datetime.strptime(date_fin,cls.settings['xml_date_template']),
                                    heure_fin=heure_fin,
                                    nom_responsable_trafic=nom,
                                    prenom_responsable_trafic=prenom,
                                    mobile_responsable_trafic=mobile,
                                    telephone_responsable_trafic=telephone,
                                    # fax_responsable_trafic=fax,
                                    courriel_responsable_trafic=courriel,
                                    remarque=remarque,
                                    id_utilisateur_ajout=cls.settings['id_user_ajout_xml_import'],
                                    id_utilisateur_modification=cls.settings['id_user_ajout_xml_import'],
                                    urgence=urgence,
                                    etat=cls.settings['perturbation_etat_acceptee_code'] if urgence == True else cls.settings['perturbation_etat_attente_code']
                                )

                                if perturbation_model:
                                    cls.request.dbsession.add(perturbation_model)
                                    cls.request.dbsession.flush()
                                    max_perturbation_id = perturbation_model.id

                                    # Occupation
                                    if type_pertubation == int(
                                            cls.settings['occupation_perturbation_id']) and section_fermeture:
                                        occupation_model = models.Occupation(
                                            id_perturbation=max_perturbation_id,
                                            id_responsable_regulation=cls.settings['id_responsable_xml_import'],
                                            type_occupation=type_occupation,
                                            type_regulation=type_regulation,
                                            voies_condamnees=voies_condamnees,
                                            largeur_gabarit=largeur_gabarit,
                                            hauteur_gabarit=hauteur_gabarit,
                                            heure_pointe=occupation_heures_pointes,
                                            week_end=occupation_weekend)
                                        cls.request.dbsession.add(occupation_model)

                                    #Fermeture
                                    elif type_pertubation == int(
                                            cls.settings['fermeture_perturbation_id']) and section_fermeture:
                                        fermeture_model = models.Fermeture(
                                            id_perturbation=max_perturbation_id,
                                            deviation=deviation,
                                            id_responsable=cls.settings['id_responsable_xml_import'])
                                        cls.request.dbsession.add(fermeture_model)

                                    # Geometries
                                    Utils.add_perturb_geometries(cls.request, geometry_collection,
                                                                 max_perturbation_id)

                # Commit transaction
                transaction.commit()


        except Exception as e:
            # transaction.abort()
            cls.request.dbsession.rollback()
            raise e
            return False

        return True





    @classmethod
    def add_file_data_fouille(cls, dossier):
        try:

            max_event_id = None
            with transaction.manager:
                cls.request.dbsession.execute('set search_path to ' + cls.settings['schema_name'])

                if dossier:

                    # libelle
                    title = dossier['title'] if 'title' in dossier else None

                    # description
                    description = dossier['descriptions'][
                        'descr_lib'] if 'descriptions' in dossier and 'descr_lib' in dossier[
                        'descriptions'] else None

                    # Date debut
                    date_debut = None

                    # Heure debut
                    heure_debut = None

                    # Date fin
                    date_fin = None

                    # Heure fin
                    heure_fin = None

                    # Surface
                    surface = None

                    # Longueur_etape
                    longueur_etape = None

                    # Cause de la fouille
                    cause_fouille = None

                    # Description fouille
                    description_fouille = None

                    # Adresse de la fouille
                    adresse_fouille = None

                    # Rue requerant entreprise
                    rue_requerant_entreprise = None

                    # Localite requerant entreprise
                    localite_requerant_entreprise = None

                    # Telephone requerant entreprise
                    telephone_requerant_entreprise = None

                    # Fax requerant entreprise
                    fax_requerant_entreprise = None

                    # Courriel requerant entreprise
                    courriel_requerant_entreprise = None

                    # Nom requerant entreprise
                    nom_requerant_entreprise = None

                    # Nom requerant personne
                    nom_requerant_personne = None

                    # Prenom requerant personne
                    prenom_requerant_personne = None

                    # Mobile requerant personne
                    mobile_requerant_personne = None

                    # Telephone requerant personne
                    telephone_requerant_personne = None

                    # Fax requerant personne
                    fax_requerant_personne = None

                    # Courriel requerant personne
                    courriel_requerant_personne = None

                    # Nom maitre ouvrage direction locale
                    nom_maitre_ouvrage_dir_loc = None

                    # Prenom maitre ouvrage direction locale
                    prenom_maitre_ouvrage_dir_loc = None

                    # Mobile maitre ouvrage direction locale
                    mobile_maitre_ouvrage_dir_loc = None

                    # Telephone maitre ouvrage direction locale
                    telephone_maitre_ouvrage_dir_loc = None

                    # Fax maitre ouvrage direction locale
                    fax_maitre_ouvrage_dir_loc = None

                    # Courriel maitre ouvrage direction locale
                    courriel_maitre_ouvrage_dir_loc = None

                    # Rue maitre ouvrage entreprise
                    rue_maitre_ouvrage_entreprise = None

                    # Localite maitre ouvrage entreprise
                    localite_maitre_ouvrage_entreprise = None

                    # Telephone maitre ouvrage entreprise
                    telephone_maitre_ouvrage_entreprise = None

                    # Fax maitre ouvrage entreprise
                    fax_maitre_ouvrage_entreprise = None

                    # Courriel maitre ouvrage entreprise
                    courriel_maitre_ouvrage_entreprise = None

                    # Nom maitre ouvrage entreprise
                    nom_maitre_ouvrage_entreprise = None

                    # Nom / Raison sociale entrepreneur entreprise
                    nom_entrepreneur_entreprise = None

                    # Rue et numéro sociale entrepreneur entreprise
                    rue_entrepreneur_entreprise = None

                    # NPA et localité entrepreneur entreprise
                    npa_localite_entrepreneur_entreprise = None

                    # N° de téléphonee entrepreneur entreprise
                    telephone_entrepreneur_entreprise = None

                    # N° de fax entrepreneur entreprise
                    fax_entrepreneur_entreprise = None

                    # Courriel entrepreneur entreprise
                    courriel_entrepreneur_entreprise = None

                    # Nom entrepreneur responsable travaux
                    nom_entrepreneur_responsable_travaux = None

                    # Prenom entrepreneur responsable travaux
                    prenom_entrepreneur_responsable_travaux = None

                    # Mobile entrepreneur responsable travaux
                    mobile_entrepreneur_responsable_travaux = None

                    # Telephone entrepreneur responsable travaux
                    telephone_entrepreneur_responsable_travaux = None

                    # Fax entrepreneur responsable travaux
                    fax_entrepreneur_responsable_travaux = None

                    # Courriel entrepreneur responsable travaux
                    courriel_entrepreneur_responsable_travaux = None


                    # Adresse facturation
                    adresse_facturation = None

                    # Num bien-fonds
                    num_bien_fonds = None

                    # Commune
                    commune = None

                    # Coordonnee X
                    coordonnee_x = None

                    # Coordonnee Y
                    coordonnee_y = None

                    # Geometry collection
                    geometry_collection = None

                    # Cadastre
                    cadastre = None

                    # Lieu dit
                    lieu_dit = None

                    # Service à appliquer
                    service_a_appliquer = None

                    form = dossier['forms']['form'] if 'forms' in dossier and 'form' in dossier[
                        'forms'] else None

                    if form and len(form) > 0:

                        """------------- (1) Form evenement ---------------"""
                        evenement_form = [f for f in form if f['@id'] == '1']
                        evenement_form = evenement_form[0] if len(evenement_form) > 0 else None

                        if evenement_form:

                            section = evenement_form['sections'][
                                'section'] if 'sections' in evenement_form and 'section' in evenement_form[
                                'sections'] else None

                            if section and len(section) > 0:

                                """( 1.1) Info evenement """
                                # date_debut, heure_debut, date_fin, heure_fin, surface ....
                                section_evenement = [sec for sec in section if sec['@id'] == '44']
                                section_evenement = section_evenement[0] if len(section_evenement) > 0 else None

                                evenement_question = section_evenement['questions'][
                                    'question'] if section_evenement and 'questions' in section_evenement and 'question' in \
                                                   section_evenement['questions'] else None

                                for one_evenement_question in evenement_question:
                                    id = one_evenement_question['@id']


                                    # date_debut
                                    if id == '121':
                                        date_debut = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None
                                        date_debut = date_debut.replace(".", "-") if date_debut else None

                                    # heure_debut
                                    elif id == '122':
                                        heure_debut = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None
                                        heure_debut = heure_debut.replace(".", ":").replace("h",
                                                                                            ":") if heure_debut else None
                                        heure_debut = heure_debut + ":00" if heure_debut and len(
                                            heure_debut) <= 2 else heure_debut
                                        heure_debut = "0" + heure_debut if heure_debut and len(
                                            heure_debut) == 3 else heure_debut

                                    # date_fin
                                    elif id == '123':
                                        date_fin = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None
                                        date_fin = date_fin.replace(".", "-") if date_fin else None


                                    # heure_fin
                                    elif id == '124':
                                        heure_fin = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None
                                        heure_fin = heure_fin.replace(".", ":").replace("h",
                                                                                        ":") if heure_fin else None
                                        heure_fin = heure_fin + ":00" if heure_fin and len(
                                            heure_fin) <= 2 else heure_fin
                                        heure_fin = "0" + heure_fin if heure_fin and len(
                                            heure_fin) == 3 else heure_fin


                                    # cause_fouille
                                    elif id == '134':
                                        cause_fouille = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None

                                    # description_fouille
                                    elif id == '135':
                                        description_fouille = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None

                                    # adresse_fouille
                                    elif id == '201':

                                        adresse_fouille = one_evenement_question['answers']['answer'][
                                            'value'] if 'answers' in one_evenement_question and 'answer' in \
                                                        one_evenement_question['answers'] and 'value' in \
                                                        one_evenement_question['answers']['answer'] else None



                                """( 1.2) Reque©rant - Entreprise / Service / Commune """
                                section_requerant_entreprise = [sec for sec in section if sec['@id'] == '1']
                                section_requerant_entreprise = section_requerant_entreprise[0] if len(section_requerant_entreprise) > 0 else None

                                requerant_entreprise_question = section_requerant_entreprise['questions'][
                                    'question'] if section_requerant_entreprise and 'questions' in section_requerant_entreprise and 'question' in \
                                                   section_requerant_entreprise['questions'] else None

                                for one_requerant_entreprise_question in requerant_entreprise_question:
                                    id = one_requerant_entreprise_question['@id']

                                    # nom_requerant_entreprise
                                    if id == '1':
                                        nom_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None


                                    # rue_requerant_entreprise
                                    elif id == '2':
                                        rue_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None

                                    # localite_requerant_entreprise
                                    elif id == '3':
                                        localite_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None

                                    # telephone_requerant_entreprise
                                    elif id == '4':
                                        telephone_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None

                                    # fax_requerant_entreprise
                                    elif id == '5':
                                        fax_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None


                                    # courriel_requerant_entreprise
                                    elif id == '6':
                                        courriel_requerant_entreprise = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_entreprise_question and 'answer' in \
                                                        one_requerant_entreprise_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_entreprise_question['answers'][
                                                            'answer'] else None


                                """( 1.3) Reque©rant - Personne de contact """
                                section_requerant_personne = [sec for sec in section if sec['@id'] == '32']
                                section_requerant_personne = section_requerant_personne[0] if len(section_requerant_personne) > 0 else None

                                requerant_personne_question = section_requerant_personne['questions'][
                                    'question'] if section_requerant_personne and 'questions' in section_requerant_personne and 'question' in \
                                                   section_requerant_personne['questions'] else None

                                for one_requerant_personne_question in requerant_personne_question:
                                    id = one_requerant_personne_question['@id']

                                    # nom_requerant_personne
                                    if id == '100':
                                        nom_requerant_personne = \
                                        one_requerant_personne_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                        one_requerant_personne_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_personne_question['answers'][
                                                            'answer'] else None

                                    # prenom_requerant_personne
                                    elif id == '101':
                                        prenom_requerant_personne = \
                                            one_requerant_personne_question['answers']['answer'][
                                                'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                            one_requerant_personne_question[
                                                                'answers'] and 'value' in \
                                                            one_requerant_personne_question['answers'][
                                                                'answer'] else None

                                    #mobile_requerant_personne
                                    elif id == '102':
                                        mobile_requerant_personne = \
                                            one_requerant_personne_question['answers']['answer'][
                                                'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                            one_requerant_personne_question[
                                                                'answers'] and 'value' in \
                                                            one_requerant_personne_question['answers'][
                                                                'answer'] else None

                                    # one_requerant_personne_question
                                    elif id == '103':
                                        one_requerant_personne_question = \
                                        one_requerant_entreprise_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                        one_requerant_personne_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_personne_question['answers'][
                                                            'answer'] else None

                                    # fax_requerant_personne
                                    elif id == '104':
                                        fax_requerant_personne = \
                                            one_requerant_personne_question['answers']['answer'][
                                                'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                            one_requerant_personne_question[
                                                                'answers'] and 'value' in \
                                                            one_requerant_personne_question['answers'][
                                                                'answer'] else None

                                    # courriel_requerant_personne
                                    elif id == '105':
                                        courriel_requerant_personne = \
                                        one_requerant_personne_question['answers']['answer'][
                                            'value'] if 'answers' in one_requerant_personne_question and 'answer' in \
                                                        one_requerant_personne_question[
                                                            'answers'] and 'value' in \
                                                        one_requerant_personne_question['answers'][
                                                            'answer'] else None


                                    """( 1.4) Maitre de l'ouvrage ou mandataire - Entreprise / Bureau d'ingÃ©nieur """
                                    section_maitre_ouvrage_entreprise = [sec for sec in section if sec['@id'] == '2']
                                    section_maitre_ouvrage_entreprise = section_maitre_ouvrage_entreprise[0] if len(section_maitre_ouvrage_entreprise) > 0 else None

                                    maitre_ouvrage_entreprise_question = \
                                        section_maitre_ouvrage_entreprise['questions'][
                                            'question'] if section_maitre_ouvrage_entreprise and 'questions' in section_requerant_entreprise and 'question' in \
                                                           section_maitre_ouvrage_entreprise[
                                                               'questions'] else None

                                    for one_maitre_ouvrage_entreprise_question in maitre_ouvrage_entreprise_question:
                                        id = one_maitre_ouvrage_entreprise_question['@id']

                                        # nom_maitre_ouvrage_entreprise
                                        if id == '1':
                                            nom_maitre_ouvrage_entreprise = \
                                            one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_entreprise_question[
                                                                'answers'][
                                                                'answer'] else None


                                        # rue_maitre_ouvrage_entreprise
                                        elif id == '2':
                                            rue_maitre_ouvrage_entreprise = \
                                                one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'][
                                                                    'answer'] else None

                                        # localite_maitre_ouvrage_entreprise
                                        elif id == '3':
                                            localite_maitre_ouvrage_entreprise = \
                                                one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'][
                                                                    'answer'] else None

                                        # telephone_maitre_ouvrage_entreprise
                                        elif id == '4':
                                            telephone_maitre_ouvrage_entreprise = \
                                                one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'][
                                                                    'answer'] else None

                                        # fax_maitre_ouvrage_entreprise
                                        elif id == '5':
                                            fax_maitre_ouvrage_entreprise = \
                                                one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'][
                                                                    'answer'] else None


                                        # courriel_maitre_ouvrage_entreprise
                                        elif id == '6':
                                            courriel_maitre_ouvrage_entreprise = \
                                                one_maitre_ouvrage_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_entreprise_question and 'answer' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_entreprise_question[
                                                                    'answers'][
                                                                    'answer'] else None


                                    """( 1.5) Maitre de l'ouvrage ou mandataire - Direction locale """
                                    section_maitre_ouvrage_dir_loc = [sec for sec in section if sec['@id'] == '33']
                                    section_maitre_ouvrage_dir_loc = section_maitre_ouvrage_dir_loc[0] if len(section_maitre_ouvrage_dir_loc) > 0 else None

                                    maitre_ouvrage_question_dir_loc = \
                                    section_maitre_ouvrage_dir_loc['questions'][
                                        'question'] if section_maitre_ouvrage_dir_loc and 'questions' in section_maitre_ouvrage_dir_loc and 'question' in \
                                                       section_maitre_ouvrage_dir_loc['questions'] else None

                                    for one_maitre_ouvrage_question_dir_loc in maitre_ouvrage_question_dir_loc:
                                        id = one_maitre_ouvrage_question_dir_loc['@id']


                                        # nom_maitre_ouvrage_dir_loc
                                        if id == '106':
                                            nom_maitre_ouvrage_dir_loc = \
                                            one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                            one_maitre_ouvrage_question_dir_loc[
                                                                'answers'] and 'value' in \
                                                            one_maitre_ouvrage_question_dir_loc['answers'][
                                                                'answer'] else None

                                        # prenom_maitre_ouvrage_dir_loc
                                        elif id == '107':
                                            prenom_maitre_ouvrage_dir_loc = \
                                                one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                                one_maitre_ouvrage_question_dir_loc[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_question_dir_loc['answers'][
                                                                    'answer'] else None

                                        # mobile_maitre_ouvrage_dir_loc
                                        elif id == '108':
                                            mobile_maitre_ouvrage_dir_loc = \
                                                one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                                one_maitre_ouvrage_question_dir_loc[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_question_dir_loc['answers'][
                                                                    'answer'] else None

                                        # telephone_maitre_ouvrage_dir_loc
                                        elif id == '109':
                                            telephone_maitre_ouvrage_dir_loc = \
                                                one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                                one_maitre_ouvrage_question_dir_loc[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_question_dir_loc['answers'][
                                                                    'answer'] else None

                                        # fax_maitre_ouvrage_dir_loc
                                        elif id == '110':
                                            fax_maitre_ouvrage_dir_loc = \
                                                one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                                one_maitre_ouvrage_question_dir_loc[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_question_dir_loc['answers'][
                                                                    'answer'] else None

                                        # courriel_maitre_ouvrage_dir_loc
                                        elif id == '111':
                                            courriel_maitre_ouvrage_dir_loc = \
                                                one_maitre_ouvrage_question_dir_loc['answers']['answer'][
                                                    'value'] if 'answers' in one_maitre_ouvrage_question_dir_loc and 'answer' in \
                                                                one_maitre_ouvrage_question_dir_loc[
                                                                    'answers'] and 'value' in \
                                                                one_maitre_ouvrage_question_dir_loc['answers'][
                                                                    'answer'] else None

                                    """( 1.6) Entrepreneur agréé - Entreprise """
                                    section_entrepreneur_entreprise = [sec for sec in section if sec['@id'] == '3']
                                    section_entrepreneur_entreprise = section_entrepreneur_entreprise[0] if len(section_entrepreneur_entreprise) > 0 else None

                                    entrepreneur_entreprise_question = \
                                        section_entrepreneur_entreprise['questions'][
                                            'question'] if section_entrepreneur_entreprise and 'questions' in section_entrepreneur_entreprise and 'question' in \
                                                           section_entrepreneur_entreprise['questions'] else None


                                    for one_entrepreneur_entreprise_question in entrepreneur_entreprise_question:
                                        id = one_entrepreneur_entreprise_question['@id']

                                        # nom_entrepreneur_entreprise
                                        if id == '1':
                                            nom_entrepreneur_entreprise = \
                                            one_entrepreneur_entreprise_question['answers']['answer'][
                                                'value'] if 'answers' in one_entrepreneur_entreprise_question and 'answer' in \
                                                            one_entrepreneur_entreprise_question[
                                                                'answers'] and 'value' in \
                                                            one_entrepreneur_entreprise_question['answers'][
                                                                'answer'] else None

                                        # rue_entrepreneur_entreprise
                                        if id == '2':
                                            rue_entrepreneur_entreprise = \
                                                one_entrepreneur_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_entrepreneur_entreprise_question and 'answer' in \
                                                                one_entrepreneur_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_entrepreneur_entreprise_question['answers'][
                                                                    'answer'] else None

                                        # npa_localite_entrepreneur_entreprise
                                        if id == '3':
                                            npa_localite_entrepreneur_entreprise = \
                                                one_entrepreneur_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_entrepreneur_entreprise_question and 'answer' in \
                                                                one_entrepreneur_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_entrepreneur_entreprise_question['answers'][
                                                                    'answer'] else None

                                        # telephone_entrepreneur_entreprise
                                        if id == '4':
                                            telephone_entrepreneur_entreprise = \
                                                one_entrepreneur_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_entrepreneur_entreprise_question and 'answer' in \
                                                                one_entrepreneur_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_entrepreneur_entreprise_question['answers'][
                                                                    'answer'] else None

                                        # fax_entrepreneur_entreprise
                                        if id == '5':
                                            fax_entrepreneur_entreprise = \
                                                one_entrepreneur_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_entrepreneur_entreprise_question and 'answer' in \
                                                                one_entrepreneur_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_entrepreneur_entreprise_question['answers'][
                                                                    'answer'] else None

                                        # courriel_entrepreneur_entreprise
                                        if id == '6':
                                            courriel_entrepreneur_entreprise = \
                                                one_entrepreneur_entreprise_question['answers']['answer'][
                                                    'value'] if 'answers' in one_entrepreneur_entreprise_question and 'answer' in \
                                                                one_entrepreneur_entreprise_question[
                                                                    'answers'] and 'value' in \
                                                                one_entrepreneur_entreprise_question['answers'][
                                                                    'answer'] else None

                                    """( 1.7) Entrepreneur agréé - Responsable des travaux """
                                    section_entrepreneur_resp_travaux = [sec for sec in section if sec['@id'] == '34']
                                    section_entrepreneur_resp_travaux = section_entrepreneur_resp_travaux[0] if len(section_entrepreneur_resp_travaux) > 0 else None

                                    section_entrepreneur_resp_travaux_question = \
                                        section_entrepreneur_resp_travaux['questions'][
                                            'question'] if section_entrepreneur_resp_travaux and 'questions' in section_entrepreneur_resp_travaux and 'question' in \
                                                           section_entrepreneur_resp_travaux['questions'] else None

                                    for one_section_entrepreneur_resp_travaux_question in section_entrepreneur_resp_travaux_question:
                                        id = one_section_entrepreneur_resp_travaux_question['@id']


                                        # nom_entrepreneur_responsable_travaux
                                        if id == '112':
                                            nom_entrepreneur_responsable_travaux = \
                                            one_section_entrepreneur_resp_travaux_question['answers']['answer'][
                                                'value'] if 'answers' in one_section_entrepreneur_resp_travaux_question and 'answer' in \
                                                            one_section_entrepreneur_resp_travaux_question[
                                                                'answers'] and 'value' in \
                                                            one_section_entrepreneur_resp_travaux_question['answers'][
                                                                'answer'] else None

                                        # prenom_entrepreneur_responsable_travaux
                                        if id == '113':
                                            prenom_entrepreneur_responsable_travaux = \
                                                one_section_entrepreneur_resp_travaux_question['answers']['answer'][
                                                    'value'] if 'answers' in one_section_entrepreneur_resp_travaux_question and 'answer' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'] and 'value' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'][
                                                                    'answer'] else None

                                        # mobile_entrepreneur_responsable_travaux
                                        if id == '114':
                                            mobile_entrepreneur_responsable_travaux = \
                                                one_section_entrepreneur_resp_travaux_question['answers']['answer'][
                                                    'value'] if 'answers' in one_section_entrepreneur_resp_travaux_question and 'answer' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'] and 'value' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'][
                                                                    'answer'] else None

                                        # telephone_entrepreneur_responsable_travaux
                                        if id == '115':
                                            telephone_entrepreneur_responsable_travaux = \
                                                one_section_entrepreneur_resp_travaux_question['answers']['answer'][
                                                    'value'] if 'answers' in one_section_entrepreneur_resp_travaux_question and 'answer' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'] and 'value' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'][
                                                                    'answer'] else None

                                        # fax_entrepreneur_responsable_travaux
                                        if id == '116':
                                            fax_entrepreneur_responsable_travaux = \
                                                one_section_entrepreneur_resp_travaux_question['answers']['answer'][
                                                    'value'] if 'answers' in one_section_entrepreneur_resp_travaux_question and 'answer' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'] and 'value' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'][
                                                                    'answer'] else None

                                        # courriel_entrepreneur_responsable_travaux
                                        if id == '117':
                                            courriel_entrepreneur_responsable_travaux = \
                                                one_section_entrepreneur_resp_travaux_question['answers']['answer'][
                                                    'value'] if 'answers' in one_section_entrepreneur_resp_travaux_question and 'answer' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'] and 'value' in \
                                                                one_section_entrepreneur_resp_travaux_question[
                                                                    'answers'][
                                                                    'answer'] else None


                                    """( 1.8) Facturation """
                                    section_facturation = [sec for sec in section if sec['@id'] == '4']
                                    section_facturation = section_facturation[0] if len(section_facturation) > 0 else None

                                    facturation_question = \
                                        section_facturation['questions'][
                                            'question'] if section_facturation and 'questions' in section_facturation and 'question' in \
                                                           section_facturation['questions'] else None

                                    if section_facturation:
                                        id = section_facturation['@id']

                                        if id == '4':
                                            adresse_facturation = \
                                                section_facturation['answers']['answer'][
                                                    'value'] if 'answers' in section_facturation and 'answer' in \
                                                                section_facturation[
                                                                    'answers'] and 'value' in \
                                                                section_facturation['answers'][
                                                                    'answer'] else None

                                    """( 1.9) Localisation et période """
                                    section_loc_periode = [sec for sec in section if sec['@id'] == '5']
                                    section_loc_periode = section_loc_periode[0] if len(section_loc_periode) > 0 else None

                                    loc_periode_question = \
                                        section_loc_periode['questions'][
                                            'question'] if section_loc_periode and 'questions' in section_loc_periode and 'question' in \
                                                           section_loc_periode['questions'] else None

                                    for one_loc_periode_question in loc_periode_question:
                                        id = one_loc_periode_question['@id']

                                        # commune
                                        if id == '12':
                                            commune = \
                                            one_loc_periode_question['answers']['answer'][
                                                'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                            one_loc_periode_question[
                                                                'answers'] and 'value' in \
                                                            one_loc_periode_question['answers'][
                                                                'answer'] else None

                                        # service_a_appliquer
                                        elif id == '93':
                                            service_a_appliquer = \
                                                one_loc_periode_question['answers']['answer'][
                                                    'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                                one_loc_periode_question[
                                                                    'answers'] and 'value' in \
                                                                one_loc_periode_question['answers'][
                                                                    'answer'] else None

                                        # coordonnee_x
                                        elif id == '94':
                                            coordonnee_x = \
                                                one_loc_periode_question['answers']['answer'][
                                                    'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                                one_loc_periode_question[
                                                                    'answers'] and 'value' in \
                                                                one_loc_periode_question['answers'][
                                                                    'answer'] else None

                                        # coordonnee_y
                                        elif id == '95':
                                            coordonnee_y = \
                                                one_loc_periode_question['answers']['answer'][
                                                    'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                                one_loc_periode_question[
                                                                    'answers'] and 'value' in \
                                                                one_loc_periode_question['answers'][
                                                                    'answer'] else None


                                        # cadastre
                                        elif id == '96':
                                            cadastre = \
                                                one_loc_periode_question['answers']['answer'][
                                                    'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                                one_loc_periode_question[
                                                                    'answers'] and 'value' in \
                                                                one_loc_periode_question['answers'][
                                                                    'answer'] else None

                                        # num_bien_fonds
                                        elif id == '97':
                                            num_bien_fonds = \
                                                one_loc_periode_question['answers']['answer'][
                                                    'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                                one_loc_periode_question[
                                                                    'answers'] and 'value' in \
                                                                one_loc_periode_question['answers'][
                                                                    'answer'] else None


                                        # lieu_dit
                                        elif id == '99':
                                            lieu_dit = \
                                                one_loc_periode_question['answers']['answer'][
                                                    'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                                one_loc_periode_question[
                                                                    'answers'] and 'value' in \
                                                                one_loc_periode_question['answers'][
                                                                    'answer'] else None

                                        # geometry_collection
                                        elif id == '213':
                                            geometry_collection = \
                                                one_loc_periode_question['answers']['answer'][
                                                    'value'] if 'answers' in one_loc_periode_question and 'answer' in \
                                                                one_loc_periode_question[
                                                                    'answers'] and 'value' in \
                                                                one_loc_periode_question['answers'][
                                                                    'answer'] else None


                            # Evenement model
                            evenement_model = models.Evenement(
                                id_entite=cls.settings['id_entite_xml_import'],
                                id_responsable=cls.settings['id_responsable_xml_import'],
                                type=int(cls.settings['fouille_evenement_id']),
                                libelle=cause_fouille,
                                date_debut=datetime.datetime.strptime(date_debut,cls.settings['xml_date_template']),
                                heure_debut=heure_debut,
                                date_fin=datetime.datetime.strptime(date_fin,cls.settings['xml_date_template']),
                                heure_fin=heure_fin,
                                id_utilisateur_ajout=cls.settings['id_user_ajout_xml_import'],
                                id_utilisateur_modification=cls.settings['id_user_ajout_xml_import'],
                                localisation= commune,
                                numero_dossier = Utils.generate_numero_dossier(cls.request, int(cls.settings['fouille_evenement_id']))
                            )

                            if evenement_model:
                                cls.request.dbsession.add(evenement_model)
                                cls.request.dbsession.flush()
                                max_event_id = evenement_model.id

                                # Fouille model
                                fouille_model = models.Fouille(
                                    id_evenement = max_event_id,
                                    nom_maitre_ouvrage = nom_maitre_ouvrage_entreprise,
                                    rue_maitre_ouvrage = rue_maitre_ouvrage_entreprise,
                                    localite_maitre_ouvrage=localite_maitre_ouvrage_entreprise,
                                    telephone_maitre_ouvrage=telephone_maitre_ouvrage_entreprise,
                                    fax_maitre_ouvrage=fax_maitre_ouvrage_entreprise,
                                    courriel_maitre_ouvrage=courriel_maitre_ouvrage_entreprise,
                                    nom_direction_locale=nom_maitre_ouvrage_dir_loc,
                                    prenom_direction_locale=prenom_maitre_ouvrage_dir_loc,
                                    mobile_direction_locale=mobile_maitre_ouvrage_dir_loc,
                                    telephone_direction_locale=telephone_maitre_ouvrage_dir_loc,
                                    fax_direction_locale=fax_maitre_ouvrage_dir_loc,
                                    courriel_direction_locale=courriel_maitre_ouvrage_dir_loc,
                                    nom_entrepreneur=nom_entrepreneur_entreprise,
                                    rue_entrepreneur=rue_entrepreneur_entreprise,
                                    localite_entrepreneur=npa_localite_entrepreneur_entreprise,
                                    telephone_entrepreneur=telephone_entrepreneur_entreprise,
                                    fax_entrepreneur=fax_entrepreneur_entreprise,
                                    courriel_entrepreneur=courriel_entrepreneur_entreprise,
                                    nom_responsable_travaux=nom_entrepreneur_responsable_travaux,
                                    prenom_responsable_travaux=prenom_entrepreneur_responsable_travaux,
                                    mobile_responsable_travaux=mobile_entrepreneur_responsable_travaux,
                                    telephone_responsable_travaux=telephone_entrepreneur_responsable_travaux,
                                    fax_responsable_travaux=fax_entrepreneur_responsable_travaux,
                                    courriel_responsable_travaux=courriel_entrepreneur_responsable_travaux
                                    #facturation = Column(Numeric)
                                    #date_debut_valide =
                                    #date_fin_valide =
                                    #date_maj_valide =
                                    #numero_facture =
                                    #date_facture =
                                    #reserve_eventuelle =
                                )

                                cls.request.dbsession.add(fouille_model)

                                # Evenement point model
                                """
                                geometry = json.loads(
                                    '{"type":"Point","coordinates":[' + coordonnee_x + ',' + coordonnee_y + ']}')
                                evenement_point_model = models.EvenementPoint(
                                    id_evenement=max_event_id,
                                )
                                evenement_point_model.set_json_geometry(str(geometry), cls.settings['srid'])
                                cls.request.dbsession.add(evenement_point_model)

                                # Evenement polygon model
                                if geometry_collection is not None:
                                    evenement_polygon_model = models.EvenementPolygone(
                                        id_evenement=max_event_id
                                    )
                                    evenement_polygon_model.set_geometry_collection(str(geometry_collection),
                                                                                    cls.settings['srid'])
                                    cls.request.dbsession.add(evenement_polygon_model)
                                """

                                Utils.add_ev_geometries(cls.request, geometry_collection, max_event_id)

                        """------------- (2) Form perturbation ---------------"""
                        perturbations_form = [f for f in form if f['@id'] == '41']
                        perturbations_form = perturbations_form[0] if len(perturbations_form) > 0 else None

                        if perturbations_form:

                            # Type perturbation
                            type_pertubation = None

                            # Heure_fin
                            heure_fin = None

                            # Periode occupation
                            periode_occupation = None

                            # Type occupation
                            type_occupation = None

                            # Occupation durant le week-end
                            occupation_weekend = False

                            # Occupation durant les heures de pointe
                            occupation_heures_pointes = False

                            # Remarque
                            remarque = None

                            # Voie(s) condamnée(s)
                            voies_condamnees = None

                            # Type de régulation
                            type_regulation = None

                            # Nom
                            nom = None

                            # Prénom
                            prenom = None

                            # Mobile
                            mobile = None

                            # Telephone
                            telephone = None

                            # Courriel
                            courriel = None

                            # Date debut
                            date_debut = None

                            # Heure debut
                            heure_debut = None

                            # Date fin
                            date_fin = None

                            # Hauteur gabarit
                            hauteur_gabarit = None

                            # Largeur gabarit
                            largeur_gabarit = None

                            # Type fermeture
                            type_fermeture = None

                            # Deviation
                            deviation = None

                            section = perturbations_form['sections'][
                                'section'] if perturbations_form and 'sections' in perturbations_form and 'section' in \
                                              perturbations_form['sections'] else None

                            if section and len(section) > 0:

                                """( 2.1) Type perturbation """
                                section_type_perturbation = [sec for sec in section if
                                                             sec['@id'] == '42']
                                section_type_perturbation = section_type_perturbation[0] if len(
                                    section_type_perturbation) > 0 else None
                                type_perturbation_question = \
                                    section_type_perturbation['questions'][
                                        'question'] if section_type_perturbation and 'questions' in section_type_perturbation and 'question' in \
                                                       section_type_perturbation['questions'] else None

                                if section_type_perturbation:
                                    id = section_type_perturbation['@id']


                                    # type_pertubation
                                    if id == '42':
                                        type_pertubation = \
                                            type_perturbation_question['answers']['answer'][
                                                'value'] if 'answers' in type_perturbation_question and 'answer' in \
                                                            type_perturbation_question[
                                                                'answers'] and 'value' in \
                                                            type_perturbation_question['answers'][
                                                                'answer'] else None
                                        if type_pertubation == "Occupation":
                                            type_pertubation = int(cls.settings['occupation_perturbation_id'])
                                        elif type_pertubation == "Fermeture":
                                            type_pertubation = int(cls.settings['fermeture_perturbation_id'])
                                        else:
                                            type_pertubation = None

                                """(2.2) Occupation"""
                                section_occupation = [sec for sec in section if
                                                      sec['@id'] == '41']
                                section_occupation = section_occupation[0] if len(
                                    section_occupation) > 0 else None

                                if type_pertubation == int(
                                        cls.settings['occupation_perturbation_id']) and section_occupation:
                                    occupation_question = \
                                        section_occupation['questions'][
                                            'question'] if section_occupation and 'questions' in section_occupation and 'question' in \
                                                           section_occupation['questions'] else None

                                    for one_occupation_question in occupation_question:
                                        id = one_occupation_question['@id']


                                        # occupation_heures_pointes
                                        if id == '20':
                                            occupation_heures_pointes = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                            occupation_heures_pointes = True if occupation_heures_pointes is not None and occupation_heures_pointes.upper() == "OUI" else occupation_heures_pointes
                                            occupation_heures_pointes = False if occupation_heures_pointes is not None and occupation_heures_pointes != True and occupation_heures_pointes.upper() == "NON" else None

                                        # occupation_weekend
                                        elif id == '21':
                                            occupation_weekend = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                            occupation_weekend = True if occupation_weekend is not None and occupation_weekend.upper() == "OUI" else occupation_weekend
                                            occupation_weekend = False if occupation_weekend is not None and occupation_weekend != True and occupation_weekend.upper() == "NON" else None

                                        # remarque
                                        elif id == '24':
                                            remarque = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # nom
                                        elif id == '100':
                                            nom = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                        # prenom
                                        elif id == '101':
                                            prenom = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # mobile
                                        elif id == '102':
                                            mobile = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # telephone
                                        elif id == '103':
                                            telephone = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # courriel
                                        elif id == '105':
                                            courriel = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # date_debut
                                        elif id == '121':
                                            date_debut = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                            date_debut = date_debut.replace(".", "-") if date_debut else None


                                        # heure_debut
                                        elif id == '122':
                                            heure_debut = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                            heure_debut = heure_debut.replace(".", ":").replace("h",
                                                                                                ":") if heure_debut else None
                                            heure_debut = heure_debut + ":00" if heure_debut and len(
                                                heure_debut) <= 2 else heure_debut
                                            heure_debut = "0" + heure_debut if heure_debut and len(
                                                heure_debut) == 3 else heure_debut


                                        # date_fin
                                        elif id == '123':
                                            date_fin = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                            date_fin = date_fin.replace(".", "-") if date_fin else None

                                        # heure_fin
                                        elif id == '124':
                                            heure_fin = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                            heure_fin = heure_fin.replace(".", ":").replace("h",
                                                                                            ":") if heure_fin else None
                                            heure_fin = heure_fin + ":00" if heure_fin and len(
                                                heure_fin) <= 2 else heure_fin
                                            heure_fin = "0" + heure_fin if heure_fin and len(
                                                heure_fin) == 3 else heure_fin

                                        # periode_occupation
                                        elif id == '126':
                                            periode_occupation = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # type_occupation
                                        elif id == '127':
                                            type_occupation = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None
                                        # voies_condamnees
                                        elif id == '128':
                                            voies_condamnees = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # type_regulation
                                        elif id == '129':
                                            type_regulation = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None



                                        # hauteur_gabarit
                                        elif id == '130':
                                            hauteur_gabarit = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None

                                        # largeur_gabarit
                                        elif id == '131':
                                            largeur_gabarit = \
                                                one_occupation_question['answers']['answer'][
                                                    'value'] if 'answers' in one_occupation_question and 'answer' in \
                                                                one_occupation_question[
                                                                    'answers'] and 'value' in \
                                                                one_occupation_question['answers'][
                                                                    'answer'] else None


                                """(2.2) Fermeture"""
                                section_fermeture = [sec for sec in section if
                                                     sec['@id'] == '43']
                                section_fermeture = section_fermeture[0] if len(
                                    section_fermeture) > 0 else None

                                if type_pertubation == int(
                                        cls.settings['fermeture_perturbation_id']) and section_fermeture:
                                    fermeture_question = \
                                        section_fermeture['questions'][
                                            'question'] if section_fermeture and 'questions' in section_fermeture and 'question' in \
                                                           section_fermeture['questions'] else None

                                    for one_fermeture_question in fermeture_question:
                                        id = one_fermeture_question['@id']

                                        # remarque
                                        if id == '24':
                                            remarque = \
                                            one_fermeture_question['answers']['answer'][
                                                'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                            one_fermeture_question[
                                                                'answers'] and 'value' in \
                                                            one_fermeture_question['answers'][
                                                                'answer'] else None


                                        # nom
                                        elif id == '100':
                                            nom = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # prenom
                                        elif id == '101':
                                            prenom = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # mobile
                                        elif id == '102':
                                            mobile = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # telephone
                                        elif id == '103':
                                            telephone = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # courriel
                                        elif id == '105':
                                            courriel = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # date_debut
                                        elif id == '121':
                                            date_debut = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None
                                            date_debut = date_debut.replace(".", "-") if date_debut else None


                                        # heure_debut
                                        elif id == '122':
                                            heure_debut = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None
                                            heure_debut = heure_debut.replace(".", ":").replace("h",
                                                                                                ":") if heure_debut else None
                                            heure_debut = heure_debut + ":00" if heure_debut and len(
                                                heure_debut) <= 2 else heure_debut
                                            heure_debut = "0" + heure_debut if heure_debut and len(
                                                heure_debut) == 3 else heure_debut


                                        # date_fin
                                        elif id == '123':
                                            date_fin = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None
                                            date_fin = date_fin.replace(".", "-") if date_fin else None


                                        # heure_fin
                                        elif id == '124':
                                            heure_fin = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None
                                            heure_fin = heure_fin.replace(".", ":").replace("h",
                                                                                            ":") if heure_fin else None
                                            heure_fin = heure_fin + ":00" if heure_fin and len(
                                                heure_fin) <= 2 else heure_fin
                                            heure_fin = "0" + heure_fin if heure_fin and len(
                                                heure_fin) == 3 else heure_fin


                                        # type_fermeture
                                        elif id == '132':
                                            type_fermeture = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None

                                        # deviation
                                        elif id == '133':
                                            deviation = \
                                                one_fermeture_question['answers']['answer'][
                                                    'value'] if 'answers' in one_fermeture_question and 'answer' in \
                                                                one_fermeture_question[
                                                                    'answers'] and 'value' in \
                                                                one_fermeture_question['answers'][
                                                                    'answer'] else None


                                # Check date_debut, if less than 24h, urgence=true
                                urgence = False
                                if date_debut != None and heure_debut != None:
                                    date_time_str = str(date_debut) + ' ' + str(heure_debut)
                                    date_time_obj = datetime.datetime.strptime(date_time_str,
                                                                               cls.settings['xml_date_template'] + ' ' + cls.settings['xml_heure_template'])
                                    now = datetime.datetime.now()

                                    if date_time_obj >= now and date_time_obj <= now + datetime.timedelta(days=1):
                                        urgence = True

                                perturbation_model = models.Perturbation(
                                    id_evenement=max_event_id,
                                    type=type_pertubation,
                                    # description=description,
                                    date_debut=datetime.datetime.strptime(date_debut,cls.settings['xml_date_template']),
                                    heure_debut=heure_debut,
                                    date_fin=datetime.datetime.strptime(date_fin,cls.settings['xml_date_template']),
                                    heure_fin=heure_fin,
                                    nom_responsable_trafic=nom,
                                    prenom_responsable_trafic=prenom,
                                    mobile_responsable_trafic=mobile,
                                    telephone_responsable_trafic=telephone,
                                    # fax_responsable_trafic=fax,
                                    courriel_responsable_trafic=courriel,
                                    remarque=remarque,
                                    id_utilisateur_ajout=cls.settings['id_user_ajout_xml_import'],
                                    id_utilisateur_modification=cls.settings['id_user_ajout_xml_import'],
                                    urgence=urgence
                                )

                                if perturbation_model:
                                    cls.request.dbsession.add(perturbation_model)
                                    cls.request.dbsession.flush()
                                    max_perturbation_id = perturbation_model.id

                                    # Occupation
                                    if type_pertubation == int(
                                            cls.settings['occupation_perturbation_id']) and section_fermeture:
                                        occupation_model = models.Occupation(
                                            id_perturbation=max_perturbation_id,
                                            id_responsable_regulation=cls.settings['id_responsable_xml_import'],
                                            type_occupation=type_occupation,
                                            type_regulation=type_regulation,
                                            voies_condamnees=voies_condamnees,
                                            largeur_gabarit=largeur_gabarit,
                                            hauteur_gabarit=hauteur_gabarit,
                                            heure_pointe=occupation_heures_pointes,
                                            week_end=occupation_weekend)
                                        cls.request.dbsession.add(occupation_model)

                                    # Fermeture
                                    elif type_pertubation == int(
                                            cls.settings['fermeture_perturbation_id']) and section_fermeture:
                                        fermeture_model = models.Fermeture(
                                            id_perturbation=max_perturbation_id,
                                            deviation=deviation,
                                            id_responsable=cls.settings['id_responsable_xml_import'])
                                        cls.request.dbsession.add(fermeture_model)


                                    #Geometries
                                    Utils.add_perturb_geometries(cls.request, geometry_collection, max_perturbation_id)

                # Commit transaction
                transaction.commit()


        except Exception as e:
            # transaction.abort()
            cls.request.dbsession.rollback()
            raise e
            return False

        return True


