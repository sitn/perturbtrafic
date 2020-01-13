import { HttpClient, HttpHeaders, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { forkJoin, Observable, of, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { AutreEvenementServerSave } from '../models/evenement/IAutreEvenement';
import { ChantierServerSave, ICategorieChantier } from '../models/evenement/IChantier';
import { IEvenementImpression, IEvenementServerEdition, IEvenementType, IEvenementLibelle } from '../models/evenement/IEvenement';
import { EvenementEcheance, IEvenementEcheanceServer } from '../models/evenement/IEvenementEcheance';
import { EvenementFormValues } from '../models/evenement/IEvenementForm';
import { FouilleServerSave, IPlanTypeFouille } from '../models/evenement/IFouilleEvenement';
import { ManifestationServerSave } from '../models/evenement/IManifestationsEvenement';
import { RechercheEvenement } from '../models/evenement/IRechercheEvenement';
import { IResultatEvenement, IResultatEvenementServer, ResultatEvenement } from '../models/evenement/IResultatEvenement';
import { IAxeMaintenance } from '../models/IAxeMaintenance';
import { ICommune } from '../models/ICommune';
import { Conflit, IConflitServer } from '../models/IConflit';
import {
  ContactPreavisServerSave,
  ContactServerSave,
  IContact,
  IContactPreavis,
  IContactPreavisUrgence,
  IContactAvisPrTouche,
  IContactAutorisation,
  ContactAutorisationServerSave,
} from '../models/IContact';
import { IDestinataireFacturation } from '../models/IDestinataireFacturation';
import { ILocalite, ILocaliteNPA } from '../models/ILocalite';
import { IOrganisme, OrganismeServerSave } from '../models/IOrganisme';
import { IPointRepere } from '../models/IPointRepere';
import { ReperageGridLine } from '../models/IReperage';
import { User, IUser, IUserAD } from '../models/IUser';
import { FermetureServerSave } from '../models/perturbation/IFermeturePerturbation';
import { OccupationServerSave } from '../models/perturbation/IOccupationPerturbation';
import {
  IPerturbationEtat,
  IPerturbationImpression,
  IPerturbationServerEdition,
  IPerturbationType,
  PerturbationFormValues,
} from '../models/perturbation/IPerturbation';
import { RecherchePerturbation } from '../models/perturbation/IRecherchePerturbation';
import { IResultatPerturbationServer, ResultatPerturbation } from '../models/perturbation/IResultatPerturbation';
import { ConfigService } from './config.service';
import { NavigationService } from './navigation.service';
import { IAutorisations } from '../models/IAutorisations';
import { ITypeOccupation } from '../models/ITypeOccupation';
import { ISuggestion } from '../models/ISuggestion';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // private wsBaseUrl = 'http://10.1.3.162:6543/perturbtrafic/api/';
  // private wsBaseUrl = '/api/';
  private wsBaseUrl; // = 'http://perturbtrafic.arxit.com/perturbtrafic/api/';

  private _requerants = ['MMI', 'MBA', 'SGI'];
  private _responsables = ['MMI', 'MBA', 'SGI'];

  private _etats = [
    { name: 'En attente', code: 0 },
    { name: 'Acceptée', code: 1 },
    { name: 'Refusée', code: 2 },
  ];


  constructor(private http: HttpClient, private navigationService: NavigationService, private configService: ConfigService) {
    this.wsBaseUrl = configService.getWsPath();
  }

  appendIdEntityParam(params: FormData, user: IUser): void {
    if (user && user.currentEntity && user.currentEntity.id) {
      params.append('idEntite', user.currentEntity.id.toString());
    }
  }

  /*
    Current User
  */

  login(login: string, password: string): Observable<IUser> {
    const body = new FormData();
    body.append('login', login);
    body.append('password', password);

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.post<IUser>(
      this.wsBaseUrl + 'login', body, { headers: headers, withCredentials: true }).pipe(
        map((user: any) => {
          console.log(user);
          /* if (user.entites && user.entites.length > 0) {
            user.currentEntity = user.entites[0];
          } */
          return user;
        }),
        catchError((error: HttpErrorResponse) => {
          return of(error as any);
        })
      );
  }

  logout(): Observable<any> {
    return this.http.get<any>(this.wsBaseUrl + 'logout').pipe(
      map((res: any) => {
        return res;
      })
    );
  }

  getUserEntities(): Observable<{ id: number, nom: string }[]> {
    return this.http.get<any>(this.wsBaseUrl + 'entites', { withCredentials: true }).pipe(
      map((res: any) => {
        return res;
      })
    );
  }

  getLoggedUser(): Observable<IUser> {
    return this.http.get<IUser>(this.wsBaseUrl + 'logged_user', { withCredentials: true }).pipe(
      map((res: any) => {
        return res;
      })
    );
  }

  getUserAutorisations(): Observable<IAutorisations> {
    return this.http.get<IAutorisations>(this.wsBaseUrl + 'autorisations_fonctions', { withCredentials: true }).pipe(
      map((res: IAutorisations) => {
        return res;
      })
    );
  }


  /*
  API Contacts
   */

  getContacts(): Observable<IContact[]> {
    return this.http.get<IContact[]>(this.wsBaseUrl + 'contacts').pipe(
      map((contacts: IContact[]) => {
        contacts.sort((l1, l2) => {
          let l1Nom;
          let l2Nom;
          if (l1.nom) {
            l1Nom = l1.nom.toLowerCase();
          }
          if (l2.nom) {
            l2Nom = l2.nom.toLowerCase();
          }
          if (l1Nom < l2Nom) { return -1; }
          if (l1Nom > l2Nom) { return 1; }
          return 0;
        });
        return contacts.map((contact: IContact) => {
          contact.nomComplet = contact.nom + ' ' + contact.prenom;
          if (contact.login) {
            contact.nomCompletEtLogin = `${contact.nom} ${contact.prenom} (${contact.login})`;
          } else {
            contact.nomCompletEtLogin = `${contact.nom} ${contact.prenom}`;
          }
          return contact;
        });
      })
    );
  }

  getContactsByEntity(entityId: number): Observable<IContact[]> {

    const params = new HttpParams().set('idEntite', entityId.toString());
    console.log(params);
    return this.http.get<IContact[]>(this.wsBaseUrl + 'contacts_entite',
      { withCredentials: true, params: params }
    ).pipe(
      map((contacts: IContact[]) => {
        return contacts.map((contact: IContact) => {
          contact.nomComplet = contact.nom + ' ' + contact.prenom;
          return contact;
        });
      })
    );
  }

  getUsers(): Observable<IUser[]> {
    return this.http.get<IUser[]>(this.wsBaseUrl + 'contacts_login').pipe(
      map((users: IUser[]) => {
        users.sort((l1, l2) => {
          let l1Nom;
          let l2Nom;
          if (l1.nom) {
            l1Nom = l1.nom.toLowerCase();
          }
          if (l2.nom) {
            l2Nom = l2.nom.toLowerCase();
          }
          if (l1Nom < l2Nom) { return -1; }
          if (l1Nom > l2Nom) { return 1; }
          return 0;
        });
        return users.map(user => {
          user.nomComplet = user.nom + ' ' + user.prenom;
          return user;
        });
      })
    );
  }

  checkNewUsers(): Observable<IUserAD[]> {
    return this.http.get<IUserAD[]>(this.wsBaseUrl + 'nouveaux_contacts_ad', { withCredentials: true }).pipe(
      map((contacts: IUserAD[]) => {
        contacts.sort((l1, l2) => {
          let l1Nom;
          let l2Nom;
          if (l1.sn) {
            l1Nom = l1.sn.toLowerCase();
          }
          if (l2.sn) {
            l2Nom = l2.sn.toLowerCase();
          }
          if (l1Nom < l2Nom) { return -1; }
          if (l1Nom > l2Nom) { return 1; }
          return 0;
        });
        return contacts;
      })
    );
  }

  updateNewUsers(users: IUserAD[]): Observable<any> {
    const body = new FormData();
    body.append('contacts', JSON.stringify(users));

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.post<IUserAD[]>(this.wsBaseUrl + 'nouveaux_contacts_ad', body, { headers: headers, withCredentials: true }).pipe(
      map((res: any) => {
        return res;
      })
    );
  }

  /*
    Preavis Fermetures / Occupations
  */
  getContactsPreavis() {
    return this.http.get<IContactPreavis[]>(this.wsBaseUrl + 'contacts_potentiels_avis_perturbation').pipe(
      map((contacts: IContactPreavis[]) => {
        return contacts.map((contact: IContactPreavis) => {
          contact.nomComplet = contact.nom + ' ' + contact.prenom;
          return contact;
        });
      })
    );
  }

  updateContactPreavis(preavisContact: IContactPreavis) {
    const formatedContact = new ContactPreavisServerSave(preavisContact);
    const body = new FormData();
    Object.keys(formatedContact).forEach(key => {
      if (formatedContact[key]) {
        body.append(key, formatedContact[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.put<any>(
      this.wsBaseUrl + 'contacts_potentiels_avis_perturbation', body, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }

  deleteContactPreavis(preavisContactId: number) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.delete<any>(
      this.wsBaseUrl + 'contacts_potentiels_avis_perturbation/' + preavisContactId, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la suppression');
          return throwError(response.error);
        })
      );
  }

  addNewContactPreavis(preavisContact: IContactPreavis) {
    const formatedContact = new ContactPreavisServerSave(preavisContact);
    const body = new FormData();
    Object.keys(formatedContact).forEach(key => {
      if (formatedContact[key]) {
        body.append(key, formatedContact[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.post<any>(
      this.wsBaseUrl + 'contacts_potentiels_avis_perturbation', body, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }

  /*
   Autorisations
 */
  getAutorisationsAccordees(entityId: number) {

    const params = new HttpParams().set('idEntite', entityId.toString());
    console.log(params);
    return this.http.get<IContactAutorisation[]>(this.wsBaseUrl + 'autorisations_accordees',
      { withCredentials: true, params: params }
    ).pipe(
      map((contacts: IContactAutorisation[]) => {
        return contacts.map((contact: IContactAutorisation) => {
          contact.nomComplet = contact.nom + ' ' + contact.prenom;
          return contact;
        });
      })
    );
  }

  getAutorisationsRecues() {
    return this.http.get<IContactAutorisation[]>(this.wsBaseUrl + 'autorisations_recues', { withCredentials: true }).pipe(
      map((contacts: IContactAutorisation[]) => {
        return contacts.map((contact: IContactAutorisation) => {
          contact.nomComplet = contact.nom + ' ' + contact.prenom;
          return contact;
        });
      })
    );
  }

  updateContactAutorisation(autorisationContact: IContactAutorisation) {
    const formatedContact = new ContactAutorisationServerSave(autorisationContact);
    const body = new FormData();
    Object.keys(formatedContact).forEach(key => {
      if (formatedContact[key]) {
        body.append(key, formatedContact[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.put<any>(
      this.wsBaseUrl + 'autorisations', body, { headers: headers, withCredentials: true }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }

  deleteContactAutorisation(autorisationContactId: number) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.delete<any>(
      this.wsBaseUrl + 'autorisations/' + autorisationContactId, { headers: headers, withCredentials: true }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la suppression');
          return throwError(response.error);
        })
      );
  }

  addNewContactAutorisation(autorisationContact: IContactAutorisation) {
    const formatedContact = new ContactAutorisationServerSave(autorisationContact);
    const body = new FormData();
    Object.keys(formatedContact).forEach(key => {
      if (formatedContact[key]) {
        body.append(key, formatedContact[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.post<any>(
      this.wsBaseUrl + 'autorisations', body, { headers: headers, withCredentials: true }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }


  /*
  Avis d'urgence
  */
  getContactsPreavisUrgence() {
    return this.http.get<IContactPreavisUrgence[]>(this.wsBaseUrl + 'contacts_avis_fermeture_urgence').pipe(
      map((contacts: IContactPreavisUrgence[]) => {
        return contacts.map((contact: IContactPreavisUrgence) => {
          contact.nomComplet = contact.nom + ' ' + contact.prenom;
          return contact;
        });
      })
    );
  }



  deleteContactPreavisUrgence(preavisContactUrgenceId: number) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.delete<any>(
      this.wsBaseUrl + 'contacts_avis_fermeture_urgence/' + preavisContactUrgenceId, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la suppression');
          return throwError(response.error);
        })
      );
  }

  addNewContactPreavisUrgence(preavisContactUrgenceId: number) {
    const formatedContact = { idContact: preavisContactUrgenceId };
    const body = new FormData();
    Object.keys(formatedContact).forEach(key => {
      if (formatedContact[key]) {
        body.append(key, formatedContact[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.post<any>(
      this.wsBaseUrl + 'contacts_avis_fermeture_urgence', body, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }


  saveContact(contact: IContact) {
    const formatedContact = new ContactServerSave(contact);
    const body = new FormData();
    Object.keys(formatedContact).forEach(key => {
      if (formatedContact[key]) {
        body.append(key, formatedContact[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.post<any>(
      this.wsBaseUrl + 'contacts', body, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }

  updateContact(contact: IContact) {
    const formatedContact = new ContactServerSave(contact);
    const body = new FormData();
    Object.keys(formatedContact).forEach(key => {
      if (formatedContact[key]) {
        body.append(key, formatedContact[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.put<any>(
      this.wsBaseUrl + 'contacts', body, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );

  }

  deleteContact(id: number) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.delete<any>(
      this.wsBaseUrl + 'contacts/' + id, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la suppression');
          return throwError(response.error);
        })
      );
  }

  /*
Avis Pr touches
*/
  getContactsAvisPrTouches() {
    return this.http.get<IContactAvisPrTouche[]>(this.wsBaseUrl + 'contact_avis_pr_touche').pipe(
      map((contacts: IContactAvisPrTouche[]) => {
        return contacts.map((contact: IContactAvisPrTouche) => {
          contact.nomComplet = contact.nom + ' ' + contact.prenom;
          return contact;
        });
      })
    );
  }

  deleteContactAvisPrTouches(prContactId: number) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.delete<any>(
      this.wsBaseUrl + 'contact_avis_pr_touche/' + prContactId, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((error) => {
          this.navigationService.openErrorDialog(error, 'Erreur lors de la suppresion');
          return throwError(error);
        })
      );
  }

  addNewContactAvisPrTouches(prContactId: number) {
    const formatedContact = { idContact: prContactId };
    const body = new FormData();
    Object.keys(formatedContact).forEach(key => {
      if (formatedContact[key]) {
        body.append(key, formatedContact[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    return this.http.post<any>(
      this.wsBaseUrl + 'contact_avis_pr_touche', body, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((error) => {
          this.navigationService.openErrorDialog(error, 'Erreur lors de la sauvegarde');
          return throwError(error);
        })
      );
  }



  /*
  API Organismes
  */

  getOrganismes(): Observable<IOrganisme[]> {
    return this.http.get<IOrganisme[]>(this.wsBaseUrl + 'organismes').pipe(
      map((organismes: IOrganisme[]) => {
        organismes.sort((l1, l2) => {
          let l1Nom;
          let l2Nom;
          if (l1.nom) {
            l1Nom = l1.nom.toLowerCase();
          }
          if (l2.nom) {
            l2Nom = l2.nom.toLowerCase();
          }
          if (l1Nom < l2Nom) { return -1; }
          if (l1Nom > l2Nom) { return 1; }
          return 0;
        });
        return organismes;
      })
    );
  }

  saveOrganisme(organisme: IOrganisme) {
    const formatedOrganisme = new OrganismeServerSave(organisme);
    const body = new FormData();
    Object.keys(formatedOrganisme).forEach(key => {
      if (formatedOrganisme[key]) {
        body.append(key, formatedOrganisme[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.post<any>(
      this.wsBaseUrl + 'organismes', body, { headers: headers }).pipe(
        map((response: any) => {
          return response;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }

  updateOrganisme(organisme: IOrganisme) {
    const formatedOrganisme = new OrganismeServerSave(organisme);
    const body = new FormData();
    Object.keys(formatedOrganisme).forEach(key => {
      if (formatedOrganisme[key]) {
        body.append(key, formatedOrganisme[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.put<any>(
      this.wsBaseUrl + 'organismes', body, { headers: headers }).pipe(
        map((response: any) => {
          return response;
        }),
        catchError((error) => {
          this.navigationService.openErrorDialog(error, 'Erreur lors de la sauvegarde');
          return throwError(error);
        })
      );
  }

  deleteOrganisme(id: number) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.delete<any>(
      this.wsBaseUrl + 'organismes/' + id, { headers: headers }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la suppression');
          return throwError(response.error);
        })
      );
  }

  /*
  API Evénements
   */

  getTypeEvenements(): Observable<IEvenementType[]> {
    return this.http.get<IEvenementType[]>(this.wsBaseUrl + 'types_evenements');
  }

  getLibellesEvenements(user: IUser): Observable<IEvenementLibelle[]> {
    let params = '';
    if (user && user.currentEntity && user.currentEntity.id) {
      params = '?idEntite=' + user.currentEntity.id.toString();
    }
    return this.http.get<IEvenementLibelle[]>(this.wsBaseUrl + 'libelles_evenements' + params, { withCredentials: true }).pipe(
      map((libelles: IEvenementLibelle[]) => {
        return libelles.map(lib => {
          if (lib.numero_dossier) {
            lib.label = lib.description + ' : ' + lib.libelle + ' (' + lib.numero_dossier + ')';
            return lib;
          } else {
            lib.label = lib.description + ' : ' + lib.libelle;
            return lib;
          }
        });
      })
    );
  }

  getEvenementsEcheances(user: IUser): Observable<EvenementEcheance[]> {
    let params = '';
    if (user && user.currentEntity && user.currentEntity.id) {
      params = '?idEntite=' + user.currentEntity.id.toString();
    }
    return this.http.get<IEvenementEcheanceServer[]>(this.wsBaseUrl + 'evenements_echeance' + params, { withCredentials: true }).pipe(
      map((echeances: IEvenementEcheanceServer[]) => {
        if (echeances && echeances.length > 0) {
          return echeances.map((echeance: IEvenementEcheanceServer) => {
            return new EvenementEcheance(echeance);
          });
        } else {
          return [];
        }
      })
    );
  }

  searchEvenement(rechercheObject: RechercheEvenement, user: IUser): Observable<IResultatEvenement[]> {

    // let httpParams = new HttpParams();
    const body = new FormData();
    Object.keys(rechercheObject).forEach(key => {
      if (rechercheObject[key]) {
        body.append(key, rechercheObject[key]);
      }
    });

    this.appendIdEntityParam(body, user);

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    console.log(body);
    // this.http.request()
    return this.http.post<IResultatEvenementServer[]>(
      this.wsBaseUrl + 'recherche/evenements', body, { headers: headers, withCredentials: true }).pipe(
        map((resultats: IResultatEvenementServer[]) => {
          if (resultats && resultats.length > -1) {
            return resultats.map((evenement: IResultatEvenementServer) => {
              return new ResultatEvenement(evenement);
            });
          } else {
            if (resultats && (resultats as any).message) {
              throw new Error((resultats as any).message);
            } else {
              throw new Error('Erreur lors de la recherche');
            }
          }
        }),
        catchError((error) => {
          /* let message = 'Erreur survenue';
          if (error && error.message) {
            message = error.message;
          } */
          this.navigationService.openErrorDialog(error, 'Erreur');
          return throwError(error);
        })
      );
  }

  getFullEvenementById(evenementId: any): Observable<IEvenementServerEdition> {
    return this.http.get<IEvenementServerEdition>(this.wsBaseUrl + `evenement_edition/${evenementId}`, { withCredentials: true }).pipe(
      map((resultat: IEvenementServerEdition) => {
        return resultat;
      }),
      catchError((error) => {
        /* let message = 'Erreur survenue';
        if (error && error.message) {
          message = error.message;
        } */
        if (error.message) {
          error = error.message;
        }
        this.navigationService.openErrorDialog(`Une ereur est survenue lors du chargement de l'événement`, `Ereur`);
        return throwError(error);
      })
    );
  }

  getEvenementImpression(evenementId): Observable<IEvenementImpression> {
    return this.http.get<IEvenementImpression>(this.wsBaseUrl + `evenement_impression/${evenementId}`).pipe(
      map((resultat: IEvenementImpression) => {
        return resultat;
      }),
      catchError((error) => {
        this.navigationService.openErrorDialog(`Une ereur est survenue lors du chargement de la perturbation`, `Ereur`);
        return throwError(error);
      })
    );
  }

  getDossierEvenementImpression(evenementId): Observable<{ evenement: IEvenementImpression, perturbations: IPerturbationImpression[] }> {
    return this.http.get<{ evenement: IEvenementImpression, perturbations: IPerturbationImpression[] }>
      (this.wsBaseUrl + `evenement_perturbations_impression/${evenementId}`).pipe(
        map((resultat: { evenement: IEvenementImpression, perturbations: IPerturbationImpression[] }) => {
          return resultat;
        }),
        catchError((error) => {
          this.navigationService.openErrorDialog(`Une ereur est survenue lors du chargement du dossier d'impression`, `Ereur`);
          return throwError(error);
        })
      );
  }

  saveEvenement(saveObject: EvenementFormValues, geometries?: any[]): Observable<any> {
    let serverFormatedEvenement; //  = new EvenementServerForSave(saveObject);
    switch (saveObject.type.type) {
      case 1: {
        serverFormatedEvenement = new AutreEvenementServerSave(saveObject, geometries);
        break;
      }
      case 2: {
        serverFormatedEvenement = new ChantierServerSave(saveObject, geometries);
        break;
      }
      case 3: {
        serverFormatedEvenement = new FouilleServerSave(saveObject, geometries);
        break;
      }
      case 4: {
        serverFormatedEvenement = new ManifestationServerSave(saveObject, geometries);
        break;
      }
    }
    const body = new FormData();
    Object.keys(serverFormatedEvenement).forEach(key => {
      if (serverFormatedEvenement[key]) {
        body.append(key, serverFormatedEvenement[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.post<any>(
      this.wsBaseUrl + 'evenement_edition', body, { headers: headers, withCredentials: true }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }


  editEvenement(saveObject: EvenementFormValues, geometries?: any[]): Observable<any> {
    let serverFormatedEvenement; //  = new EvenementServerForSave(saveObject);
    switch (saveObject.type.type) {
      case 1: {
        serverFormatedEvenement = new AutreEvenementServerSave(saveObject, geometries);
        break;
      }
      case 2: {
        serverFormatedEvenement = new ChantierServerSave(saveObject, geometries);
        break;
      }
      case 3: {
        serverFormatedEvenement = new FouilleServerSave(saveObject, geometries);
        break;
      }
      case 4: {
        serverFormatedEvenement = new ManifestationServerSave(saveObject, geometries);
        break;
      }
    }
    const body = new FormData();
    Object.keys(serverFormatedEvenement).forEach(key => {
      if (serverFormatedEvenement[key]) {
        body.append(key, serverFormatedEvenement[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.put<any>(
      this.wsBaseUrl + 'evenement_edition', body, { headers: headers, withCredentials: true }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }

  deleteEvenement(id: number) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.delete<any>(
      this.wsBaseUrl + 'evenements/' + id, { headers: headers, withCredentials: true }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la suppression');
          return throwError(response.error);
        })
      );
  }

  /*
  API Perturbations
  */

  getTypePerturbations(): Observable<IPerturbationType[]> {
    return this.http.get<IPerturbationType[]>(this.wsBaseUrl + 'types_perturbations');
  }

  getFullPerturbationById(evenementId: any): Observable<IPerturbationServerEdition> {
    return this.http.get<IPerturbationServerEdition>(this.wsBaseUrl + `perturbation_edition/${evenementId}`, { withCredentials: true })
      .pipe(
        map((resultat: IPerturbationServerEdition) => {
          return resultat;
        }),
        catchError((error) => {
          if (error.message) {
            error = error.message;
          }
          this.navigationService.openErrorDialog(`Une ereur est survenue lors du chargement de la perturbation`, `Ereur`);
          return throwError(error);
        })
      );
  }

  getPerturbationImpression(perturbationId): Observable<IPerturbationImpression> {
    return this.http.get<IPerturbationImpression>(this.wsBaseUrl + `perturbation_impression/${perturbationId}`).pipe(
      map((resultat: IPerturbationImpression) => {
        return resultat;
      }),
      catchError((error) => {
        this.navigationService.openErrorDialog(`Une ereur est survenue lors du chargement de la perturbation`, `Ereur`);
        return throwError(error);
      })
    );
  }

  searchPerturbations(rechercheObject: RecherchePerturbation, user: IUser): Observable<ResultatPerturbation[]> {
    const body = new FormData();
    Object.keys(rechercheObject).forEach(key => {
      if (rechercheObject[key]) {
        body.append(key, rechercheObject[key]);
      }
    });

    this.appendIdEntityParam(body, user);

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');
    console.log(body);
    return this.http.post<IResultatPerturbationServer[]>(
      this.wsBaseUrl + 'recherche/perturbations', body, { headers: headers, withCredentials: true }).pipe(
        map((resultats: IResultatPerturbationServer[]) => {
          if (resultats && resultats.length > -1) {
            return resultats.map((evenement: IResultatPerturbationServer) => {
              return new ResultatPerturbation(evenement);
            });
          } else {
            if (resultats && (resultats as any).message) {
              throw new Error((resultats as any).message);
            } else {
              throw new Error('Erreur lors de la recherche');
            }
          }
        }),
        catchError((error) => {
          /* let message = 'Erreur survenue';
          if (error && error.message) {
            message = error.message;
          } */
          if (error.message) {
            error = error.message;
          }
          this.navigationService.openErrorDialog(error, 'Erreur');
          return throwError(error);
        })
      );
  }

  savePerturbation(saveObject: PerturbationFormValues, user: IUser, geometries?: any[],
    deviations?: any[], contacts?: number[]): Observable<any> {
    let serverFormatedPerturbation;
    switch (saveObject.type) {
      case 1: {
        serverFormatedPerturbation = new FermetureServerSave(saveObject, geometries, deviations, contacts);
        break;
      }
      case 2: {
        serverFormatedPerturbation = new OccupationServerSave(saveObject, geometries, contacts);
        break;
      }
    }
    delete serverFormatedPerturbation.idPerturbation;
    const body = new FormData();
    Object.keys(serverFormatedPerturbation).forEach(key => {
      if (serverFormatedPerturbation[key]) {
        body.append(key, serverFormatedPerturbation[key]);
      }
    });

    this.appendIdEntityParam(body, user);

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.post<any>(
      this.wsBaseUrl + 'perturbation_edition', body, { headers: headers, withCredentials: true }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response: HttpErrorResponse) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }

  editPerturbation(saveObject: PerturbationFormValues, geometries?: any[], deviations?: any[], contacts?: number[]): Observable<any> {
    let serverFormatedPerturbation;
    switch (saveObject.type) {
      case 1: {
        serverFormatedPerturbation = new FermetureServerSave(saveObject, geometries, deviations, contacts);
        break;
      }
      case 2: {
        serverFormatedPerturbation = new OccupationServerSave(saveObject, geometries, contacts);
        break;
      }
    }
    const body = new FormData();
    Object.keys(serverFormatedPerturbation).forEach(key => {
      if (serverFormatedPerturbation[key]) {
        body.append(key, serverFormatedPerturbation[key]);
      }
    });

    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.put<any>(
      this.wsBaseUrl + 'perturbation_edition', body, { headers: headers, withCredentials: true }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la sauvegarde');
          return throwError(response.error);
        })
      );
  }

  deletePerturbation(id: number) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers.append('Accept', '*/*');

    return this.http.delete<any>(
      this.wsBaseUrl + 'perturbations/' + id, { headers: headers, withCredentials: true }).pipe(
        map((resultats: any) => {
          return resultats;
        }),
        catchError((response) => {
          let message = 'Erreur survenue';
          if (response.error && response.error.message) {
            message = response.error.message;
          } else if (response.error) {
            message = response.message;
          }
          this.navigationService.openErrorDialog(message, 'Erreur lors de la suppression');
          return throwError(response.error);
        })
      );
  }

  /*
  API Conflits
  */

  getConflits(): Observable<Conflit[]> {
    return this.http.get<IConflitServer[]>(this.wsBaseUrl + 'conflits_perturbations').pipe(
      map((conflits: IConflitServer[]) => {
        if (conflits && conflits.length > 0) {
          return conflits.map((conflit: IConflitServer) => {
            return new Conflit(conflit);
          });
        } else {
          return [];
        }
      })
    );
  }

  getConflitsByEvenementId(evenementId): Observable<Conflit[]> {
    return this.http.get<IConflitServer[]>(this.wsBaseUrl + `conflits_perturbations/${evenementId}`).pipe(
      map((conflits: IConflitServer[]) => {
        if (conflits && conflits.length > 0) {
          return conflits.map((conflit: IConflitServer) => {
            return new Conflit(conflit);
          });
        } else {
          return [];
        }
      })
    );
  }

  /*
  API Autres
  */

  getAxeMaintenances(): Observable<IAxeMaintenance[]> {
    return this.http.get<IAxeMaintenance[]>(this.wsBaseUrl + 'axes_routiers');
  }

  getPrByAxeMaintenance(axeMaintenance: IAxeMaintenance): Observable<IPointRepere[]> {
    const params = new HttpParams().set('id', axeMaintenance.nom_complet);
    console.log(params);
    return this.http.get<IPointRepere[]>(this.wsBaseUrl + `pr_par_axe_routier`, { params: params });
  }


  getTypeReperages(): Observable<any[]> {
    return this.http.get<any[]>(this.wsBaseUrl + 'types_reperages');
  }

  getGeometryReperages(reperages: ReperageGridLine[]): Observable<any[]> {
    const reperagesObservables = [];
    if (reperages && reperages.length > 0) {
      reperages.forEach(reperage => {
        const axe = reperage.axe.nom_complet.split(':');
        const params = new HttpParams().set('f_prop', axe[0])
          .set('f_axe', axe[1])
          .set('f_sens', axe[2])
          .set('f_pr_d', reperage.debutPr.secteur_nom)
          .set('f_pr_f', reperage.finPr.secteur_nom)
          .set('f_dist_d', reperage.distanceDebut.toString())
          .set('f_dist_f', reperage.distanceFin.toString())
          .set('f_ecart_d', '1')
          .set('f_ecart_f', '0')
          .set('f_usaneg', 'false');
        console.log(params);
        reperagesObservables.push(this.http.get<any>(this.wsBaseUrl + `geometry_reperage`, { params: params }).pipe(
          map(res => {
            if (res && Array.isArray(res)) {
              res[0].id = reperage.id;
              return res[0];
            } else {
              return res;
            }
          })
        ));
      });
      return forkJoin(reperagesObservables);
    } else {
      return of([]);
    }
  }

  getCategorieChantiers(): Observable<ICategorieChantier[]> {
    return this.http.get<ICategorieChantier[]>(this.wsBaseUrl + 'categories_chantiers');
  }

  getPlanTypeFouille(): Observable<IPlanTypeFouille[]> {
    return this.http.get<IPlanTypeFouille[]>(this.wsBaseUrl + 'plans_types_fouille');
  }

  getEtats(): Observable<{ name: string, code: number }[]> {
    return of(this._etats);
  }

  getTypesOccupations(): Observable<ITypeOccupation[]> {
    return this.http.get<ITypeOccupation[]>(this.wsBaseUrl + 'types_occupations');
  }


  getEtatsPerturbations(): Observable<IPerturbationEtat[]> {
    return this.http.get<IEvenementType[]>(this.wsBaseUrl + 'etats_perturbations');
  }

  // Evenements
  getRequerants(): Observable<string[]> {
    return of(this._requerants);
  }

  getResponsables(): Observable<string[]> {
    return of(this._responsables);
  }


  /*   getLocalites(): Observable<ILocalite[]> {
      return this.http.get<ILocalite[]>(this.wsBaseUrl + 'localites');
    } */

  getLocalitesNPA(): Observable<ILocaliteNPA[]> {
    return this.http.get<ILocaliteNPA[]>(this.wsBaseUrl + 'localites_npa');
  }

  getCommunes(): Observable<ICommune[]> {
    return this.http.get<ICommune[]>(this.wsBaseUrl + 'communes');
  }

  getDestinatairesFacturations(): Observable<IDestinataireFacturation[]> {
    return this.http.get<IDestinataireFacturation[]>(this.wsBaseUrl + 'destinataires_facturation');
  }


  // Suggestions
  getListOfSuggestions(listName: string): Observable<ISuggestion[]> {
    return this.http.get<string[]>(this.wsBaseUrl + 'suggestion_by_liste_name/' + listName).pipe(
      map(res => {
        const suggestions: any[] = [];
        res.forEach(val => {
          suggestions.push({ id: val, name: val });
        });
        return suggestions;
      })
    );
  }


}
