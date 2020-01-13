import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { IUser, IUserAD } from 'src/app/models/IUser';
import { DropDownService } from 'src/app/services/dropdown.service';
import { Subscription } from 'rxjs';

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
    this.newUsers = [];
    this.newUsersOpened = true;
    this.apiService.checkNewUsers().subscribe(users => {
      this.newUsers = users;
    });
  }

  closeNewUsersDialog(): void {
    this.newUsersOpened = false;
    this.newUsers = [];
  }

  registerNewUsers(): void {

    this.apiService.updateNewUsers(this.newUsers).subscribe(res => {
      if (!res.error) {
        this.closeNewUsersDialog();
      }
    });
  }

  private setSubscriptions(): void {
  }
}
