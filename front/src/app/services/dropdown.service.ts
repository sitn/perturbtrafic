import { EventEmitter, Injectable } from '@angular/core';

import { ICommune } from '../models/ICommune';
import { IContact } from '../models/IContact';
import { IDestinataireFacturation } from '../models/IDestinataireFacturation';
import { ILocalite, ILocaliteNPA } from '../models/ILocalite';
import { IOrganisme } from '../models/IOrganisme';
import { ApiService } from './api.service';
import { ICategorieChantier } from '../models/evenement/IChantier';
import { IPlanTypeFouille } from '../models/evenement/IFouilleEvenement';
import { UserService } from './user.service';
import { ITypeOccupation } from '../models/ITypeOccupation';
import { ConfigService } from './config.service';
import { ISuggestion } from '../models/ISuggestion';

@Injectable({
    providedIn: 'root'
})
export class DropDownService {

    contacts: IContact[];
    entityContacts: IContact[];
    organismes: IOrganisme[];
    localitesNPA: ILocaliteNPA[];
    typesOccupations: string[];
    divisions: ISuggestion[];
    voiesCondamnees: ISuggestion[];
    regulations: ISuggestion[];
    localitesPrimitiveNPA: string[];
    communes: ICommune[];
    categoriesChantier: ICategorieChantier[];
    plansTypeFouille: IPlanTypeFouille[];
    destinatairesFacturations: IDestinataireFacturation[];
    libellesEvenements: any[];

    public contactReceived$: EventEmitter<{ contacts: IContact[], lastUpdatedId?: number }>;
    public entityContactReceived$: EventEmitter<IContact[]>;
    public organismesReceived$: EventEmitter<IOrganisme[]>;
    public localitesNPAReceived$: EventEmitter<ILocaliteNPA[]>;
    public typesOccupationsReceived$: EventEmitter<string[]>;
    public regulationsReceived$: EventEmitter<ISuggestion[]>;
    public divisionsReceived$: EventEmitter<ISuggestion[]>;
    public voiesCondamneesReceived$: EventEmitter<ISuggestion[]>;
    public localitesPrimitiveNPAReceived$: EventEmitter<string[]>;
    public communesReceived$: EventEmitter<ICommune[]>;
    public categoriesChantierReceived$: EventEmitter<ICategorieChantier[]>;
    public plansTypeFouilleReceived$: EventEmitter<IPlanTypeFouille[]>;
    public destinatairesFacturationsReceived$: EventEmitter<IDestinataireFacturation[]>;
    public libellesEvenementsReceived$: EventEmitter<any[]>;

    constructor(private apiService: ApiService, private userService: UserService, private configService: ConfigService) {
        this.contacts = [];
        this.entityContacts = [];
        this.organismes = [];
        this.localitesNPA = [];
        this.typesOccupations = [];
        this.divisions = [];
        this.regulations = [];
        this.voiesCondamnees = [];
        this.localitesPrimitiveNPA = [];
        this.communes = [];
        this.categoriesChantier = [];
        this.destinatairesFacturations = [];
        this.plansTypeFouille = [];

        this.contactReceived$ = new EventEmitter();
        this.entityContactReceived$ = new EventEmitter();
        this.organismesReceived$ = new EventEmitter();
        this.localitesNPAReceived$ = new EventEmitter();
        this.typesOccupationsReceived$ = new EventEmitter();
        this.divisionsReceived$ = new EventEmitter();
        this.regulationsReceived$ = new EventEmitter();
        this.voiesCondamneesReceived$ = new EventEmitter();
        this.localitesPrimitiveNPAReceived$ = new EventEmitter();
        this.communesReceived$ = new EventEmitter();
        this.categoriesChantierReceived$ = new EventEmitter();
        this.plansTypeFouilleReceived$ = new EventEmitter();
        this.destinatairesFacturationsReceived$ = new EventEmitter();
        this.libellesEvenementsReceived$ = new EventEmitter();
    }

    getContacts(lastUpdatedId?: number): void {
        this.apiService.getContacts().subscribe(contacts => {
            contacts.sort((c1, c2) => {
                let c1Nom = '';
                let c2Nom = '';
                if (c1.nom) {
                    c1Nom = c1.nom.toLowerCase();
                }
                if (c2.nom) {
                    c2Nom = c2.nom.toLowerCase();
                }
                return c1Nom.localeCompare(c2Nom);
            });
            this.contacts = [...contacts];
            this.contactReceived$.emit({ contacts: this.contacts, lastUpdatedId: lastUpdatedId });
        });
    }

    getContactsByEntity(entityId: number): void {
        this.apiService.getContactsByEntity(entityId).subscribe(contacts => {
            contacts.sort((c1, c2) => {
                let c1Nom = '';
                let c2Nom = '';
                if (c1.nom) {
                    c1Nom = c1.nom.toLowerCase();
                }
                if (c2.nom) {
                    c2Nom = c2.nom.toLowerCase();
                }
                return c1Nom.localeCompare(c2Nom);
            });
            this.entityContacts = [...contacts];
            this.entityContactReceived$.emit(this.entityContacts);
        });
    }

