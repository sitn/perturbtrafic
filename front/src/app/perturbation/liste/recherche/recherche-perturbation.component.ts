import { Component, EventEmitter, OnDestroy, OnInit, Output, HostListener } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';
import { IEvenementType } from 'src/app/models/evenement/IEvenement';
import { IAxeMaintenance } from 'src/app/models/IAxeMaintenance';
import { IContact } from 'src/app/models/IContact';
import { IPointRepere } from 'src/app/models/IPointRepere';
import { User, IUser } from 'src/app/models/IUser';
import { IPerturbationEtat, IPerturbationType } from 'src/app/models/perturbation/IPerturbation';
import { RecherchePerturbation, RecherchePerturbationForm } from 'src/app/models/perturbation/IRecherchePerturbation';
import { ResultatPerturbation } from 'src/app/models/perturbation/IResultatPerturbation';
import { ApiService } from 'src/app/services/api.service';
import { InputsUtils } from 'src/app/utils/inputs.utils';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'recherche-perturbation',
  templateUrl: './recherche-perturbation.component.html',
  styleUrls: ['./recherche-perturbation.component.less']
})
export class RecherchePerturbationComponent implements OnInit, OnDestroy {

  @Output() searchChange = new EventEmitter<ResultatPerturbation[]>();

  recherchePerturbationForm: FormGroup;

  typePerturbationListe: IPerturbationType[];
  typeEvenementListe: IEvenementType[];
  etatPerturbationListe: IPerturbationEtat[];
  ajouteParListe: IUser[];

  typeEvenements: { name: string, code: number }[];
  etats: { name: string, code: number }[];
  axeMaintenances: IAxeMaintenance[];
  prDebuts: IPointRepere[];
  prFins: IPointRepere[];
  users: User[];

  filteredAxeMaintenances: IAxeMaintenance[];
  filteredPrDebuts: IPointRepere[];
  filteredPrFins: IPointRepere[];
  filteredAjoutePar: IUser[];

  private subscriptions: Subscription[];

  get numeroDossier() { return this.recherchePerturbationForm.controls.numeroDossier; }
  get typePerturbation() { return this.recherchePerturbationForm.controls.typePerturbation; }
  get etatPerturbation() { return this.recherchePerturbationForm.controls.etatPerturbation; }
  get typeEvenement() { return this.recherchePerturbationForm.controls.typeEvenement; }
  get axeMaintenance() { return this.recherchePerturbationForm.controls.axeMaintenance; }
  get description() { return this.recherchePerturbationForm.controls.description; }
  get prDebut() { return this.recherchePerturbationForm.controls.prDebut; }
  get prFin() { return this.recherchePerturbationForm.controls.prFin; }
  get dates() { return this.recherchePerturbationForm.controls.dates; }
  get urgence() { return this.recherchePerturbationForm.controls.urgence; }
  get etat() { return this.recherchePerturbationForm.controls.etat; }
  get dateDebut() { return (this.recherchePerturbationForm.controls.dates as FormGroup).controls.dateDebut; }
  get dateFin() { return (this.recherchePerturbationForm.controls.dates as FormGroup).controls.dateFin; }
  get ajoutePar() { return this.recherchePerturbationForm.controls.ajoutePar; }

  @HostListener('document:keyup', ['$event'])
  saveOnClickEnter(e) {
    if (e.keyCode === 13 && !(e.target && e.target.type === 'textarea')) {
      this.onSearchPerturbation();
    }
  }

  constructor(private fb: FormBuilder, private apiService: ApiService, private inputsUtils: InputsUtils, private userService: UserService) {
    this.recherchePerturbationForm = this.fb.group(
      new RecherchePerturbationForm()
    );
    this.subscriptions = [];
    this.typePerturbationListe = this.inputsUtils.initiateKendoDropDownList();
    this.etatPerturbationListe = this.inputsUtils.initiateKendoDropDownList();
    this.typeEvenementListe = this.inputsUtils.initiateKendoDropDownList();
  }

  ngOnInit() {
    this.prDebut.disable();
    this.prFin.disable();
    this.setSubscriptions();
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
    this.onSearchPerturbation();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  private dateOrderValidator(g: FormGroup) {
    const valueDebut = g.get('dateDebut').value;
    const valueFin = g.get('dateFin').value;

    if (valueDebut && valueFin) {
      const debut = new Date();
      const fin = new Date(g.get('dateFin').value);

      return fin > debut ? null : { 'order': true };
    }

    return null;
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

  onDebutPrChanged(event) {
    if (event) {
      this.prFin.setValue(null);
      this.filterPrFins('');
    } else {
      this.prFin.setValue(null);
      this.filteredPrFins = this.prFins;
    }
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

  filterAjoutePars(event) {
    this.filteredAjoutePar = [];
    for (const user of this.ajouteParListe) {
      if (user.nomComplet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredAjoutePar.push(user);
      }
    }
  }

  onReset() {
    this.recherchePerturbationForm.reset();
    this.resetCombobox();
    this.recherchePerturbationForm.controls.compteurTouche.setValue('unknown');
    this.recherchePerturbationForm.controls.urgence.setValue('unknown');
    this.recherchePerturbationForm.markAsPristine();
  }

  onSearchPerturbation() {
    if (this.recherchePerturbationForm.invalid) {
      return;
    }
    const recherche = new RecherchePerturbation(this.recherchePerturbationForm.value);
    // this.searchChange.emit(recherche);
    const formModel = this.recherchePerturbationForm.value;
    this.apiService.searchPerturbations(recherche, this.userService.currentUser).subscribe(results => {
      this.searchChange.emit(results);
    });
  }

  submitForm() {
    if (this.recherchePerturbationForm.invalid) {
      return;
    }
    const recherche = new RecherchePerturbation(this.recherchePerturbationForm.value);
    // this.searchChange.emit(recherche);
    const formModel = this.recherchePerturbationForm.value;

  }

  resetCombobox(): void {
    this.filteredAjoutePar = [...this.ajouteParListe];
    this.filteredAxeMaintenances = [...this.axeMaintenances];
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getTypePerturbations().subscribe((data: IPerturbationType[]) => {
        this.typePerturbationListe = [...this.typePerturbationListe.concat(data)];
      })
    );

    this.subscriptions.push(
      this.apiService.getEtatsPerturbations().subscribe((data: IPerturbationEtat[]) => {
        this.etatPerturbationListe = [...this.etatPerturbationListe.concat(data)];
      })
    );

    this.subscriptions.push(
      this.apiService.getTypeEvenements().subscribe((data: IEvenementType[]) => {
        this.typeEvenementListe = [...this.typeEvenementListe.concat(data)];
      })
    );

    this.subscriptions.push(
      this.apiService.getUsers().subscribe((data: IUser[]) => {
        this.filteredAjoutePar = data;
        this.ajouteParListe = data;
      })
    );

    this.subscriptions.push(
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
