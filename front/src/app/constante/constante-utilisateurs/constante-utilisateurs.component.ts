import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { IUser, IUserAD } from 'src/app/models/IUser';
import { DropDownService } from 'src/app/services/dropdown.service';
import { Subscription } from 'rxjs';
import { IOrganisme } from 'src/app/models/IOrganisme';

@Component({
  selector: 'constante-utilisateurs',
  templateUrl: './constante-utilisateurs.component.html',
  styleUrls: ['./constante-utilisateurs.component.less']
})
export class ConstanteUtilisateursComponent implements OnInit {

  newUsersOpened = false;
  missingOrganisme = false;
  users: IUser[];
  newUsers: IUserAD[];
  subscriptions: Subscription[];
  organismes: IOrganisme[];
  constructor(private apiService: ApiService, private dropdownService: DropDownService) { }

  ngOnInit() {
    this.users = [];
    this.newUsers = [];
    this.subscriptions = [];
    this.apiService.getUsers().subscribe(users => {
      this.users = users;
    });
    this.setSubscriptions();
  }


  checkNewUsers(): void {
    this.dropdownService.getOrganismes();
    this.newUsersOpened = true;
    this.apiService.checkNewUsers().subscribe(users => {
      this.newUsers = users;
    });
  }

  closeNewUsersDialog(): void {
    this.newUsersOpened = false;
  }

  registerNewUsers(): void {
    this.missingOrganisme = false;
    if (this.newUsers.some(user => {
      return !user.id_organisme;
    })) {
      this.missingOrganisme = true;
    } else {
      this.missingOrganisme = false;
    }

    if (!this.missingOrganisme) {
      this.apiService.updateNewUsersWithOrganismes(this.newUsers).subscribe(res => {
        if (!res.error) {
          this.closeNewUsersDialog();
        }
      });
    }
  }

  private setSubscriptions(): void {


    this.subscriptions.push(
      this.dropdownService.organismesReceived$.subscribe(organismes => {
        this.organismes = [...organismes];
      })
    );
  }
}
