import { Component, EventEmitter, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';
import { IOrganisme, OrganismeEditionFormGroup } from 'src/app/models/IOrganisme';
import { ApiService } from 'src/app/services/api.service';
import { DropDownService } from 'src/app/services/dropdown.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { ILocaliteNPA } from 'src/app/models/ILocalite';

@Component({
  selector: 'organisme-edition-dialog',
  templateUrl: './organisme-edition-dialog.component.html',
  styleUrls: ['./organisme-edition-dialog.component.less']
})
export class OrganismeEditionComponent implements OnInit, OnDestroy {

  public opened = false;
  public mode: string;

  organisme: IOrganisme;

  public localites: ILocaliteNPA[];
  public filteredLocalites: ILocaliteNPA[];

  public organismeEditionFormGroup: FormGroup;
  public contactReceived$: EventEmitter<any>;
  public organismesReceived$: EventEmitter<any>;

  subscriptions: Subscription[];

  constructor(private navigationService: NavigationService, private fb: FormBuilder, private apiService: ApiService,
    private dropDownService: DropDownService) {
    this.organismeEditionFormGroup = this.fb.group(
      new OrganismeEditionFormGroup()
    );
    this.localites = [...this.dropDownService.localitesNPA];
    this.filteredLocalites = [...this.dropDownService.localitesNPA];
    this.subscriptions = [];
    this.dropDownService.getLocalitesNPA();
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  saveOrganisme() {
    if (this.organismeEditionFormGroup.valid) {
      if (this.mode === 'NEW') {
        this.apiService.saveOrganisme(this.organismeEditionFormGroup.value).subscribe(res => {
          if (!res.error) {
            this.navigationService.closeNewOrganismeDialog(true);
            this.dropDownService.getOrganismes();
            this.close();
          }
        });
      } else {
        this.apiService.updateOrganisme(this.organismeEditionFormGroup.value).subscribe(res => {
          if (!res.error) {
            this.navigationService.closeNewOrganismeDialog(true);
            this.dropDownService.getOrganismes();
            this.close();
          }
        });
      }
    } else {
      this.markAsTouched();
    }
  }

  filterLocalites(event) {
    this.filteredLocalites = [];
    for (const localite of this.localites) {
      if (localite.npa_nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredLocalites.push(localite);
      }
    }
  }

  markAsTouched() {
    this.markFormGroupTouched(this.organismeEditionFormGroup);
  }

  markFormGroupTouched = (formGroup) => {
    (<any>Object).values(formGroup.controls).forEach(control => {
      control.markAsTouched();

      if (control.controls) {
        this.markFormGroupTouched(control);
      }
    });
  }


  public close() {
    this.opened = false;
  }

  public open() {
    this.opened = true;
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.navigationService.openNewOrganismeDialog$.subscribe((val: { mode: string, organisme: IOrganisme }) => {
        this.organismeEditionFormGroup.reset();
        this.mode = val.mode;
        console.log(val.organisme);
        this.organisme = val.organisme;
        if (this.organisme) {
          this.organismeEditionFormGroup.patchValue(this.organisme);
        }
        console.log('formGroup : ', this.organismeEditionFormGroup);
        if (this.mode === 'READ') {
          this.organismeEditionFormGroup.disable();
        } else {
          this.organismeEditionFormGroup.enable();
        }
        this.open();
      })
    );

    this.subscriptions.push(
      this.dropDownService.localitesNPAReceived$.subscribe(data => {
        this.filteredLocalites = data;
        this.localites = data;
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
