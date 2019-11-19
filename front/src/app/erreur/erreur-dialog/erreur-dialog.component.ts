import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { NavigationService } from 'src/app/services/navigation.service';

@Component({
  selector: 'erreur-dialog',
  templateUrl: './erreur-dialog.component.html',
  styleUrls: ['./erreur-dialog.component.less']
})
export class ErreurDialogComponent implements OnInit, OnDestroy {

  public opened = false;

  public errorMessage: string;
  public title = 'Erreur survenue';

  subscriptions: Subscription[];

  constructor(private navigationService: NavigationService) {
    this.subscriptions = [];
    this.errorMessage = 'Une erreur est survenue';
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  public close() {
    this.opened = false;
  }

  public open() {
    this.opened = true;
  }

  reset() {
    this.title = 'Erreur';
    this.errorMessage = 'Une erreur est survenue';
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.navigationService.openErrorDialog$.subscribe(val => {
        if (val) {
          if (val.message) {
            this.errorMessage = val.message;
          }
          if (val.title) {
            this.title = val.title;
          }
        }
        this.open();
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
