import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { IPerturbationType } from 'src/app/models/perturbation/IPerturbation';
import { InputsUtils } from 'src/app/utils/inputs.utils';
import { Subscription } from 'rxjs';
import { ApiService } from 'src/app/services/api.service';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';

@Component({
  selector: 'type-perturbation',
  templateUrl: './type-perturbation.component.html',
  styleUrls: ['./type-perturbation.component.less']
})
export class TypePerturbationComponent implements OnInit, OnDestroy {

  typePerturbationListe: IPerturbationType[];

  private subscriptions: Subscription[];

  constructor(private inputsUtils: InputsUtils, private apiService: ApiService, public perturbationFormService: PerturbationFormService) {
    this.subscriptions = [];
    this.typePerturbationListe = this.inputsUtils.initiateKendoDropDownList();
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getTypePerturbations().subscribe((data: IPerturbationType[]) => {
        this.typePerturbationListe = [...this.typePerturbationListe.concat(data)];
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
