import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';
import { IEvenementType, IEvenementLibelle } from 'src/app/models/evenement/IEvenement';
import { ApiService } from 'src/app/services/api.service';
import { InputsUtils } from 'src/app/utils/inputs.utils';
import { DropDownService } from 'src/app/services/dropdown.service';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';
import { Router } from '@angular/router';

@Component({
  selector: 'perturbation-type-evenement',
  templateUrl: './perturbation-type-evenement.component.html',
  styleUrls: ['./perturbation-type-evenement.component.less']
})
export class PerturbationTypeEvenementComponent implements OnInit, OnDestroy {

  private subscriptions: Subscription[];
  typeEvenementListe: IEvenementType[];
  evenementsListe: IEvenementLibelle[];
  filteredEvenementsListe: any[];


  constructor(private inputsUtils: InputsUtils,
    private apiService: ApiService, private router: Router,
    private dropDownService: DropDownService,
    public perturbationFormService: PerturbationFormService) {
    this.subscriptions = [];
    this.typeEvenementListe = this.inputsUtils.initiateKendoDropDownList();
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  filterEvenement(event) {
    this.filteredEvenementsListe = [];
    for (const eve of this.evenementsListe) {
      if (eve.label.toLowerCase().includes(event.toLowerCase())) {
        this.filteredEvenementsListe.push(eve);
      }
    }
  }

  openEvenement() {
    if (this.perturbationFormService.evenement && this.perturbationFormService.evenement.value) {
      window.open(`${window.location.origin}/evenements/formulaire/view/${this.perturbationFormService.evenement.value}`, '_blank');
    }
  }

  private setSubscriptions(): void {

    /* this.subscriptions.push(
      this.apiService.getTypeEvenements().subscribe((data: IEvenementType[]) => {
        this.typeEvenementListe = [...this.typeEvenementListe.concat(data)];
      })
    ); */


    this.subscriptions.push(
      this.dropDownService.libellesEvenementsReceived$.subscribe(data => {
        this.evenementsListe = data;
        this.filteredEvenementsListe = data;
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
