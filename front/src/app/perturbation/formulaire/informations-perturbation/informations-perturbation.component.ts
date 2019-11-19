import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { IPerturbationEtat } from 'src/app/models/perturbation/IPerturbation';
import { Subscription } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { InputsUtils } from 'src/app/utils/inputs.utils';
import { IContact } from 'src/app/models/IContact';
import { DropDownService } from 'src/app/services/dropdown.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';

@Component({
  selector: 'informations-perturbation',
  templateUrl: './informations-perturbation.component.html',
  styleUrls: ['./informations-perturbation.component.less']
})
export class InformationsPerturbationComponent implements OnInit, OnDestroy {

  public timeMask = '00:00';

  public contacts: IContact[];

  public filteredResponsableTrafic: IContact[];

  get etat() { return this.perturbationFormService.perturbationForm.controls.etat; }

  etatPerturbationListe: IPerturbationEtat[];
  subscriptions: Subscription[];

  constructor(private apiService: ApiService, private inputsUtils: InputsUtils, private dropDownService: DropDownService,
    private navigationService: NavigationService, public perturbationFormService: PerturbationFormService) {
    this.subscriptions = [];
    this.etatPerturbationListe = this.inputsUtils.initiateKendoDropDownList();
    this.contacts = [...this.dropDownService.contacts];
    this.filteredResponsableTrafic = [...this.dropDownService.contacts];
  }

  ngOnInit() {
    this.setSubscriptions();
    console.log(this.perturbationFormService.perturbationForm);
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  filterResponsableTrafic(event) {
    this.filteredResponsableTrafic = [];
    for (const contact of this.contacts) {
      if (contact.nomComplet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredResponsableTrafic.push(contact);
      }
    }
  }

  setResponsableTraficValues(contact: IContact) {
    console.log(contact);
    this.perturbationFormService.responsableTraficContactInfos.controls.nom.setValue(contact.nom);
    this.perturbationFormService.responsableTraficContactInfos.controls.prenom.setValue(contact.prenom);
    this.perturbationFormService.responsableTraficContactInfos.controls.mobile.setValue(contact.mobile);
    this.perturbationFormService.responsableTraficContactInfos.controls.telephone.setValue(contact.telephone);
    this.perturbationFormService.responsableTraficContactInfos.controls.fax.setValue(contact.fax);
    this.perturbationFormService.responsableTraficContactInfos.controls.courriel.setValue(contact.courriel);
  }

  createNewContact() {
    this.navigationService.openNewContactDialog('NEW', null);
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getEtatsPerturbations().subscribe((data: IPerturbationEtat[]) => {
        this.etatPerturbationListe = [...this.etatPerturbationListe.concat(data)];
      })
    );
    this.subscriptions.push(
      this.dropDownService.contactReceived$.subscribe(contacts => {
        this.contacts = [...contacts];
        this.filteredResponsableTrafic = [...contacts];
      })
    );


    this.subscriptions.push(
      this.perturbationFormService.responsableTraficId.valueChanges.subscribe(val => {
        this.perturbationFormService.responsableTraficContactInfos.reset();
        if (val) {
          this.setResponsableTraficValues(val);
          this.perturbationFormService.responsableTraficContactInfos.disable();
        } else {
          this.perturbationFormService.responsableTraficContactInfos.enable();
        }
      })
    );

    /* this.subscriptions.push(
      this.perturbationFormService.typePerturbation.valueChanges.subscribe(val => {
        if (val && this.perturbationFormService.evenement.value) {
          this.perturbationFormService.enableGeneralInfos();
        } else {
          this.perturbationFormService.disableGeneralInfos();
        }
      })
    );

    this.subscriptions.push(
      this.perturbationFormService.evenement.valueChanges.subscribe(val => {
        if (val && this.perturbationFormService.typePerturbation.value) {
          this.perturbationFormService.enableGeneralInfos();
        } else {
          this.perturbationFormService.disableGeneralInfos();
        }
      })
    ); */
  }

  private cleanUpSubscriptions(): void {
    let subscription: Subscription = null;

    while (subscription = this.subscriptions.pop()) {
      subscription.unsubscribe();
    }
  }
}
