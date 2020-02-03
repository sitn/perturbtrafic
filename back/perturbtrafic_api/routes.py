def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/perturbtrafic/api')
    config.add_route('home_slash', '/perturbtrafic/api/')
    # Get 'type_evenement' by id
    config.add_route('type_evenement_by_id', '/perturbtrafic/api/types_evenements/{id}')
    # All 'types_evenements' response
    config.add_route('types_evenements', '/perturbtrafic/api/types_evenements')
    config.add_route('types_evenements_slash', '/perturbtrafic/api/types_evenements/')
    # Get 'evenement' by id
    config.add_route('evenement_by_id', '/perturbtrafic/api/evenements/{id}')
    # All 'evenements' response
    config.add_route('evenements', '/perturbtrafic/api/evenements')
    config.add_route('evenements_slash', '/perturbtrafic/api/evenements/')
    # All 'libelles_evenements' response
    config.add_route('libelles_evenements', '/perturbtrafic/api/libelles_evenements')
    config.add_route('libelles_evenements_slash', '/perturbtrafic/api/libelles_evenements/')
    # Get 'evenements_echeance' response
    config.add_route('evenements_echeance', '/perturbtrafic/api/evenements_echeance')
    config.add_route('evenements_echeance_slash', '/perturbtrafic/api/evenements_echeance/')
    # Get 'evenement_impression_by_id'
    config.add_route('evenement_impression_by_id', '/perturbtrafic/api/evenement_impression/{id}')
    # Get 'evenement_perturbations_impression_by_id'
    config.add_route('evenement_perturbations_impression_by_id', '/perturbtrafic/api/evenement_perturbations_impression/{id}')
    # Get 'evenement_edition by id' response
    config.add_route('evenement_edition_by_id', '/perturbtrafic/api/evenement_edition/{id}')
    # 'evenement_edition for add and update
    config.add_route('evenement_edition', '/perturbtrafic/api/evenement_edition')
    config.add_route('evenement_edition_slash', '/perturbtrafic/api/evenement_edition/')
    # Get 'type_perturbation' by id
    config.add_route('types_perturbation_by_id', '/perturbtrafic/api/types_perturbations/{id}')
    # All 'types_perturbations' response
    config.add_route('types_perturbations', '/perturbtrafic/api/types_perturbations')
    config.add_route('types_perturbations_slash', '/perturbtrafic/api/types_perturbations/')
    # Get 'perturbation_edition' by id
    config.add_route('perturbation_edition_by_id', '/perturbtrafic/api/perturbation_edition/{id}')
    # 'perturbation_edition for add and update
    config.add_route('perturbation_edition', '/perturbtrafic/api/perturbation_edition')
    config.add_route('perturbation_edition_slash', '/perturbtrafic/api/perturbation_edition/')
    # Get 'perturbation' by id
    config.add_route('perturbation_by_id', '/perturbtrafic/api/perturbations/{id}')
    # All 'perturbations' response
    config.add_route('perturbations', '/perturbtrafic/api/perturbations')
    config.add_route('perturbations_slash', '/perturbtrafic/api/perturbations/')
    # Get 'etat_perturbation' by id
    config.add_route('etat_perturbation_by_id', '/perturbtrafic/api/etats_perturbations/{id}')
    # All 'perturbations' response
    config.add_route('etats_perturbations', '/perturbtrafic/api/etats_perturbations')
    config.add_route('etats_perturbations_slash', '/perturbtrafic/api/etats_perturbations/')
    # Get 'perturbation_impression_by_id' response
    config.add_route('perturbation_impression_by_id', '/perturbtrafic/api/perturbation_impression/{id}')
    # Get 'destinataire_facturation' by id
    config.add_route('destinataire_facturation_by_id', '/perturbtrafic/api/destinataires_facturation/{id}')
    # Get destinataires facturation
    config.add_route('destinataires_facturation', '/perturbtrafic/api/destinataires_facturation')
    config.add_route('destinataires_facturation_slash', '/perturbtrafic/api/destinataires_facturation/')
    # Get 'categorie_chantier' by id
    config.add_route('categorie_chantier_by_id', '/perturbtrafic/api/categories_chantiers/{id}')
    # All 'perturbations' response
    config.add_route('categories_chantiers', '/perturbtrafic/api/categories_chantiers')
    config.add_route('categories_chantiers_slash', '/perturbtrafic/api/categories_chantiers/')
    # Get 'type_reperage' by id
    config.add_route('type_reperage_by_id', '/perturbtrafic/api/types_reperages/{id}')
    # All 'types_reperages' response
    config.add_route('types_reperages', '/perturbtrafic/api/types_reperages')
    config.add_route('types_reperages_slash', '/perturbtrafic/api/types_reperages/')
    # Get 'contact' by id
    config.add_route('contact_by_id', '/perturbtrafic/api/contacts/{id}')
    # All 'contacts' response
    config.add_route('contacts', '/perturbtrafic/api/contacts')
    config.add_route('contacts_slash', '/perturbtrafic/api/contacts/')
    # All 'contacts' of entite response
    config.add_route('contacts_entite', '/perturbtrafic/api/contacts_entite')
    config.add_route('contacts_entite_slash', '/perturbtrafic/api/contacts_entite/')
    # All 'contacts_having_login' response
    config.add_route('contacts_having_login', '/perturbtrafic/api/contacts_login')
    config.add_route('contacts_having_login_slash', '/perturbtrafic/api/contacts_login/')
    #contact_potentiel_avis_perturbation
    config.add_route('contacts_potentiels_avis_perturbation', '/perturbtrafic/api/contacts_potentiels_avis_perturbation')
    config.add_route('contacts_potentiels_avis_perturbation_slash', '/perturbtrafic/api/contacts_potentiels_avis_perturbation/')
    config.add_route('contacts_potentiels_avis_perturbation_by_id', '/perturbtrafic/api/contacts_potentiels_avis_perturbation/{id}')
    # contact_avis_fermeture_urgence
    config.add_route('contacts_avis_fermeture_urgence','/perturbtrafic/api/contacts_avis_fermeture_urgence')
    config.add_route('contacts_avis_fermeture_urgence_slash','/perturbtrafic/api/contacts_avis_fermeture_urgence/')
    config.add_route('contacts_avis_fermeture_urgence_by_id','/perturbtrafic/api/contacts_avis_fermeture_urgence/{id}')
    # contact_avis_pr_touche
    config.add_route('contact_avis_pr_touche', '/perturbtrafic/api/contact_avis_pr_touche')
    config.add_route('contact_avis_pr_touche_slash', '/perturbtrafic/api/contact_avis_pr_touche/')
    config.add_route('contact_avis_pr_touche_by_id', '/perturbtrafic/api/contact_avis_pr_touche/{id}')
    # Get 'organism' by id
    config.add_route('organisme_by_id', '/perturbtrafic/api/organismes/{id}')
    # Get 'suggestion' by liste name
    config.add_route('suggestion_by_liste_name', '/perturbtrafic/api/suggestion_by_liste_name/{id}')
    # All 'organismes' response
    config.add_route('organismes', '/perturbtrafic/api/organismes')
    config.add_route('organismes_slash', '/perturbtrafic/api/organismes/')
    # All 'plans_types_fouille' response
    config.add_route('plans_types_fouille', '/perturbtrafic/api/plans_types_fouille')
    config.add_route('plans_types_fouille_slash', '/perturbtrafic/api/plans_types_fouille/')
    # All 'axes_routiers' response
    config.add_route('axes_routiers', '/perturbtrafic/api/axes_routiers')
    config.add_route('axes_routiers_slash', '/perturbtrafic/api/axes_routiers/')
    # All 'pr_par_axe_routier' response
    config.add_route('pr_par_axe_routier', '/perturbtrafic/api/pr_par_axe_routier')
    config.add_route('pr_par_axe_routier_slash', '/perturbtrafic/api/pr_par_axe_routier/')
    # All 'localité' response
    config.add_route('localites', '/perturbtrafic/api/localites')
    config.add_route('localites_slash', '/perturbtrafic/api/localites/')
    # All 'cadastre' response
    config.add_route('cadastre', '/perturbtrafic/api/cadastre')
    config.add_route('cadastre_slash', '/perturbtrafic/api/cadastre/')
    # All 'communes' response
    config.add_route('communes', '/perturbtrafic/api/communes')
    config.add_route('communes_slash', '/perturbtrafic/api/communes/')
    # Search 'evenements'
    config.add_route('search_evenements', '/perturbtrafic/api/recherche/evenements')
    config.add_route('search_evenements_slash', '/perturbtrafic/api/recherche/evenements/')
    # Search 'perturbations'
    config.add_route('search_perturbations', '/perturbtrafic/api/recherche/perturbations')
    config.add_route('search_perturbations_slash', '/perturbtrafic/api/recherche/perturbations/')
    # Get 'conflits_perturabations' by id
    config.add_route('conflits_perturabations', '/perturbtrafic/api/conflits_perturbations')
    config.add_route('conflits_perturabations_slash', '/perturbtrafic/api/conflits_perturbations/')
    config.add_route('conflits_perturabations_by_id', '/perturbtrafic/api/conflits_perturbations/{id}')
    config.add_route('conflits_evenement_by_id', '/perturbtrafic/api/conflits_evenement/{id}')
    #Get geometry_reperage
    config.add_route('geometry_reperage', '/perturbtrafic/api/geometry_reperage')
    config.add_route('geometry_reperage_slash', '/perturbtrafic/api/geometry_reperage/')
    #Charger evenements xml
    config.add_route('evenements_xml', '/perturbtrafic/api/evenements_xml')
    config.add_route('evenements_xml_slash', '/perturbtrafic/api/evenements_xml/')
    # Login
    config.add_route('login', '/perturbtrafic/api/login')
    config.add_route('login_slash', '/perturbtrafic/api/login/')
    # Logout
    config.add_route('logout', '/perturbtrafic/api/logout')
    config.add_route('logout_slash', '/perturbtrafic/api/logout/')
    # Logged user
    config.add_route('logged_user', '/perturbtrafic/api/logged_user')
    config.add_route('logged_user_slash', '/perturbtrafic/api/logged_user/')
    # Entités current user
    config.add_route('entites', '/perturbtrafic/api/entites')
    config.add_route('entites_slash', '/perturbtrafic/api/entites/')
    # Localites npa
    config.add_route('localites_npa', '/perturbtrafic/api/localites_npa')
    config.add_route('localites_npa_slash', '/perturbtrafic/api/localites_npa/')
    # Autorisations accordees of current user
    config.add_route('autorisations_accordees', '/perturbtrafic/api/autorisations_accordees')
    config.add_route('autorisations_accordees_slash', '/perturbtrafic/api/autorisations_accordees/')
    # Autorisations recues of current user
    config.add_route('autorisations_recues', '/perturbtrafic/api/autorisations_recues')
    config.add_route('autorisations_recues_slash', '/perturbtrafic/api/autorisations_recues/')
    # Autorisations
    config.add_route('autorisation_by_id', '/perturbtrafic/api/autorisations/{id}')
    config.add_route('autorisations', '/perturbtrafic/api/autorisations')
    config.add_route('autorisations_slash', '/perturbtrafic/api/autorisations/')
    # Autorisations_fonctions
    config.add_route('autorisations_fonctions', '/perturbtrafic/api/autorisations_fonctions')
    config.add_route('autorisations_fonctions_slash', '/perturbtrafic/api/autorisations_fonctions/')
    # LDAP users
    config.add_route('ldap_users', '/perturbtrafic/api/ldap_users')
    config.add_route('ldap_users_slash', '/perturbtrafic/api/ldap_users/')
    # Nouveaux contact AD
    config.add_route('nouveaux_contacts_ad', '/perturbtrafic/api/nouveaux_contacts_ad')
    config.add_route('nouveaux_contacts_ad_slash', '/perturbtrafic/api/nouveaux_contacts_ad/')
    # Mise à jour groupes AD
    config.add_route('mise_a_jours_groupes_ad', '/perturbtrafic/api/mise_a_jours_groupes_ad')
    config.add_route('mise_a_jours_groupes_ad_slash', '/perturbtrafic/api/mise_a_jours_groupes_ad/')

