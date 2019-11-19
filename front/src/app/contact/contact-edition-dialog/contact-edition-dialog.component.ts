import { Component, EventEmitter, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';
import { ContactEditionFormGroup, IContact } from 'src/app/models/IContact';
import { IOrganisme } from 'src/app/models/IOrganisme';
import { ApiService } from 'src/app/services/api.service';
import { DropDownService } from 'src/app/services/dropdown.service';
import { NavigationService } from 'src/app/services/navigation.service';

@Component({
  selector: 'contact-edition-dialog',
  templateUrl: './contact-edition-dialog.component.html',
  styleUrls: ['./contact-edition-dialog.component.less']
})
export class ContactEditionComponent implements OnInit, OnDestroy {

  public opened = false;
  public mode: string;

  contact: IContact;

  errorMessage: string;
  warningDisplayed: boolean;

  public contactEditionFormGroup: FormGroup;
  public contactReceived$: EventEmitter<any>;
  public organismesReceived$: EventEmitter<any>;

  public organismes: IOrganisme[];
  public filteredOrganismes: IOrganisme[];

  subscriptions: Subscription[];

  constructor(private navigationService: NavigationService, private fb: FormBuilder,
    private dropDownService: DropDownService, private apiService: ApiService) {
    this.contactEditionFormGroup = this.fb.group(
      new ContactEditionFormGroup()
    );
    this.errorMessage = null;
    this.warningDisplayed = false;
    this.dropDownService.getOrganismes();
    this.filteredOrganismes = [];
    this.subscriptions = [];
  }

  ngOnInit() {
    this.errorMessage = null;
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  saveContact() {
    this.errorMessage = null;
    if (this.contactEditionFormGroup.valid) {
      if (this.mode === 'NEW') {
        this.apiService.saveContact(this.contactEditionFormGroup.value).subscribe(res => {
          if (!res.error) {
            this.navigationService.closeNewContactDialog(true);
            this.dropDownService.getOrganismes();
            this.close();
          } else {
            if (res.message.toLowerCase() === 'Contact already exists'.toLowerCase()) {
              if (this.warningDisplayed) {

              } else {
                this.errorMessage = 'Attention, ce contact existe déjà. Voulez-vous continuer ?';
              }
            } else {
              this.errorMessage = res.message.toLowerCase();
            }
          }
        });
      } else {
        this.apiService.updateContact(this.contactEditionFormGroup.value).subscribe(res => {
          if (!res.error) {
            this.navigationService.closeNewContactDialog(true);
            this.dropDownService.getOrganismes();
            this.close();
          } else {
            if (res.message.toLowerCase() === 'Contact already exists'.toLowerCase()) {
              this.errorMessage = 'Attention, ce contact existe déjà. Voulez-vous continuer ?';
            } else {
              this.errorMessage = res.message.toLowerCase();
            }
          }
        });
      }
    }
  }

  public close() {
    this.opened = false;
  }

  public open() {
    this.errorMessage = null;
    this.opened = true;
  }

  filterOrganismes(event) {
    this.filteredOrganismes = [];
    for (const organisme of this.organismes) {
      if (organisme.nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredOrganismes.push(organisme);
      }
    }
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.navigationService.openNewContactDialog$.subscribe((val: { mode: string, contact: IContact }) => {
        this.contactEditionFormGroup.reset();
        this.mode = val.mode;
        this.contact = val.contact;
        if (this.contact) {
          this.contactEditionFormGroup.patchValue(this.contact);
        }
        if (this.mode === 'READ') {
          this.contactEditionFormGroup.disable();
        } else {
          this.contactEditionFormGroup.enable();
        }
        this.open();
      })
    );
    this.subscriptions.push(
      this.dropDownService.organismesReceived$.subscribe(organismes => {
        this.organismes = organismes;
        this.filteredOrganismes = organismes;
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
