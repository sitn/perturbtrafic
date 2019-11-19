import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';

import { Conflit } from '../models/IConflit';
import { ApiService } from '../services/api.service';
import { ConfigService } from '../services/config.service';

@Component({
  selector: 'app-conflit',
  templateUrl: './conflit.component.html',
  styleUrls: ['./conflit.component.less']
})
export class ConflitComponent implements OnInit, OnDestroy {

  private subscriptions: Subscription[];

  cols: any[] = [
    { field: 'evenementNumeroDossier', header: 'N° Evénement', type: 'string', filterable: true, show: true },
    { field: 'perturbationId', header: 'N° Perturbation', type: 'string', filterable: true, show: true },
    { field: 'evenementConflitNumeroDossier', header: 'N° Evénement en conflit', type: 'string', filterable: false, show: true },
    { field: 'perturbationConflitId', header: 'N° Perturbation en conflit', type: 'string', filterable: false, show: true }
  ];

  conflictList: Conflit[] = [];

  constructor(private apiService: ApiService, private configService: ConfigService, private router: Router) {
    this.subscriptions = [];
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  public showEvenement(eventId) {
    window.open(`${window.location.origin}/evenements/formulaire/view/${eventId}`, '_blank');
  }

  public editEvenement(eventId) {
    window.open(`${window.location.origin}/evenements/formulaire/edit/${eventId}`, '_blank');
  }


  public showPerturbation(eventId) {
    window.open(`${window.location.origin}/perturbations/formulaire/view/${eventId}`, '_blank');
  }

  public editPerturbation(eventId) {
    window.open(`${window.location.origin}/perturbations/formulaire/edit/${eventId}`, '_blank');
  }

  public showSITNConflits(id1, id2) {
    window.open(this.configService.getUrlConflits() + id1 + ',' + id2, '_blank');
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getConflits().subscribe((conflicts: Conflit[]) => {
        this.conflictList = [...conflicts];
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
