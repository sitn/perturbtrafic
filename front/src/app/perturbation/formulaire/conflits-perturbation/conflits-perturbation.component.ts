import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { Conflit, IConflitServer } from 'src/app/models/IConflit';
import { ApiService } from 'src/app/services/api.service';
import { ConfigService } from 'src/app/services/config.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'conflits-perturbation',
  templateUrl: './conflits-perturbation.component.html',
  styleUrls: ['./conflits-perturbation.component.less']
})
export class ConflitsPerturbationComponent implements OnInit, OnDestroy {

  private subscriptions: Subscription[];

  public conflicts: Conflit[];

  constructor(private apiService: ApiService, private route: ActivatedRoute, private router: Router, private configService: ConfigService,
    private userService: UserService) {
    this.subscriptions = [];
    this.conflicts = [];
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  public editPerturbation(perturbationId) {
    window.open(`${window.location.origin}/perturbations/formulaire/edit/${perturbationId}`);
  }

  public showGuichetCarto(perturbationId, evenementId) {
    if (evenementId) {
      window.open(this.configService.getUrlConflits() + evenementId + ',' + perturbationId, '_blank');
    }
  }

  isEven(i: number) {
    return i % 2 === 0;
  }

  isOdd(i: number) {
    return Math.abs(i % 2) === 1;
  }

  setConflits(conflicts: Conflit[]): void {
    this.conflicts = conflicts;
  }

  private setSubscriptions(): void {

    const perturbation = this.route.snapshot.paramMap.get('id');
    if (perturbation) {
      this.subscriptions.push(
        this.apiService.getConflitsByPerturbationId(perturbation).subscribe(res => {
          if (res && res.length > -1) {
            this.conflicts = res;
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
