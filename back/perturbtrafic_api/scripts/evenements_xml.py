

import xmltodict
import os
from sqlalchemy import exc
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
    def move_file_to_success_folder(cls, request, file_name):
        try:
            os.rename(request.registry.settings['evenements_xml_files_folder'] + '/' + file_name,
            request.registry.settings['evenements_xml_files_success_folder'] + '/' + file_name)

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



        except exc.ResourceClosedError as e:
            log.error(str(e), exc_info=True)
            return False

        return True

    @classmethod
    def add_file_data_autre_entrave(cls, dossier):

		sp = cls.request.dbsession.savepoint()

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

					# Reférence CAMAC
					ref_camac = dossier['instance_id'] if 'instance_id' in dossier else None

					# Section_evenement entrave : id 51

					# Date debut : id 121
					date_debut = None

					# Heure debut : id 122
					heure_debut = None

					# Date fin : id 123
					date_fin = None

					# Heure fin : id 124
					heure_fin = None

					# Surface : id 15
					surface = None

					# Longueur_etape : id 16
					longueur_etape = None

					# Cause_entrave  : id 134
					cause_entrave = None

					# Description_entrave : id 135
					description_entrave = None

					# Adresse de la fouille  : id 201
					adresse_fouille = None

					# Section_requerant_entreprise entrave : id 1

					# Rue requerant entreprise : id 2
					rue_requerant_entreprise = None

					# Localite requerant entreprise : id 3
					localite_requerant_entreprise = None

					# Telephone requerant entreprise : id 4
					telephone_requerant_entreprise = None

					# Fax requerant entreprise : id 5
					fax_requerant_entreprise = None

					# Courriel requerant entreprise : id 6
					courriel_requerant_entreprise = None

					# Nom requerant entreprise : id 1
					nom_requerant_entreprise = None

					# Section_requerant_personne entrave : id 32
                
					# Nom requerant personne : id 100
					nom_requerant_personne = None

					# Prenom requerant personne : id 101
					prenom_requerant_personne = None

					# Mobile requerant personne : id 102
					mobile_requerant_personne = None

					# Telephone requerant personne : id 103
					telephone_requerant_personne = None

					# Fax requerant personne : id 104
					fax_requerant_personne = None

					# Courriel requerant personne : id 105
					courriel_requerant_personne = None

					# Section_maitre_ouvrage_dir_loc entrave : id 33

					# Nom maitre ouvrage direction locale : id 106
					nom_maitre_ouvrage_dir_loc = None

					# Prenom maitre ouvrage direction locale : id 107
					prenom_maitre_ouvrage_dir_loc = None

					# Mobile maitre ouvrage direction locale : id 108
					mobile_maitre_ouvrage_dir_loc = None

					# Telephone maitre ouvrage direction locale : id 109
					telephone_maitre_ouvrage_dir_loc = None

					# Fax maitre ouvrage direction locale : id 110
					fax_maitre_ouvrage_dir_loc = None

					# Courriel maitre ouvrage direction locale : id 111
					courriel_maitre_ouvrage_dir_loc = None

					# section_maitre_ouvrage_entreprise entrave : id 2

					# Rue maitre ouvrage entreprise : id 2
					rue_maitre_ouvrage_entreprise = None

					# Localite maitre ouvrage entreprise : id 3
					localite_maitre_ouvrage_entreprise = None

					# Telephone maitre ouvrage entreprise : id 4
					telephone_maitre_ouvrage_entreprise = None

					# Fax maitre ouvrage entreprise : id 5
					fax_maitre_ouvrage_entreprise = None

					# Courriel maitre ouvrage entreprise : id 6
					courriel_maitre_ouvrage_entreprise = None

					# Nom maitre ouvrage entreprise : id 1
					nom_maitre_ouvrage_entreprise = None

					# section_facturation entrave : id 4
            
					# Adresse facturation : id 10
					adresse_facturation = None

					# section_loc_periode entrave : id 52

					# Num bien-fonds : id 97
					num_bien_fonds = None

					# Commune : id 12
					commune = None

					# Coordonnee X : id 94
					coordonnee_x = None

					# Coordonnee Y : id 95
					coordonnee_y = None

					# Geometry collection : id 213 & 222
					geometry_collection = None

					# Cadastre : id 96
					cadastre = None

					# Lieu dit : id 99
					lieu_dit = None

					# Service à appliquer : id 242
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

								if not evenement_question:
									return False

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

										if date_debut == None:
											log.error('date_debut is null', exc_info=True)
											return False

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

										if heure_debut == None:
											log.error('heure_debut is null', exc_info=True)
											return False


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

									# cause_entrave
									elif id == '134':
										cause_entrave = one_evenement_question['answers']['answer'][
											'value'] if 'answers' in one_evenement_question and 'answer' in \
														one_evenement_question['answers'] and 'value' in \
														one_evenement_question['answers']['answer'] else None

									# description_entrave
									elif id == '135':
										description_entrave = one_evenement_question['answers']['answer'][
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

									# telephone_requerant_personne
									elif id == '103':
										telephone_requerant_personne = \
										one_requerant_personne_question['answers']['answer'][
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

									# geometry_collection 213
									elif id == '213':
										geometry_collection = \
											one_loc_periode_question['answers']['answer'][
												'value'] if 'answers' in one_loc_periode_question and 'answer' in \
															one_loc_periode_question[
																'answers'] and 'value' in \
															one_loc_periode_question['answers'][
																'answer'] else None

									# geometry_collection 222
									elif id == '222':
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
								libelle=title,
								description=description,
								ref_camac=ref_camac,
								date_debut=datetime.datetime.strptime(date_debut,cls.settings['xml_date_template']) if date_debut else None,
								heure_debut=heure_debut,
								date_fin=datetime.datetime.strptime(date_fin,cls.settings['xml_date_template']) if date_fin else None,
								heure_fin=heure_fin,
								nom_requerant=nom_requerant_entreprise,
								rue_requerant=rue_requerant_entreprise,
								localite_requerant=localite_requerant_entreprise,
								telephone_requerant=telephone_requerant_entreprise,
								fax_requerant=fax_requerant_entreprise,
								courriel_requerant=courriel_requerant_entreprise,
								nom_contact=nom_requerant_personne,
								prenom_contact=prenom_requerant_personne,
								mobile_contact=mobile_requerant_personne,
								telephone_contact=telephone_requerant_personne,
								fax_contact=fax_requerant_personne,
								courriel_contact=courriel_requerant_personne,
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
									cause = cause_entrave,
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
									#nom_entrepreneur=nom_requerant_entreprise,
									#rue_entrepreneur=rue_requerant_entreprise,
									#localite_entrepreneur=localite_requerant_entreprise,
									#telephone_entrepreneur=telephone_requerant_entreprise,
									#fax_entrepreneur=fax_requerant_entreprise,
									#courriel_entrepreneur=courriel_requerant_entreprise,
									#nom_responsable_travaux=nom_requerant_personne,
									#prenom_responsable_travaux=prenom_requerant_personne,
									#mobile_responsable_travaux=mobile_requerant_personne,
									#telephone_responsable_travaux=telephone_requerant_personne,
									#fax_responsable_travaux=fax_requerant_personne,
									#courriel_responsable_travaux=courriel_requerant_personne
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

							# Occupations perturbations
							perturbations_values = {}

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
										item_id = type_perturbation_question['answers']['answer']['@item']
										perturbations_values[item_id] = {}

										type_pertubation = \
											type_perturbation_question['answers']['answer'][
												'value'] if 'answers' in type_perturbation_question and 'answer' in \
															type_perturbation_question[
																'answers'] and 'value' in \
															type_perturbation_question['answers'][
																'answer'] else None

										if type_pertubation == "Occupation":
											type_pertubation = int(
												cls.settings['occupation_perturbation_id'])
										elif type_pertubation == "Fermeture":
											type_pertubation = int(
												cls.settings['fermeture_perturbation_id'])

										perturbations_values[item_id]['type_pertubation'] = type_pertubation

									# Other perturbations types
									section_type_other_perturbation = [sec for sec in section if
																	   sec['@id'] == '45']
									section_type_other_perturbation = section_type_other_perturbation[
										0] if section_type_other_perturbation and len(
										section_type_other_perturbation) > 0 else section_type_other_perturbation

									if section_type_other_perturbation:

										type_other_perturbation_question = \
											section_type_other_perturbation['questions'][
												'question'] if section_type_other_perturbation and 'questions' in section_type_other_perturbation and 'question' in \
															   section_type_other_perturbation['questions'] else None

										other_perturb_types_answers = cls.get_answers(type_other_perturbation_question)
										for one_item_id in other_perturb_types_answers:
											one_type_pertubation = other_perturb_types_answers[one_item_id]

											if one_item_id and one_type_pertubation:
												one_item_id = int(one_item_id)
												perturbations_values[str(one_item_id + 1)] = {}

												if one_type_pertubation == "Occupation":
													perturbations_values[str(one_item_id + 1)]['type_pertubation'] = int(
														cls.settings['occupation_perturbation_id'])
												elif one_type_pertubation == "Fermeture":
													perturbations_values[str(one_item_id + 1)]['type_pertubation'] = int(
														cls.settings['fermeture_perturbation_id'])

								"""(2.2) Occupation"""

								section_occupation = [sec for sec in section if
													  sec['@id'] == '41']
								section_occupation = section_occupation[0] if len(
									section_occupation) > 0 else None

								# Set occupation values
								if section_occupation:
									cls.set_ocuppations_values(section_occupation, perturbations_values)


								"""(2.2) Fermeture"""
								section_fermeture = [sec for sec in section if
													 sec['@id'] == '43']
								section_fermeture = section_fermeture[0] if len(
									section_fermeture) > 0 else None

								# Set fermetures values
								if section_fermeture:
									cls.set_fermetures_values(section_fermeture, perturbations_values)

								for one_perturb_item_id in perturbations_values:
									one_perturb_item = perturbations_values[one_perturb_item_id]

									if 'type_pertubation' in one_perturb_item:
										type_pertubation = one_perturb_item['type_pertubation']

										# Check date_debut, if less than 24h, urgence=true
										urgence = False
										date_debut = one_perturb_item['date_debut'] if 'date_debut' in one_perturb_item else None
										heure_debut = one_perturb_item['heure_debut'] if 'heure_debut' in one_perturb_item else None
										date_fin = one_perturb_item['date_fin'] if 'date_fin' in one_perturb_item else None
										heure_fin = one_perturb_item['heure_fin'] if 'heure_fin' in one_perturb_item else None

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
											description=description_entrave,
											date_debut=datetime.datetime.strptime(date_debut,cls.settings['xml_date_template']) if date_debut else None,
											heure_debut=heure_debut,
											date_fin=datetime.datetime.strptime(date_fin,cls.settings['xml_date_template']) if date_fin else None,
											heure_fin=heure_fin,
											nom_responsable_trafic=one_perturb_item['nom'] if 'nom' in one_perturb_item else None,
											prenom_responsable_trafic=one_perturb_item['prenom'] if 'prenom' in one_perturb_item else None,
											mobile_responsable_trafic=one_perturb_item['mobile'] if 'mobile' in one_perturb_item else None,
											telephone_responsable_trafic=one_perturb_item['telephone'] if 'telephone' in one_perturb_item else None,
											# fax_responsable_trafic=fax,
											courriel_responsable_trafic=one_perturb_item['courriel'] if 'courriel' in one_perturb_item else None,
											remarque=one_perturb_item['remarque'] if 'remarque' in one_perturb_item else None,
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
													type_occupation=one_perturb_item['type_occupation'] if 'type_occupation' in one_perturb_item else None,
													type_regulation=one_perturb_item['type_regulation'] if 'type_regulation' in one_perturb_item else None,
													voies_condamnees=one_perturb_item['voies_condamnees'] if 'voies_condamnees' in one_perturb_item else None,
													largeur_gabarit=one_perturb_item['largeur_gabarit'] if 'largeur_gabarit' in one_perturb_item else None,
													hauteur_gabarit=one_perturb_item['hauteur_gabarit'] if 'hauteur_gabarit' in one_perturb_item else None,
													heure_pointe=one_perturb_item['occupation_heures_pointes'] if 'occupation_heures_pointes' in one_perturb_item else None,
													week_end=one_perturb_item['occupation_weekend'] if '' in one_perturb_item else None)
												cls.request.dbsession.add(occupation_model)

											#Fermeture
											elif type_pertubation == int(
													cls.settings['fermeture_perturbation_id']) and section_fermeture:
												fermeture_model = models.Fermeture(
													id_perturbation=max_perturbation_id,
													deviation=one_perturb_item['deviation'] if 'deviation' in one_perturb_item else None,
													id_responsable=cls.settings['id_responsable_xml_import'])
												cls.request.dbsession.add(fermeture_model)

											# Geometries
											Utils.add_perturb_geometries(cls.request, geometry_collection,
																		 max_perturbation_id)

				# Commit transaction
				transaction.commit()

        except Exception as e:
            # transaction.abort()
            sp.rollback()
			log.error(str(e), exc_info=True)
            # raise e
            return False

		cls.request.dbsession.commit()

        return True

    @classmethod
    def add_file_data_fouille(cls, dossier):

		sp = cls.request.dbsession.savepoint()

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

					# Reférence CAMAC
					ref_camac = dossier['instance_id'] if 'instance_id' in dossier else None

					# Section_evenement fouille : id 44

					# Date debut : id 121
					date_debut = None

					# Heure debut : id 122
					heure_debut = None

					# Date fin : id 123
					date_fin = None

					# Heure fin : id 124
					heure_fin = None

					# Cause_fouille  : id 134
					cause_entrave = None

					# Description_fouille : id 135
					description_entrave = None

					# Adresse de la fouille  : id 201
					adresse_fouille = None

					# Section_requerant_entreprise fouille : id 1

					# Rue requerant entreprise : id 2
					rue_requerant_entreprise = None

					# Localite requerant entreprise : id 3
					localite_requerant_entreprise = None

					# Telephone requerant entreprise : id 4
					telephone_requerant_entreprise = None

					# Fax requerant entreprise : id 5
					fax_requerant_entreprise = None

					# Courriel requerant entreprise : id 6
					courriel_requerant_entreprise = None

					# Nom requerant entreprise : id 1
					nom_requerant_entreprise = None

					# Section_requerant_personne fouille : id 32
                
					# Nom requerant personne : id 100
					nom_requerant_personne = None

					# Prenom requerant personne : id 101
					prenom_requerant_personne = None

					# Mobile requerant personne : id 102
					mobile_requerant_personne = None

					# Telephone requerant personne : id 103
					telephone_requerant_personne = None

					# Fax requerant personne : id 104
					fax_requerant_personne = None

					# Courriel requerant personne : id 105
					courriel_requerant_personne = None

					# section_maitre_ouvrage_entreprise fouille : id 2

					# Rue maitre ouvrage entreprise : id 2
					rue_maitre_ouvrage_entreprise = None

					# Localite maitre ouvrage entreprise : id 3
					localite_maitre_ouvrage_entreprise = None

					# Telephone maitre ouvrage entreprise : id 4
					telephone_maitre_ouvrage_entreprise = None

					# Fax maitre ouvrage entreprise : id 5
					fax_maitre_ouvrage_entreprise = None

					# Courriel maitre ouvrage entreprise : id 6
					courriel_maitre_ouvrage_entreprise = None

					# Nom maitre ouvrage entreprise : id 1
					nom_maitre_ouvrage_entreprise = None

					# Section_maitre_ouvrage_dir_loc fouille : id 33

					# Nom maitre ouvrage direction locale : id 106
					nom_maitre_ouvrage_dir_loc = None

					# Prenom maitre ouvrage direction locale : id 107
					prenom_maitre_ouvrage_dir_loc = None

					# Mobile maitre ouvrage direction locale : id 108
					mobile_maitre_ouvrage_dir_loc = None

					# Telephone maitre ouvrage direction locale : id 109
					telephone_maitre_ouvrage_dir_loc = None

					# Fax maitre ouvrage direction locale : id 110
					fax_maitre_ouvrage_dir_loc = None

					# Courriel maitre ouvrage direction locale : id 111
					courriel_maitre_ouvrage_dir_loc = None

					# Section_entrepreneur_entreprise fouille : id 3

					# Nom / Raison sociale entrepreneur entreprise : id 1
					nom_entrepreneur_entreprise = None

					# Rue et numéro sociale entrepreneur entreprise : id 2
					rue_entrepreneur_entreprise = None

					# NPA et localité entrepreneur entreprise : id 3
					npa_localite_entrepreneur_entreprise = None

					# N° de téléphonee entrepreneur entreprise : id 4
					telephone_entrepreneur_entreprise = None

					# N° de fax entrepreneur entreprise : id 5
					fax_entrepreneur_entreprise = None

					# Courriel entrepreneur entreprise : id 6
					courriel_entrepreneur_entreprise = None

					# Section_entrepreneur_resp_travaux fouille : id 34

					# Nom entrepreneur responsable travaux : id 112
					nom_entrepreneur_responsable_travaux = None

					# Prenom entrepreneur responsable travaux : id 113
					prenom_entrepreneur_responsable_travaux = None

					# Mobile entrepreneur responsable travaux : id 114
					mobile_entrepreneur_responsable_travaux = None

					# Telephone entrepreneur responsable travaux : id 115
					telephone_entrepreneur_responsable_travaux = None

					# Fax entrepreneur responsable travaux : id 116
					fax_entrepreneur_responsable_travaux = None

					# Courriel entrepreneur responsable travaux : id 117
					courriel_entrepreneur_responsable_travaux = None

					# section_facturation fouille : id 4
            
					# Adresse facturation : id 10
					adresse_facturation = None

					# section_loc_periode fouille : id 5

					# Num bien-fonds : id 97
					num_bien_fonds = None

					# Commune : id 12
					commune = None

					# Coordonnee X : id 94
					coordonnee_x = None

					# Coordonnee Y : id 95
					coordonnee_y = None

					# Geometry collection : id 223
					geometry_collection = None

					# Cadastre : id 96
					cadastre = None

					# Lieu dit : id 99
					lieu_dit = None

					# Service à appliquer : id 93
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

								if not evenement_question:
									return False

								for one_evenement_question in evenement_question:
									id = one_evenement_question['@id']


									# date_debut
									if id == '121':
										date_debut = one_evenement_question['answers']['answer'][
											'value'] if 'answers' in one_evenement_question and 'answer' in \
														one_evenement_question['answers'] and 'value' in \
														one_evenement_question['answers']['answer'] else None
										date_debut = date_debut.replace(".", "-") if date_debut else None

										if date_debut == None:
											log.error('date_debut is null', exc_info=True)
											return False


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

										if heure_debut == None:
											log.error('heure_debut is null', exc_info=True)
											return False


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

									# telephone_requerant_personne
									elif id == '103':
										telephone_requerant_personne = \
											one_requerant_personne_question['answers']['answer'][
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

										# geometry_collection 223
										elif id == '223':
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
								libelle=title,
								description=description_fouille,
								ref_camac=ref_camac,
								date_debut=datetime.datetime.strptime(date_debut,cls.settings['xml_date_template']) if date_debut else None,
								heure_debut=heure_debut,
								date_fin=datetime.datetime.strptime(date_fin,cls.settings['xml_date_template']) if date_fin else None,
								heure_fin=heure_fin,
								nom_requerant=nom_requerant_entreprise,
								rue_requerant=rue_requerant_entreprise,
								localite_requerant=localite_requerant_entreprise,
								telephone_requerant=telephone_requerant_entreprise,
								fax_requerant=fax_requerant_entreprise,
								courriel_requerant=courriel_requerant_entreprise,
								nom_contact=nom_requerant_personne,
								prenom_contact=prenom_requerant_personne,
								mobile_contact=mobile_requerant_personne,
								telephone_contact=telephone_requerant_personne,
								fax_contact=fax_requerant_personne,
								courriel_contact=courriel_requerant_personne,
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

							# Perturbations
							perturbations_values = {}

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
										item_id = type_perturbation_question['answers']['answer']['@item']
										perturbations_values[item_id] = {}

										type_pertubation = \
											type_perturbation_question['answers']['answer'][
												'value'] if 'answers' in type_perturbation_question and 'answer' in \
															type_perturbation_question[
																'answers'] and 'value' in \
															type_perturbation_question['answers'][
																'answer'] else None

										if type_pertubation == "Occupation":
											type_pertubation = int(
												cls.settings['occupation_perturbation_id'])
										elif type_pertubation == "Fermeture":
											type_pertubation = int(
												cls.settings['fermeture_perturbation_id'])

										perturbations_values[item_id]['type_pertubation'] = type_pertubation

									# Other perturbations types
									section_type_other_perturbation = [sec for sec in section if
																	   sec['@id'] == '45']
									section_type_other_perturbation = section_type_other_perturbation[
										0] if section_type_other_perturbation and len(
										section_type_other_perturbation) > 0 else section_type_other_perturbation

									if section_type_other_perturbation:

										type_other_perturbation_question = \
											section_type_other_perturbation['questions'][
												'question'] if section_type_other_perturbation and 'questions' in section_type_other_perturbation and 'question' in \
															   section_type_other_perturbation['questions'] else None

										other_perturb_types_answers = cls.get_answers(type_other_perturbation_question)
										for one_item_id in other_perturb_types_answers:
											one_type_pertubation = other_perturb_types_answers[one_item_id]

											if one_item_id and one_type_pertubation:
												one_item_id = int(one_item_id)
												perturbations_values[str(one_item_id + 1)] = {}

												if one_type_pertubation == "Occupation":
													perturbations_values[str(one_item_id + 1)]['type_pertubation'] = int(
														cls.settings['occupation_perturbation_id'])
												elif one_type_pertubation == "Fermeture":
													perturbations_values[str(one_item_id + 1)]['type_pertubation'] = int(
														cls.settings['fermeture_perturbation_id'])

								"""(2.2) Occupation"""

								section_occupation = [sec for sec in section if
													  sec['@id'] == '41']
								section_occupation = section_occupation[0] if len(
									section_occupation) > 0 else None

								# Set occupation values
								if section_occupation:
									cls.set_ocuppations_values(section_occupation, perturbations_values)


								"""(2.2) Fermeture"""
								section_fermeture = [sec for sec in section if
													 sec['@id'] == '43']
								section_fermeture = section_fermeture[0] if len(
									section_fermeture) > 0 else None

								# Set fermetures values
								if section_fermeture:
									cls.set_fermetures_values(section_fermeture, perturbations_values)

								for one_perturb_item_id in perturbations_values:
									one_perturb_item = perturbations_values[one_perturb_item_id]

									if 'type_pertubation' in one_perturb_item:
										type_pertubation = one_perturb_item['type_pertubation']

										# Check date_debut, if less than 24h, urgence=true
										urgence = False
										date_debut = one_perturb_item['date_debut'] if 'date_debut' in one_perturb_item else None
										heure_debut = one_perturb_item['heure_debut'] if 'heure_debut' in one_perturb_item else None
										date_fin = one_perturb_item['date_fin'] if 'date_fin' in one_perturb_item else None
										heure_fin = one_perturb_item['heure_fin'] if 'heure_fin' in one_perturb_item else None

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
											date_debut=datetime.datetime.strptime(date_debut,cls.settings['xml_date_template']) if date_debut else None,
											heure_debut=heure_debut,
											date_fin=datetime.datetime.strptime(date_fin,cls.settings['xml_date_template']) if date_fin else None,
											heure_fin=heure_fin,
											nom_responsable_trafic=one_perturb_item['nom'] if 'nom' in one_perturb_item else None,
											prenom_responsable_trafic=one_perturb_item['prenom'] if 'prenom' in one_perturb_item else None,
											mobile_responsable_trafic=one_perturb_item['mobile'] if 'mobile' in one_perturb_item else None,
											telephone_responsable_trafic=one_perturb_item['telephone'] if 'telephone' in one_perturb_item else None,
											# fax_responsable_trafic=fax,
											courriel_responsable_trafic=one_perturb_item['courriel'] if 'courriel' in one_perturb_item else None,
											remarque=one_perturb_item['remarque'] if 'remarque' in one_perturb_item else None,
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
													type_occupation=one_perturb_item['type_occupation'] if 'type_occupation' in one_perturb_item else None,
													type_regulation=one_perturb_item['type_regulation'] if 'type_regulation' in one_perturb_item else None,
													voies_condamnees=one_perturb_item['voies_condamnees'] if 'voies_condamnees' in one_perturb_item else None,
													largeur_gabarit=one_perturb_item['largeur_gabarit'] if 'largeur_gabarit' in one_perturb_item else None,
													hauteur_gabarit=one_perturb_item['hauteur_gabarit'] if 'hauteur_gabarit' in one_perturb_item else None,
													heure_pointe=one_perturb_item['occupation_heures_pointes'] if 'occupation_heures_pointes' in one_perturb_item else None,
													week_end=one_perturb_item['occupation_weekend'] if '' in one_perturb_item else None)
												cls.request.dbsession.add(occupation_model)

											#Fermeture
											elif type_pertubation == int(
													cls.settings['fermeture_perturbation_id']) and section_fermeture:
												fermeture_model = models.Fermeture(
													id_perturbation=max_perturbation_id,
													deviation=one_perturb_item['deviation'] if 'deviation' in one_perturb_item else None,
													id_responsable=cls.settings['id_responsable_xml_import'])
												cls.request.dbsession.add(fermeture_model)

											# Geometries
											Utils.add_perturb_geometries(cls.request, geometry_collection,
																		 max_perturbation_id)

				# Commit transaction
				transaction.commit()

        except Exception as e:
            # transaction.abort()
            sp.rollback()
			log.error(str(e), exc_info=True)
            # raise e
            return False

		cls.request.dbsession.commit()

        return True

    @classmethod
    def get_answers(cls, question):
        items = {}

        answers = question['answers']['answer'] if 'answers' in question and 'answer' in question['answers'] else None

        # Array
        if answers and isinstance(answers, list):
           for answer in answers:
               items[answer['@item']] = answer['value']
        else:
            items[question['answers']['answer'][
                '@item']] = question['answers']['answer'][
                'value']

        return items

    @classmethod
    def set_ocuppations_values(cls, section, perturb_obj):

        question = \
            section['questions'][
                'question'] if section and 'questions' in section and 'question' in \
                               section['questions'] else None

        for one_question in question:
            id = one_question['@id']
            answsers = cls.get_answers(one_question)

            for one_answser in answsers:
                answser_value = answsers[one_answser] if one_answser in answsers and answsers[one_answser] != '' else None

                if answser_value:
                    # occupation_heures_pointes
                    if id == '20':
                        answser_value = True if answser_value is not None and answser_value.upper() == "OUI" else answser_value

                        if answser_value != True and answser_value.upper() != "OUI":
                            answser_value = False if answser_value != True and answser_value.upper() == "NON" else None

                        perturb_obj[one_answser]['occupation_heures_pointes'] = answser_value

                    # occupation_weekend
                    elif id == '21':
                        answser_value = True if answser_value is not None and answser_value.upper() == "OUI" else answser_value

                        if answser_value != True and answser_value.upper() != "OUI":
                            answser_value = False if answser_value != True and answser_value.upper() == "NON" else None

                        perturb_obj[one_answser]['occupation_weekend'] = answser_value

                    # remarque
                    elif id == '24':
                        perturb_obj[one_answser]['remarque'] = answser_value

                    # nom
                    elif id == '100':
                        perturb_obj[one_answser]['nom'] = answser_value

                    # prenom
                    elif id == '101':
                        perturb_obj[one_answser]['prenom'] = answser_value

                    # mobile
                    elif id == '102':
                        perturb_obj[one_answser]['mobile'] = answser_value

                    # telephone
                    elif id == '103':
                        perturb_obj[one_answser]['telephone'] = answser_value

                    # courriel
                    elif id == '105':
                        perturb_obj[one_answser]['courriel'] = answser_value

                    # date_debut
                    elif id == '121':
                        date_debut = answser_value
                        date_debut = date_debut.replace(".", "-") if date_debut else None
                        perturb_obj[one_answser]['date_debut'] = date_debut

                    # heure_debut
                    elif id == '122':
                        heure_debut = answser_value
                        heure_debut = heure_debut.replace(".", ":").replace("h",
                                                                            ":") if heure_debut else None
                        heure_debut = heure_debut + ":00" if heure_debut and len(
                            heure_debut) <= 2 else heure_debut
                        heure_debut = "0" + heure_debut if heure_debut and len(
                            heure_debut) == 3 else heure_debut

                        perturb_obj[one_answser]['heure_debut'] = heure_debut

                    # date_fin
                    elif id == '123':
                        date_fin = answser_value
                        date_fin = date_fin.replace(".", "-") if date_fin else None
                        perturb_obj[one_answser]['date_fin'] = date_fin

                    # heure_fin
                    elif id == '124':
                        heure_fin = answser_value
                        heure_fin = heure_fin.replace(".", ":").replace("h",
                                                                            ":") if heure_fin else None
                        heure_fin = heure_fin + ":00" if heure_fin and len(
                            heure_fin) <= 2 else heure_fin
                        heure_fin = "0" + heure_fin if heure_fin and len(
                            heure_fin) == 3 else heure_fin

                        perturb_obj[one_answser]['heure_fin'] = heure_fin

                    # periode_occupation
                    elif id == '126':
                        perturb_obj[one_answser]['periode_occupation'] = answser_value

                    # type_occupation
                    elif id == '127':
                        perturb_obj[one_answser]['type_occupation'] = answser_value

                    # voies_condamnees
                    elif id == '128':
                        perturb_obj[one_answser]['voies_condamnees'] = answser_value

                    # type_regulation
                    elif id == '129':
                        perturb_obj[one_answser]['type_regulation'] = answser_value

                    # hauteur_gabarit
                    elif id == '130':
                        perturb_obj[one_answser]['hauteur_gabarit'] = answser_value

                    # largeur_gabarit
                    elif id == '131':
                        perturb_obj[one_answser]['largeur_gabarit'] = answser_value

    @classmethod
    def set_fermetures_values(cls, section, perturb_obj):

        question = \
            section['questions'][
                'question'] if section and 'questions' in section and 'question' in \
                               section['questions'] else None

        for one_question in question:
            id = one_question['@id']
            answsers = cls.get_answers(one_question)

            for one_answser in answsers:
                answser_value = answsers[one_answser] if one_answser in answsers and answsers[one_answser] != '' else None

                if answser_value:
                    # remarque
                    if id == '24':
                        perturb_obj[one_answser]['remarque'] = answser_value

                    # nom
                    elif id == '100':
                        perturb_obj[one_answser]['nom'] = answser_value

                    # prenom
                    elif id == '101':
                        perturb_obj[one_answser]['prenom'] = answser_value

                    # mobile
                    elif id == '102':
                        perturb_obj[one_answser]['mobile'] = answser_value

                    # telephone
                    elif id == '103':
                        perturb_obj[one_answser]['telephone'] = answser_value

                    # courriel
                    elif id == '105':
                        perturb_obj[one_answser]['courriel'] = answser_value

                    # date_debut
                    elif id == '121':
                        date_debut = answser_value
                        date_debut = date_debut.replace(".", "-") if date_debut else None
                        perturb_obj[one_answser]['date_debut'] = date_debut

                    # heure_debut
                    elif id == '122':
                        heure_debut = answser_value
                        heure_debut = heure_debut.replace(".", ":").replace("h",
                                                                            ":") if heure_debut else None
                        heure_debut = heure_debut + ":00" if heure_debut and len(
                            heure_debut) <= 2 else heure_debut
                        heure_debut = "0" + heure_debut if heure_debut and len(
                            heure_debut) == 3 else heure_debut

                        perturb_obj[one_answser]['heure_debut'] = heure_debut

                    # date_fin
                    elif id == '123':
                        date_fin = answser_value
                        date_fin = date_fin.replace(".", "-") if date_fin else None
                        perturb_obj[one_answser]['date_fin'] = date_fin

                    # heure_fin
                    elif id == '124':
                        heure_fin = answser_value
                        heure_fin = heure_fin.replace(".", ":").replace("h",
                                                                        ":") if heure_fin else None
                        heure_fin = heure_fin + ":00" if heure_fin and len(
                            heure_fin) <= 2 else heure_fin
                        heure_fin = "0" + heure_fin if heure_fin and len(
                            heure_fin) == 3 else heure_fin

                        perturb_obj[one_answser]['heure_fin'] = heure_fin

                    # type_fermeture
                    elif id == '132':
                        perturb_obj[one_answser]['type_fermeture'] = answser_value

                    # deviation
                    elif id == '133':
                        perturb_obj[one_answser]['deviation'] = answser_value