    getOrganismes(): void {
        this.apiService.getOrganismes().subscribe(organismes => {
            organismes.sort((c1, c2) => {
                let c1Nom = '';
                let c2Nom = '';
                if (c1.nom) {
                    c1Nom = c1.nom.toLowerCase();
                }
                if (c2.nom) {
                    c2Nom = c2.nom.toLowerCase();
                }
                return c1Nom.localeCompare(c2Nom);
            });
            this.organismes = [...organismes];
            this.organismesReceived$.emit(this.organismes);
        });
    }

    getLocalitesNPA(): void {
        this.apiService.getLocalitesNPA().subscribe(localites => {
            if (localites && Array.isArray(localites)) {
                localites.sort((l1, l2) => {
                    let l1Nom = '';
                    let l2Nom = '';
                    if (l1.npa_nom) {
                        l1Nom = l1.npa_nom.toLowerCase();
                    }
                    if (l2.npa_nom) {
                        l2Nom = l2.npa_nom.toLowerCase();
                    }
                    return l1Nom.localeCompare(l2Nom);
                });
                this.localitesNPA = [...localites];
            } else {
                this.localitesNPA = [];
            }
            this.localitesPrimitiveNPA = this.localitesNPA.map(loc => {
                return loc.npa_nom;
            });
            this.localitesPrimitiveNPAReceived$.emit(this.localitesPrimitiveNPA);
            this.localitesNPAReceived$.emit(this.localitesNPA);
        });
    }

    getTypesOccupations(): void {
        this.apiService.getListOfSuggestions(this.configService.getConfig().listeSuggestions.occupation).subscribe(typesOccupations => {
            if (typesOccupations && Array.isArray(typesOccupations)) {
                const occupations = [];
                typesOccupations.forEach(occupation => {
                    occupations.push(occupation.name);
                });
                this.typesOccupations = [...occupations];
            } else {
                this.typesOccupations = [];
            }
            this.typesOccupationsReceived$.emit(this.typesOccupations);
        });
    }

    getTypesVoiesCondamnees(): void {
        this.apiService.getListOfSuggestions(this.configService.getConfig().listeSuggestions.voieCondamnee).subscribe(voies => {
            if (voies && Array.isArray(voies)) {
                this.voiesCondamnees = [...voies];
            } else {
                this.voiesCondamnees = [];
            }
            this.voiesCondamneesReceived$.emit(this.voiesCondamnees);
        });
    }

    getDivisions(): void {
        this.apiService.getListOfSuggestions(this.configService.getConfig().listeSuggestions.division).subscribe(divisions => {
            if (divisions && Array.isArray(divisions)) {
                this.divisions = [...divisions];
            } else {
                this.divisions = [];
            }
            this.divisionsReceived$.emit(this.divisions);
        });
    }

    getTypesRegulations(): void {
        this.apiService.getListOfSuggestions(this.configService.getConfig().listeSuggestions.regulationPar).subscribe(regulations => {
            if (regulations && Array.isArray(regulations)) {
                this.regulations = [...regulations];
            } else {
                this.regulations = [];
            }
            this.regulationsReceived$.emit(this.regulations);
        });
    }

    getLibellesEvenements(): void {
        this.apiService.getLibellesEvenements(this.userService.currentUser).subscribe(libelles => {
            if (libelles && Array.isArray(libelles)) {
                this.libellesEvenements = [...libelles];
            } else {
                this.libellesEvenements = [];
            }
            this.libellesEvenementsReceived$.emit(this.libellesEvenements);
        });
    }

    getCommunes(): void {
        this.apiService.getCommunes().subscribe(communes => {
            if (communes && Array.isArray(communes)) {
                communes.sort((l1, l2) => {
                    let l1Nom = '';
                    let l2Nom = '';
                    if (l1.name) {
                        l1Nom = l1.name.toLowerCase();
                    }
                    if (l2.name) {
                        l2Nom = l2.name.toLowerCase();
                    }
                    return l1Nom.localeCompare(l2Nom);
                });
                this.communes = [...communes];
            } else {
                this.communes = [];
            }
            this.communesReceived$.emit(this.communes);
        });
    }

    getCategoriesChantier(): void {
        this.apiService.getCategorieChantiers().subscribe(categories => {
            this.categoriesChantier = [...categories];
            this.categoriesChantierReceived$.emit(this.categoriesChantier);
        });
    }

    getPlansTypeFouille(): void {
        this.apiService.getPlanTypeFouille().subscribe(plans => {
            this.plansTypeFouille = [...plans];
            this.plansTypeFouilleReceived$.emit(this.plansTypeFouille);
        });
    }


    getDestinatairesFacturations(): void {
        this.apiService.getDestinatairesFacturations().subscribe(destinataires => {
            destinataires.sort((l1, l2) => {
                let l1Nom = '';
                let l2Nom = '';
                if (l1.description) {
                    l1Nom = l1.description.toLowerCase();
                }
                if (l2.description) {
                    l2Nom = l2.description.toLowerCase();
                }
                return l1Nom.localeCompare(l2Nom);
            });
            this.destinatairesFacturations = [...destinataires];
            this.destinatairesFacturationsReceived$.emit(this.destinatairesFacturations);
        });
    }
}
