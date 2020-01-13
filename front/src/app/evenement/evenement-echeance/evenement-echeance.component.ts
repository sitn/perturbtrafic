import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { EvenementEcheance } from 'src/app/models/evenement/IEvenementEcheance';
import { ApiService } from 'src/app/services/api.service';
import { CookieService } from 'src/app/services/cookie.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'evenement-echeance',
  templateUrl: './evenement-echeance.component.html',
  styleUrls: ['./evenement-echeance.component.less']
})
export class EvenementEcheanceComponent implements OnInit, OnDestroy {

  private subscriptions: Subscription[];

  public opened = false;
  public endedEvenements = [];

  cols: any[] = [
    { field: 'numeroDossier', header: 'N° dossier', type: 'string', filterable: false },
    { field: 'libelle', header: 'Libellé', type: 'string', filterable: false },
    { field: 'dateDebut', header: 'Début', type: 'date', format: 'dd.MM.yyyy', filterable: false },
    { field: 'action', header: 'Actions', type: 'action', filterable: false, width: '40px' }

  ];

  constructor(private apiService: ApiService, private router: Router,
    private cookieService: CookieService, private userService: UserService) {
    this.subscriptions = [];
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  public close() {
    this.cookieService.remove('show-popup');
    this.opened = false;
  }

  public open() {
    this.opened = true;
  }

  editEvenement(evenement) {
    this.router.navigate([`/evenements/formulaire/edit/${evenement.id}`]);
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getEvenementsEcheances(this.userService.currentUser).subscribe((echeances: EvenementEcheance[]) => {
        this.endedEvenements = [...echeances];
        if (this.endedEvenements && this.endedEvenements.length > 0) {
          this.open();
        }
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
