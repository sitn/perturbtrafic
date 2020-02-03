import { Component, EventEmitter, OnDestroy, OnInit, Output, HostListener } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';
import { IEvenementType } from 'src/app/models/evenement/IEvenement';
import { RechercheEvenement, RechercheEvenementForm } from 'src/app/models/evenement/IRechercheEvenement';
import { IResultatEvenement } from 'src/app/models/evenement/IResultatEvenement';
import { IContact } from 'src/app/models/IContact';
import { IOrganisme } from 'src/app/models/IOrganisme';
import { InputsUtils } from 'src/app/utils/inputs.utils';

import { IAxeMaintenance } from '../../../models/IAxeMaintenance';
import { IPointRepere } from '../../../models/IPointRepere';
import { User, IUser } from '../../../models/IUser';
import { ApiService } from '../../../services/api.service';
import { UserService } from 'src/app/services/user.service';
import { DropDownService } from 'src/app/services/dropdown.service';
import { ISuggestion } from 'src/app/models/ISuggestion';

@Component({
  selector: 'recherche-evenement',
  templateUrl: './recherche-evenement.component.html',
  styleUrls: ['./recherche-evenement.component.less']
})
export class RechercheEvenementComponent implements OnInit, OnDestroy {

  @Output() searchChange = new EventEmitter<IResultatEvenement[]>();

  form: FormGroup;

  requerants: IOrganisme[];
  responsables: IContact[];
  ajouteParListe: IUser[];
  typeEvenements: { name: string, code: number }[] = [];
  axeMaintenances: IAxeMaintenance[];
  prDebuts: IPointRepere[];
  prFins: IPointRepere[];
  users: User[];
  divisions: ISuggestion[];

  filteredRequerants: IOrganisme[];
  filteredResponsables: IContact[];
  filteredAxeMaintenances: IAxeMaintenance[];
  filteredPrDebuts: IPointRepere[];
  filteredPrFins: IPointRepere[];
  filteredAjoutePar: IUser[];

  typeEvenementListe: IEvenementType[];
  private subscriptions: Subscription[];

  get numeroDossier() { return this.form.controls.numeroDossier; }
  get requerant() { return this.form.controls.requerant; }
  get type() { return this.form.controls.typeEvenement; }
  get prevision() { return this.form.controls.prevision; }
  get axeMaintenance() { return this.form.controls.axeMaintenance; }
  get libelle() { return this.form.controls.libelle; }
  get prDebut() { return this.form.controls.prDebut; }
  get prFin() { return this.form.controls.prFin; }
  get dates() { return this.form.controls.dates; }
  get dateDebut() { return (this.form.controls.dates as FormGroup).controls.dateDebut; }
  get dateFin() { return (this.form.controls.dates as FormGroup).controls.dateFin; }
  get division() { return this.form.controls.division; }
  get ajoutePar() { return this.form.controls.ajoutePar; }

  @HostListener('document:keyup', ['$event'])
  saveOnClickEnter(e) {
    if (e.keyCode === 13) {
      this.searchEvenement();
    }
  }

  constructor(private fb: FormBuilder, private apiService: ApiService, private dropdownService: DropDownService,
    private inputsUtils: InputsUtils, private userService: UserService) {
    this.form = this.fb.group(
      new RechercheEvenementForm()
    );
    this.subscriptions = [];
    this.divisions = [...this.dropdownService.divisions];
    this.typeEvenementListe = this.inputsUtils.initiateKendoDropDownList();
  }

