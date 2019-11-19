import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { Conflit } from 'src/app/models/IConflit';
import { ApiService } from 'src/app/services/api.service';
import { ConfigService } from 'src/app/services/config.service';

@Component({
  selector: 'conflits-evenement',
  templateUrl: './conflits-evenement.component.html',
  styleUrls: ['./conflits-evenement.component.less']
})
export class ConflitsEvenementComponent implements OnInit, OnDestroy {

  private subscriptions: Subscription[];

  public conflicts: Conflit[];

  constructor(private apiService: ApiService, private route: ActivatedRoute, private router: Router, private configService: ConfigService) {
    this.subscriptions = [];
    this.conflicts = [];
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  public editPerturbation(eventId) {
    this.router.navigate([`/perturbations/formulaire/edit/${eventId}`]);
  }

  public showGuichetCarto() {
    window.open(this.configService.getUrlGuichetCarto(), '_blank');
  }


  private setSubscriptions(): void {

    const evenementId = this.route.snapshot.paramMap.get('id');
    if (evenementId) {
      this.subscriptions.push(
        this.apiService.getConflitsByEvenementId(evenementId).subscribe(res => {
          if (res && res.length > -1) {
            this.conflicts = res.slice(0, 10);
          }
        })
      );
    }

  }


  private cleanUpSubscriptions(): void {
    let subscription: Subscription = null;

    while (subscription = this.subscriptions.pop()) {
      subscription.unsubscribe();
    }
  }
}
