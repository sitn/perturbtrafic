import { ChangeDetectorRef, Component, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { Subscription } from 'rxjs';
import { IEvenementType } from 'src/app/models/evenement/IEvenement';
import { ApiService } from 'src/app/services/api.service';
import { EvenementFormService } from 'src/app/services/evenement-form.service';
import { InputsUtils } from 'src/app/utils/inputs.utils';

@Component({
  selector: 'type-evenement',
  templateUrl: './type-evenement.component.html',
  styleUrls: ['./type-evenement.component.less']
})
export class TypeEvenementComponent implements OnInit, OnDestroy, OnChanges {


  typeEvenementListe: IEvenementType[];
  private subscriptions: Subscription[];

  constructor(private apiService: ApiService, private inputsUtils: InputsUtils,
    private ref: ChangeDetectorRef, public evenementFormService: EvenementFormService) {
    this.subscriptions = [];
    this.typeEvenementListe = this.inputsUtils.initiateKendoDropDownList();
  }

  onTypeChange(value) {
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnChanges(changes: SimpleChanges) {
    this.ref.detectChanges();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }


  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getTypeEvenements().subscribe((data: IEvenementType[]) => {
        this.typeEvenementListe = [...this.typeEvenementListe.concat(data)];
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