  ngOnInit() {
    this.dropdownService.getDivisions();
    this.setSubscriptions();
    this.apiService.getOrganismes().subscribe(data => {
      this.filteredRequerants = data;
      this.requerants = data;
    });

    this.apiService.getUsers().subscribe(data => {
      this.ajouteParListe = data;
      this.filteredAjoutePar = data;
    });

    this.apiService.getAxeMaintenances().subscribe(data => {
      data.sort((a1, a2) => {
        let a1Nom = '';
        let a2Nom = '';
        if (a1.nom_complet) {
          a1Nom = a1.nom_complet.toLowerCase();
        }
        if (a2.nom_complet) {
          a2Nom = a2.nom_complet.toLowerCase();
        }
        return a1Nom.localeCompare(a2Nom);
      });
      this.axeMaintenances = data;
      this.filteredAxeMaintenances = data;
    });

    this.axeMaintenance.valueChanges.subscribe(value => {
      this.filteredPrDebuts = [];
      this.filteredPrFins = [];
      if (value) {
        this.prDebut.enable();
        this.prFin.enable();
        this.apiService.getPrByAxeMaintenance(this.axeMaintenance.value)
          .subscribe(data => {
            this.prDebuts = data;
            this.filteredPrDebuts = data;
            this.filterPrDebuts('');
            this.prFins = data;
            this.filteredPrFins = data;
            this.filterPrFins('');
          });
      } else {
        this.prDebut.disable();
        this.prFin.disable();
      }
    });
    this.searchEvenement();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  onReset() {
    this.form.reset();
    this.resetCombobox();
    this.form.controls.srbTouche.setValue('unknown');
    this.form.controls.compteurTouche.setValue('unknown');
    this.form.controls.prevision.setValue('unknown');
    this.form.markAsPristine();
  }

  searchEvenement() {
    if (this.form.invalid) {
      return;
    }
    const recherche = new RechercheEvenement(this.form.value);
    this.apiService.searchEvenement(recherche, this.userService.currentUser).subscribe(results => {
      this.searchChange.emit(results);
    });
  }

  filterRequerants(event) {
    this.filteredRequerants = [];
    for (const requerant of this.requerants) {
      if (requerant.nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredRequerants.push(requerant);
      }
    }
  }

  filterResponsables(event) {
    this.filteredResponsables = [];
    for (const responsable of this.responsables) {
      if (responsable.nom.toLowerCase().includes(event.toLowerCase()) ||
        (responsable.prenom && responsable.prenom.toLowerCase().includes(event.toLowerCase()))) {
        this.filteredResponsables.push(responsable);
      }
    }
  }

  filterAxeMaintenances(event) {
    this.filteredAxeMaintenances = [];
    for (const axeMaintenance of this.axeMaintenances) {
      if (axeMaintenance.nom_complet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredAxeMaintenances.push(axeMaintenance);
      }
    }
    this.prDebut.reset();
    this.prFin.reset();
  }

  filterPrDebuts(event) {
    if (!this.axeMaintenance && !this.axeMaintenance.value.nom) {
      return [];
    }

    this.filteredPrDebuts = [];
    for (const prDebut of this.prDebuts) {
      if (prDebut.secteur_nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredPrDebuts.push(prDebut);
      }
    }
    this.filteredPrDebuts.sort((a1, a2) => {
      return Number(a1.segment_sequence) - Number(a2.segment_sequence) || Number(a1.secteur_sequence) - Number(a2.secteur_sequence);
    });
  }

  filterPrFins(event) {
    if (!this.axeMaintenance.value.nom) {
      return [];
    }

    this.filteredPrFins = [];
    for (const prFin of this.prFins) {
      if (prFin.secteur_nom.toLowerCase().includes(event.toLowerCase())) {
        if (!this.prDebut.value || Number(prFin.segment_sequence) > Number(this.prDebut.value.segment_sequence) ||
          (Number(prFin.segment_sequence) === Number(this.prDebut.value.segment_sequence)
            && Number(prFin.secteur_sequence) >= Number(this.prDebut.value.secteur_sequence))) {
          this.filteredPrFins.push(prFin);
        }
      }
    }
    this.filteredPrFins.sort((a1, a2) => {
      return (Number(a1.segment_sequence) - Number(a2.segment_sequence) || Number(a1.secteur_sequence) - Number(a2.secteur_sequence));
    });
  }

  onDebutPrChanged(event) {
    if (event) {
      this.prFin.setValue(null);
      this.filterPrFins('');
    } else {
      this.prFin.setValue(null);
      this.filteredPrFins = this.prFins;
    }
  }

  filterAjoutePars(event) {
    this.filteredAjoutePar = [];
    for (const user of this.ajouteParListe) {
      if (user.nomComplet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredAjoutePar.push(user);
      }
    }
  }

  resetCombobox(): void {
    this.filteredAjoutePar = [...this.ajouteParListe];
    this.filteredAxeMaintenances = [...this.axeMaintenances];
    this.filteredRequerants = [...this.requerants];
    this.filteredResponsables = [...this.responsables];
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getTypeEvenements().subscribe((data: IEvenementType[]) => {
        this.typeEvenementListe = [...this.typeEvenementListe.concat(data)];
      })
    );

    this.subscriptions.push(
      this.dropdownService.divisionsReceived$.subscribe(data => {
        this.divisions = data;
      })
    );

    this.subscriptions.push(
      this.apiService.getContacts().subscribe(data => {
        this.responsables = data;
        this.filteredResponsables = data;
      })
    );
  }

  private cleanUpSubscriptions(): void {
    let subscription: Subscription = null;

    while (subscription = this.subscriptions.pop()) {
      subscription.unsubscribe();
    }
  }
}
